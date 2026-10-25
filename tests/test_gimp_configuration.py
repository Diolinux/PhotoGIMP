from __future__ import annotations

from pathlib import Path
import shlex
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".config" / "GIMP" / "3.0"


def parse_sexpressions(path: Path) -> list[list]:
    lexer = shlex.shlex(path.read_text(encoding="utf-8"), posix=True, punctuation_chars="()")
    lexer.commenters = "#"
    lexer.whitespace_split = True

    expressions: list[list] = []
    stack = [expressions]
    for raw_token in lexer:
        tokens = list(raw_token) if raw_token and set(raw_token) <= {"(", ")"} else [raw_token]
        for token in tokens:
            if token == "(":
                expression: list = []
                stack[-1].append(expression)
                stack.append(expression)
            elif token == ")":
                if len(stack) == 1:
                    raise ValueError(f"Unexpected ')' in {path}")
                stack.pop()
            else:
                stack[-1].append(token)

    if len(stack) != 1:
        raise ValueError(f"Unclosed expression in {path}")
    return expressions


def walk(expressions: list[list]):
    for expression in expressions:
        if not isinstance(expression, list):
            continue
        yield expression
        yield from walk(expression)


def tool_ids(expression: list) -> set[str]:
    return {
        item[1]
        for item in walk([expression])
        if len(item) >= 2 and item[0] == "GimpToolInfo"
    }


class GimpConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.toolrc = parse_sexpressions(CONFIG / "toolrc")
        cls.shortcuts = parse_sexpressions(CONFIG / "shortcutsrc")

    def test_shape_selectors_are_separate_toolbox_buttons(self) -> None:
        top_level_tools = {
            expression[1]
            for expression in self.toolrc
            if len(expression) >= 2 and expression[0] == "GimpToolInfo"
        }
        self.assertIn("gimp-rect-select-tool", top_level_tools)
        self.assertIn("gimp-ellipse-select-tool", top_level_tools)

    def test_adjustment_and_offset_tools_are_exposed(self) -> None:
        groups = [
            expression
            for expression in self.toolrc
            if expression and expression[0] == "GimpToolGroup"
        ]
        adjustments = {
            "gimp-brightness-contrast-tool",
            "gimp-levels-tool",
            "gimp-curves-tool",
            "gimp-threshold-tool",
        }

        self.assertTrue(any(adjustments <= tool_ids(group) for group in groups))
        self.assertTrue(
            any(
                {"gimp-unified-transform-tool", "gimp-offset-tool"} <= tool_ids(group)
                for group in groups
            )
        )

    def test_each_tool_appears_once(self) -> None:
        tools = [
            expression[1]
            for expression in walk(self.toolrc)
            if len(expression) >= 2 and expression[0] == "GimpToolInfo"
        ]
        self.assertEqual(len(tools), len(set(tools)))

    def test_shape_and_adjustment_shortcuts_are_active(self) -> None:
        actions = {
            expression[1]: expression[2] if len(expression) >= 3 else None
            for expression in self.shortcuts
            if len(expression) >= 2 and expression[0] == "action"
        }
        self.assertEqual(actions["plug-in-gfig"], "u")
        self.assertEqual(actions["select-stroke"], "<Primary><Shift>BackSpace")
        self.assertEqual(actions["tools-levels"], "<Primary>l")
        self.assertEqual(actions["tools-curves"], "<Primary>m")

    def test_workspace_and_drawing_shortcuts_are_active(self) -> None:
        actions = {
            expression[1]: expression[2] if len(expression) >= 3 else None
            for expression in self.shortcuts
            if len(expression) >= 2 and expression[0] == "action"
        }
        self.assertEqual(
            actions["plug-in-photogimp-workspaces"], "<Primary><Shift>space"
        )
        self.assertEqual(actions["tools-ink"], "k")
        self.assertEqual(actions["tools-mypaint-brush"], "y")

    def test_shortcuts_do_not_map_to_different_actions(self) -> None:
        bindings: dict[str, str] = {}
        for expression in self.shortcuts:
            if len(expression) < 3 or expression[0] != "action":
                continue
            action, shortcut = expression[1:3]
            previous = bindings.setdefault(shortcut, action)
            self.assertEqual(previous, action, f"{shortcut} is assigned to multiple actions")


if __name__ == "__main__":
    unittest.main()
