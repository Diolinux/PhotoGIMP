from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import sys
import unittest
from xml.etree import ElementTree


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = (
    ROOT / ".config" / "GIMP" / "3.0" / "plug-ins" / "photogimp-workspaces"
)
CORE_PATH = PLUGIN_ROOT / "workspace_core.py"
ENTRYPOINT = PLUGIN_ROOT / "photogimp-workspaces.py"
SHORTCUTSRC = ROOT / ".config" / "GIMP" / "3.0" / "shortcutsrc"
TOOLRC = ROOT / ".config" / "GIMP" / "3.0" / "toolrc"
GIMP_MODIFIERS = {"<Primary>": "Ctrl", "<Shift>": "Shift", "<Alt>": "Alt"}

spec = importlib.util.spec_from_file_location("workspace_core", CORE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load the PhotoGIMP workspace core")
workspace_core = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = workspace_core
spec.loader.exec_module(workspace_core)


class WorkspaceCoreTests(unittest.TestCase):
    def test_three_modes_have_icons_tools_and_unique_shortcuts(self) -> None:
        self.assertEqual(
            set(workspace_core.MODE_DEFINITIONS),
            {"designer", "artist", "comic"},
        )
        for mode in workspace_core.MODE_DEFINITIONS.values():
            self.assertGreaterEqual(len(mode["tools"]), 8)
            self.assertTrue((PLUGIN_ROOT / "icons" / mode["icon"]).is_file())
            shortcuts = [tool[1] for tool in mode["tools"]]
            self.assertEqual(len(shortcuts), len(set(shortcuts)))

    def test_palette_shortcuts_match_the_active_gimp_bindings(self) -> None:
        bindings: dict[str, set[tuple[frozenset[str], str]]] = {}
        for action, accelerator in re.findall(
            r'^\(action "([^"]+)" "([^"]+)"\)', SHORTCUTSRC.read_text(encoding="utf-8"), re.M
        ):
            modifiers = frozenset(
                GIMP_MODIFIERS[token] for token in re.findall(r"<[^>]+>", accelerator)
            )
            key = re.sub(r"<[^>]+>", "", accelerator).upper()
            bindings.setdefault(action, set()).add((modifiers, key))

        for mode_id, mode in workspace_core.MODE_DEFINITIONS.items():
            for label, shortcut, _icon, action in mode["tools"]:
                with self.subTest(mode=mode_id, tool=label):
                    modifiers, key = workspace_core.parse_shortcut(shortcut)
                    self.assertIn((frozenset(modifiers), key), bindings.get(action, set()))

    def test_palette_uses_existing_gimp_tool_icon_names(self) -> None:
        for mode in workspace_core.MODE_DEFINITIONS.values():
            for _label, _shortcut, icon, _action in mode["tools"]:
                self.assertRegex(icon, r"^gimp-tool-[a-z-]+$")
                self.assertNotEqual(icon, "gimp-tool-rectangle-select")

    def test_shortcut_parsing(self) -> None:
        self.assertEqual(
            workspace_core.parse_shortcut("Shift+Alt+O"), (("Shift", "Alt"), "O")
        )
        self.assertEqual(workspace_core.parse_shortcut("Ctrl+t"), (("Ctrl",), "T"))
        for invalid in ("", "Ctrl+", "Super+K", "Ctrl+Ctrl+K", "F5", "Ctrl+1"):
            with self.subTest(shortcut=invalid):
                with self.assertRaises(ValueError):
                    workspace_core.parse_shortcut(invalid)

    def test_saved_mode_falls_back_to_designer(self) -> None:
        self.assertEqual(workspace_core.normalize_mode("comic\n"), "comic")
        self.assertEqual(workspace_core.normalize_mode("unknown"), "designer")
        self.assertEqual(workspace_core.normalize_mode(None), "designer")

    def test_image_id_is_read_from_the_gimp_window_title(self) -> None:
        self.assertEqual(
            workspace_core.image_id_from_title(
                "*[Untitled]-12.0 (RGB color 8-bit, 1 layer) 1920x1080 – GIMP"
            ),
            12,
        )
        self.assertEqual(
            workspace_core.image_id_from_title("foto-2024-3.1 (RGB) 800x600 – GIMP"), 3
        )
        self.assertIsNone(
            workspace_core.image_id_from_title("GNU Image Manipulation Program")
        )

    def test_shape_is_drawn_after_the_drag_ends(self) -> None:
        ready = workspace_core.shape_ready
        self.assertFalse(ready(None, 5, False, 1))
        self.assertFalse(ready((0, 0, 10, 10), 5, True, 1))
        self.assertFalse(ready((0, 0, 10, 10), 0, False, 1))
        self.assertTrue(ready((0, 0, 10, 10), 1, False, 1))

    def test_shapes_activate_the_matching_selection_tool(self) -> None:
        shapes = workspace_core.SHAPES
        self.assertEqual(set(shapes), {"rectangle", "ellipse"})
        self.assertEqual(shapes["rectangle"]["select_shortcut"], "M")
        self.assertEqual(shapes["ellipse"]["select_shortcut"], "Shift+M")
        shortcuts = SHORTCUTSRC.read_text(encoding="utf-8")
        self.assertIn('(action "tools-rect-select" "m")', shortcuts)
        self.assertIn('(action "tools-ellipse-select" "<Shift>m")', shortcuts)
        self.assertEqual(workspace_core.SHAPE_STYLES[0][0], 0)

    def test_modes_cycle_and_start_with_their_primary_tool(self) -> None:
        self.assertEqual(workspace_core.next_mode("designer"), "artist")
        self.assertEqual(workspace_core.next_mode("artist"), "comic")
        self.assertEqual(workspace_core.next_mode("comic"), "designer")
        self.assertEqual(workspace_core.primary_tool("designer")[3], "tools-move")
        self.assertEqual(workspace_core.primary_tool("artist")[3], "tools-paintbrush")
        self.assertEqual(workspace_core.primary_tool("comic")[3], "tools-ink")

    def test_toolbox_tools_exist_in_toolrc(self) -> None:
        known = set(re.findall(r'\(GimpToolInfo "([^"]+)"', TOOLRC.read_text(encoding="utf-8")))
        for mode_id, tools in workspace_core.TOOLBOX_TOOLS.items():
            with self.subTest(mode=mode_id):
                self.assertLessEqual(tools, known)
            primary = workspace_core.primary_tool(mode_id)[3]
            self.assertIn(primary.replace("tools-", "gimp-", 1) + "-tool", tools)

    def test_toolbox_for_mode_only_changes_visibility(self) -> None:
        toolrc = TOOLRC.read_text(encoding="utf-8")
        for mode_id, tools in workspace_core.TOOLBOX_TOOLS.items():
            with self.subTest(mode=mode_id):
                updated = workspace_core.toolbox_for_mode(toolrc, mode_id)
                self.assertEqual(workspace_core.toolbox_for_mode(updated, mode_id), updated)
                self.assertEqual(
                    re.sub(r"\(visible (?:yes|no)\)|\(active-tool \"[^\"]+\"\)", "", updated),
                    re.sub(r"\(visible (?:yes|no)\)|\(active-tool \"[^\"]+\"\)", "", toolrc),
                )
                for tool, flag in re.findall(
                    r'\(GimpToolInfo "([^"]+)"[^()]*(?:\([^()]*\)\s*)*?\(visible (yes|no)\)',
                    updated,
                ):
                    self.assertEqual(flag == "yes", tool in tools, tool)

    def test_toolbox_groups_follow_their_visible_children(self) -> None:
        toolrc = (
            '(GimpToolGroup "tool group"\n'
            "    (visible yes)\n"
            '    (active-tool "gimp-warp-tool")\n'
            "    (children\n"
            '        (GimpToolInfo "gimp-warp-tool"\n'
            "            (visible yes))\n"
            '        (GimpToolInfo "gimp-cage-tool"\n'
            "            (visible yes))))\n"
        )
        designer = workspace_core.toolbox_for_mode(toolrc, "designer")
        self.assertEqual(designer.count("(visible no)"), 3)
        artist = workspace_core.toolbox_for_mode(toolrc, "artist")
        self.assertIn('(active-tool "gimp-warp-tool")', artist)
        self.assertEqual(artist.count("(visible yes)"), 2)

    def test_toolbox_helper_applies_the_saved_mode(self) -> None:
        import tempfile

        helper_spec = importlib.util.spec_from_file_location(
            "apply_toolbox", PLUGIN_ROOT / "apply_toolbox.py"
        )
        helper = importlib.util.module_from_spec(helper_spec)
        helper_spec.loader.exec_module(helper)
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory)
            (config / "toolrc").write_text(TOOLRC.read_text(encoding="utf-8"), encoding="utf-8")
            (config / "photogimp-workspace-mode").write_text("comic", encoding="utf-8")
            helper.apply(config)
            self.assertEqual(
                (config / "toolrc").read_text(encoding="utf-8"),
                workspace_core.toolbox_for_mode(TOOLRC.read_text(encoding="utf-8"), "comic"),
            )
            self.assertFalse((config / "toolrc.photogimp-tmp").exists())

    def test_toolbox_helper_relaunches_only_recent_restart_requests(self) -> None:
        import tempfile

        helper_spec = importlib.util.spec_from_file_location(
            "apply_toolbox", PLUGIN_ROOT / "apply_toolbox.py"
        )
        helper = importlib.util.module_from_spec(helper_spec)
        helper_spec.loader.exec_module(helper)
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory)
            executable = config / "gimp.exe"
            executable.write_bytes(b"")
            request = config / "photogimp-restart"

            request.write_text(f"1000\n{executable}\n", encoding="utf-8")
            self.assertEqual(helper.pending_relaunch(config, 1010), str(executable))
            self.assertFalse(request.exists())

            request.write_text(f"1000\n{executable}\n", encoding="utf-8")
            self.assertIsNone(helper.pending_relaunch(config, 1000 + 3600))
            self.assertFalse(request.exists())

            request.write_text(f"1000\n{config / 'missing.exe'}\n", encoding="utf-8")
            self.assertIsNone(helper.pending_relaunch(config, 1010))
            self.assertIsNone(helper.pending_relaunch(config, 1010))

    def test_mode_switcher_is_anchored_to_the_main_window_top_right(self) -> None:
        self.assertEqual(
            workspace_core.mode_switcher_position(
                (16, 16, 1904, 1027),
                (252, 34),
                titlebar_height=31,
            ),
            (1644, 47),
        )

    def test_mode_switcher_position_stays_inside_small_windows(self) -> None:
        self.assertEqual(
            workspace_core.mode_switcher_position(
                (100, 50, 300, 120),
                (260, 80),
                titlebar_height=40,
            ),
            (100, 50),
        )

    def test_a4_size_and_landscape_orientation(self) -> None:
        portrait = workspace_core.page_size_pixels("a4", 300, "portrait")
        landscape = workspace_core.page_size_pixels("a4", 300, "landscape")

        self.assertEqual(portrait, (2480, 3508))
        self.assertEqual(landscape, portrait[::-1])

    def test_webtoon_size_is_resolution_independent(self) -> None:
        self.assertEqual(
            workspace_core.page_size_pixels("webtoon", 72, "portrait"),
            workspace_core.page_size_pixels("webtoon", 600, "portrait"),
        )

    def test_every_panel_layout_stays_inside_page_and_does_not_overlap(self) -> None:
        page_width, page_height = 1600, 2400
        margin, gutter = 80, 24

        for layout_id, layout in workspace_core.PANEL_LAYOUTS.items():
            with self.subTest(layout=layout_id):
                rectangles = workspace_core.panel_rectangles(
                    layout_id, page_width, page_height, margin, gutter
                )
                self.assertEqual(len(rectangles), len(layout["cells"]))
                for x, y, width, height in rectangles:
                    self.assertGreaterEqual(x, margin)
                    self.assertGreaterEqual(y, margin)
                    self.assertLessEqual(x + width, page_width - margin)
                    self.assertLessEqual(y + height, page_height - margin)
                for index, first in enumerate(rectangles):
                    for second in rectangles[index + 1 :]:
                        self.assertFalse(self._overlaps(first, second))

    def test_invalid_page_geometry_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "leave no room"):
            workspace_core.panel_rectangles(
                "six_grid", 100, 100, 45, 20
            )
        with self.assertRaisesRegex(ValueError, "Unknown paper"):
            workspace_core.page_size_pixels("letter", 300, "portrait")

    def test_screentone_validation_accepts_supported_styles(self) -> None:
        for style in workspace_core.TONE_STYLES:
            self.assertEqual(
                workspace_core.validate_tone_settings(style, 12, 4, 45, 35),
                (style, 12, 4.0, 45.0, 35.0),
            )

    def test_screentone_validation_rejects_oversized_marks(self) -> None:
        with self.assertRaisesRegex(ValueError, "Mark size"):
            workspace_core.validate_tone_settings("dots", 8, 9, 0, 50)

    @staticmethod
    def _overlaps(first, second) -> bool:
        first_x, first_y, first_width, first_height = first
        second_x, second_y, second_width, second_height = second
        return not (
            first_x + first_width <= second_x
            or second_x + second_width <= first_x
            or first_y + first_height <= second_y
            or second_y + second_height <= first_y
        )


class WorkspacePluginAssetTests(unittest.TestCase):
    def test_entrypoint_name_matches_plugin_directory(self) -> None:
        self.assertEqual(ENTRYPOINT.stem, PLUGIN_ROOT.name)

    def test_plugin_sources_compile_without_importing_gimp(self) -> None:
        for source in (CORE_PATH, ENTRYPOINT):
            compile(source.read_text(encoding="utf-8"), str(source), "exec")

    def test_custom_button_icons_are_valid_svg_files(self) -> None:
        expected = {
            "designer.svg",
            "artist.svg",
            "comic.svg",
            "comic-page.svg",
            "screentone.svg",
            "shape-square.svg",
            "shape-circle.svg",
        }
        icons = {path.name for path in (PLUGIN_ROOT / "icons").glob("*.svg")}
        self.assertEqual(icons, expected)
        for name in expected:
            root = ElementTree.parse(PLUGIN_ROOT / "icons" / name).getroot()
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
            self.assertEqual(root.attrib["viewBox"], "0 0 48 48")

    def test_plugin_registers_workspace_page_and_screentone_procedures(self) -> None:
        source = ENTRYPOINT.read_text(encoding="utf-8")
        for procedure in (
            "plug-in-photogimp-workspaces",
            "plug-in-photogimp-comic-page",
            "plug-in-photogimp-screentone",
        ):
            self.assertIn(procedure, source)

    def test_workspace_uses_an_icon_selector_anchored_to_main_window(self) -> None:
        source = ENTRYPOINT.read_text(encoding="utf-8")
        self.assertIn("class WorkspaceModeSwitcher(Gtk.Window)", source)
        self.assertIn("Gtk.ComboBox.new_with_model", source)
        self.assertIn("self.mode_select.set_id_column(2)", source)
        self.assertIn("Gimp.default_display()", source)
        self.assertIn("display.get_window_handle()", source)
        self.assertIn("mode_switcher_position(", source)
        self.assertNotIn("header.pack_end(mode_control", source)
        self.assertNotIn("header.pack_end(mode_control", source)

    def test_switcher_starts_with_gimp_and_stays_visible(self) -> None:
        source = ENTRYPOINT.read_text(encoding="utf-8")
        self.assertIn('EXTENSION_PROCEDURE = "extension-photogimp-workspaces"', source)
        self.assertIn("Gimp.PDBProcType.PERSISTENT", source)
        self.assertIn("procedure.persistent_ready()", source)
        self.assertIn("plug_in.persistent_enable()", source)
        self.assertIn("plug_in.add_temp_procedure(next_mode_procedure)", source)
        self.assertIn("_win32_set_owner(", source)
        self.assertNotIn("GetForegroundWindow", source)

    def test_mode_change_uses_the_left_toolbox_without_a_palette(self) -> None:
        source = ENTRYPOINT.read_text(encoding="utf-8")
        self.assertNotIn("ToolPalette", source)
        self.assertNotIn('Gtk.Button(label="Ferramentas")', source)
        self.assertIn("_win32_send_shortcut(self.gimp_window, shortcut)", source)
        self.assertIn('SCRIPT_DIR / "apply_toolbox.py"', source)
        self.assertIn('lookup_procedure("gimp-quit")', source)
        self.assertIn("_Reiniciar o GIMP agora", source)

    def test_shape_buttons_draw_the_selection_on_a_new_layer(self) -> None:
        source = ENTRYPOINT.read_text(encoding="utf-8")
        self.assertIn("def draw_selection_shape(", source)
        self.assertIn("layer.edit_fill(Gimp.FillType.FOREGROUND)", source)
        self.assertIn("layer.edit_stroke_selection()", source)
        self.assertIn("image.insert_layer(layer, None, -1)", source)
        self.assertIn("self._host.arm_shape(kind)", source)


if __name__ == "__main__":
    unittest.main()
