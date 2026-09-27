from __future__ import annotations

import importlib.util
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
