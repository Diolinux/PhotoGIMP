"""Pure data and geometry helpers for the PhotoGIMP workspace plug-in."""

from __future__ import annotations

from math import isfinite
import re


MODE_DEFINITIONS = {
    "designer": {
        "label": "Designer gráfico",
        "icon": "designer.svg",
        "tools": (
            ("Mover", "V", "gimp-tool-move", "tools-move"),
            ("Seleção retangular", "M", "gimp-tool-rect-select", "tools-rect-select"),
            ("Caminhos", "P", "gimp-tool-path", "tools-path"),
            ("Texto", "T", "gimp-tool-text", "tools-text"),
            ("Gradiente", "G", "gimp-tool-gradient", "tools-gradient"),
            ("Formas geométricas", "U", "gimp-tool-ellipse-select", "plug-in-gfig"),
            ("Transformação", "Ctrl+T", "gimp-tool-unified-transform", "tools-unified-transform"),
            ("Curvas", "Ctrl+M", "gimp-tool-curves", "tools-curves"),
        ),
    },
    "artist": {
        "label": "Artista digital",
        "icon": "artist.svg",
        "tools": (
            ("Pincel", "B", "gimp-tool-paintbrush", "tools-paintbrush"),
            ("MyPaint", "Y", "gimp-tool-mypaint-brush", "tools-mypaint-brush"),
            ("Lápis", "Shift+B", "gimp-tool-pencil", "tools-pencil"),
            ("Borracha", "E", "gimp-tool-eraser", "tools-eraser"),
            ("Conta-gotas", "I", "gimp-tool-color-picker", "tools-color-picker"),
            ("Borrar", "Shift+Alt+O", "gimp-tool-smudge", "tools-smudge"),
            ("Subexpor / superexpor", "O", "gimp-tool-dodge", "tools-dodge-burn"),
            ("Zoom", "Z", "gimp-tool-zoom", "tools-zoom"),
        ),
    },
    "comic": {
        "label": "Quadrinista",
        "icon": "comic.svg",
        "tools": (
            ("Tinta", "K", "gimp-tool-ink", "tools-ink"),
            ("Pincel", "B", "gimp-tool-paintbrush", "tools-paintbrush"),
            ("Borracha", "E", "gimp-tool-eraser", "tools-eraser"),
            ("Preenchimento", "Shift+G", "gimp-tool-bucket-fill", "tools-bucket-fill"),
            ("Caminhos", "P", "gimp-tool-path", "tools-path"),
            ("Texto", "T", "gimp-tool-text", "tools-text"),
            ("Formas geométricas", "U", "gimp-tool-ellipse-select", "plug-in-gfig"),
            ("Zoom", "Z", "gimp-tool-zoom", "tools-zoom"),
        ),
    },
}

DEFAULT_MODE = "designer"
SHORTCUT_MODIFIERS = ("Ctrl", "Shift", "Alt")


# Tools kept visible in the left toolbox for each mode (toolrc ids). Hidden
# tools stay reachable through the Tools menu and their keyboard shortcuts.
TOOLBOX_COMMON = frozenset(
    {
        "gimp-move-tool",
        "gimp-rect-select-tool",
        "gimp-ellipse-select-tool",
        "gimp-free-select-tool",
        "gimp-crop-tool",
        "gimp-color-picker-tool",
        "gimp-zoom-tool",
    }
)

TOOLBOX_TOOLS = {
    "designer": TOOLBOX_COMMON
    | {
        "gimp-align-tool",
        "gimp-fuzzy-select-tool",
        "gimp-by-color-select-tool",
        "gimp-unified-transform-tool",
        "gimp-rotate-tool",
        "gimp-scale-tool",
        "gimp-flip-tool",
        "gimp-perspective-tool",
        "gimp-bucket-fill-tool",
        "gimp-gradient-tool",
        "gimp-paintbrush-tool",
        "gimp-eraser-tool",
        "gimp-path-tool",
        "gimp-text-tool",
        "gimp-measure-tool",
        "gimp-brightness-contrast-tool",
        "gimp-levels-tool",
        "gimp-curves-tool",
        "gimp-threshold-tool",
    },
    "artist": TOOLBOX_COMMON
    | {
        "gimp-unified-transform-tool",
        "gimp-rotate-tool",
        "gimp-flip-tool",
        "gimp-warp-tool",
        "gimp-bucket-fill-tool",
        "gimp-gradient-tool",
        "gimp-paintbrush-tool",
        "gimp-pencil-tool",
        "gimp-airbrush-tool",
        "gimp-ink-tool",
        "gimp-mypaint-brush-tool",
        "gimp-eraser-tool",
        "gimp-clone-tool",
        "gimp-heal-tool",
        "gimp-smudge-tool",
        "gimp-convolve-tool",
        "gimp-dodge-burn-tool",
    },
    "comic": TOOLBOX_COMMON
    | {
        "gimp-fuzzy-select-tool",
        "gimp-unified-transform-tool",
        "gimp-rotate-tool",
        "gimp-flip-tool",
        "gimp-perspective-tool",
        "gimp-bucket-fill-tool",
        "gimp-paintbrush-tool",
        "gimp-pencil-tool",
        "gimp-ink-tool",
        "gimp-eraser-tool",
        "gimp-path-tool",
        "gimp-text-tool",
        "gimp-levels-tool",
        "gimp-threshold-tool",
    },
}


PAPER_PRESETS = {
    "a4": {"label": "A4 — 210 × 297 mm", "millimeters": (210.0, 297.0)},
    "a5": {"label": "A5 — 148 × 210 mm", "millimeters": (148.0, 210.0)},
    "b5": {"label": "B5 mangá — 176 × 250 mm", "millimeters": (176.0, 250.0)},
    "us_comic": {
        "label": "Comic americano — 6,625 × 10,25 pol",
        "millimeters": (168.275, 260.35),
    },
    "webtoon": {"label": "Webtoon — 1600 × 4800 px", "pixels": (1600, 4800)},
}


PANEL_LAYOUTS = {
    "full": {
        "label": "Página inteira",
        "grid": (1, 1),
        "cells": ((0, 0, 1, 1),),
    },
    "two_rows": {
        "label": "2 tiras horizontais",
        "grid": (1, 2),
        "cells": ((0, 0, 1, 1), (0, 1, 1, 1)),
    },
    "two_columns": {
        "label": "2 colunas verticais",
        "grid": (2, 1),
        "cells": ((0, 0, 1, 1), (1, 0, 1, 1)),
    },
    "three_rows": {
        "label": "3 tiras horizontais",
        "grid": (1, 3),
        "cells": ((0, 0, 1, 1), (0, 1, 1, 1), (0, 2, 1, 1)),
    },
    "four_grid": {
        "label": "4 quadros em grade",
        "grid": (2, 2),
        "cells": (
            (0, 0, 1, 1),
            (1, 0, 1, 1),
            (0, 1, 1, 1),
            (1, 1, 1, 1),
        ),
    },
    "manga_five": {
        "label": "Mangá com 5 quadros",
        "grid": (2, 3),
        "cells": (
            (0, 0, 2, 1),
            (0, 1, 1, 1),
            (1, 1, 1, 1),
            (0, 2, 1, 1),
            (1, 2, 1, 1),
        ),
    },
    "dynamic_four": {
        "label": "4 quadros dinâmicos",
        "grid": (3, 2),
        "cells": (
            (0, 0, 2, 1),
            (2, 0, 1, 1),
            (0, 1, 1, 1),
            (1, 1, 2, 1),
        ),
    },
    "six_grid": {
        "label": "6 quadros em grade",
        "grid": (2, 3),
        "cells": (
            (0, 0, 1, 1),
            (1, 0, 1, 1),
            (0, 1, 1, 1),
            (1, 1, 1, 1),
            (0, 2, 1, 1),
            (1, 2, 1, 1),
        ),
    },
}


TONE_STYLES = {
    "dots": "Pontos",
    "lines": "Linhas",
    "crosshatch": "Cruzada",
}


def normalize_mode(value: object) -> str:
    """Return a known mode id, falling back to the default mode."""
    if isinstance(value, str) and value.strip() in MODE_DEFINITIONS:
        return value.strip()
    return DEFAULT_MODE


SHAPES = {
    "rectangle": {
        "label": "Retângulo",
        "icon": "shape-square.svg",
        "select_shortcut": "M",
        "tooltip": "Desenhar retângulo: clique e arraste no canvas "
        "(segure Shift para um quadrado)",
    },
    "ellipse": {
        "label": "Elipse",
        "icon": "shape-circle.svg",
        "select_shortcut": "Shift+M",
        "tooltip": "Desenhar elipse: clique e arraste no canvas "
        "(segure Shift para um círculo)",
    },
}

# Shape styles: stroke width in pixels, where 0 means a filled shape.
SHAPE_STYLES = (
    (0, "Preenchida"),
    (3, "Contorno fino"),
    (8, "Contorno médio"),
    (16, "Contorno grosso"),
)


def image_id_from_title(title: str) -> int | None:
    """Read the image ID from GIMP's default window title ("name-ID.view (...)")."""
    match = re.search(r"-(\d+)\.\d+ \(", title or "")
    return int(match.group(1)) if match else None


def shape_ready(
    current: tuple[int, int, int, int] | None,
    stable_polls: int,
    button_down: bool,
    required_polls: int,
) -> bool:
    """A drawn selection is finished once it exists, stops changing, and the
    mouse button is released."""
    return current is not None and not button_down and stable_polls >= required_polls


def next_mode(mode_id: str) -> str:
    """Return the mode after mode_id, wrapping around."""
    modes = list(MODE_DEFINITIONS)
    return modes[(modes.index(normalize_mode(mode_id)) + 1) % len(modes)]


def primary_tool(mode_id: str) -> tuple[str, str, str, str]:
    """The tool activated right away when switching to a mode."""
    return MODE_DEFINITIONS[normalize_mode(mode_id)]["tools"][0]


def _sexp_nodes(text: str) -> list:
    """Parse toolrc into nested nodes that remember their source spans.

    A list node is ("list", start, end, children); an atom is
    ("atom", start, end, value). Comments and whitespace are skipped.
    """
    stack: list[list] = [[]]
    starts: list[int] = []
    index = 0
    length = len(text)
    while index < length:
        char = text[index]
        if char.isspace():
            index += 1
        elif char == "#":
            while index < length and text[index] != "\n":
                index += 1
        elif char == "(":
            starts.append(index)
            stack.append([])
            index += 1
        elif char == ")":
            if not starts:
                raise ValueError("Unexpected ')' in toolrc")
            children = stack.pop()
            stack[-1].append(("list", starts.pop(), index + 1, children))
            index += 1
        elif char == '"':
            end = index + 1
            while end < length and text[end] != '"':
                end += 2 if text[end] == "\\" else 1
            if end >= length:
                raise ValueError("Unterminated string in toolrc")
            stack[-1].append(("atom", index, end + 1, text[index + 1 : end]))
            index = end + 1
        else:
            end = index
            while end < length and not text[end].isspace() and text[end] not in '()"':
                end += 1
            stack[-1].append(("atom", index, end, text[index:end]))
            index = end
    if starts:
        raise ValueError("Unclosed expression in toolrc")
    return stack[0]


def _head(node) -> str | None:
    if node[0] != "list" or not node[3] or node[3][0][0] != "atom":
        return None
    return node[3][0][3]


def _field(node, name: str):
    for child in node[3][1:]:
        if child[0] == "list" and _head(child) == name:
            return child
    return None


def toolbox_for_mode(toolrc: str, mode_id: str) -> str:
    """Rewrite toolrc so only the tools of mode_id are visible in the toolbox.

    Only the (visible ...) and (active-tool ...) values change, so the file
    keeps GIMP's own formatting, ordering, and any other settings.
    """
    visible_tools = TOOLBOX_TOOLS[normalize_mode(mode_id)]
    edits: list[tuple[int, int, str]] = []

    def set_value(node, name: str, value: str) -> None:
        field = _field(node, name)
        if field is not None and len(field[3]) == 2:
            atom = field[3][1]
            edits.append((atom[1], atom[2], value))

    def tool_id(node) -> str | None:
        return node[3][1][3] if len(node[3]) > 1 and node[3][1][0] == "atom" else None

    for node in _sexp_nodes(toolrc):
        head = _head(node)
        if head == "GimpToolInfo":
            shown = tool_id(node) in visible_tools
            set_value(node, "visible", "yes" if shown else "no")
        elif head == "GimpToolGroup":
            children = _field(node, "children")
            members = [
                child
                for child in (children[3][1:] if children is not None else ())
                if _head(child) == "GimpToolInfo"
            ]
            shown_ids = [tool_id(child) for child in members if tool_id(child) in visible_tools]
            for child in members:
                set_value(child, "visible", "yes" if tool_id(child) in visible_tools else "no")
            set_value(node, "visible", "yes" if shown_ids else "no")
            active = _field(node, "active-tool")
            if shown_ids and active is not None and len(active[3]) == 2:
                if active[3][1][3] not in shown_ids:
                    atom = active[3][1]
                    edits.append((atom[1], atom[2], f'"{shown_ids[0]}"'))

    for start, end, value in sorted(edits, reverse=True):
        toolrc = toolrc[:start] + value + toolrc[end:]
    return toolrc


def parse_shortcut(shortcut: str) -> tuple[tuple[str, ...], str]:
    """Split a display shortcut such as "Shift+Alt+O" into modifiers and key."""
    if not isinstance(shortcut, str):
        raise TypeError("The shortcut must be a string")
    *modifiers, key = shortcut.split("+")
    if len(key) != 1 or not key.isascii() or not key.isalpha():
        raise ValueError(f"Unsupported shortcut key: {shortcut}")
    if any(modifier not in SHORTCUT_MODIFIERS for modifier in modifiers):
        raise ValueError(f"Unsupported shortcut modifier: {shortcut}")
    if len(set(modifiers)) != len(modifiers):
        raise ValueError(f"Repeated shortcut modifier: {shortcut}")
    ordered = tuple(sorted(modifiers, key=SHORTCUT_MODIFIERS.index))
    return ordered, key.upper()


def mode_switcher_position(
    window_bounds: tuple[int, int, int, int],
    switcher_size: tuple[int, int],
    titlebar_height: int,
    margin: int = 8,
) -> tuple[int, int]:
    """Place the mode switcher at the upper-right edge of the main window."""
    left, top, right, bottom = window_bounds
    width, height = switcher_size
    values = (*window_bounds, width, height, titlebar_height, margin)
    if any(not isinstance(value, int) for value in values):
        raise TypeError("Switcher geometry values must be integers")
    if right <= left or bottom <= top or width <= 0 or height <= 0:
        raise ValueError("Window and switcher dimensions must be positive")
    if titlebar_height < 0 or margin < 0:
        raise ValueError("Titlebar height and margin must be non-negative")

    x = max(left, right - width - margin)
    y = min(max(top, top + titlebar_height), max(top, bottom - height))
    return x, y


def mm_to_pixels(value: float, dpi: int) -> int:
    """Convert millimeters to pixels using a positive output resolution."""
    if not isfinite(value) or value < 0:
        raise ValueError("The millimeter value must be finite and non-negative")
    if not isinstance(dpi, int) or not 36 <= dpi <= 1200:
        raise ValueError("DPI must be an integer between 36 and 1200")
    return int(round(value * dpi / 25.4))


def page_size_pixels(preset_id: str, dpi: int, orientation: str) -> tuple[int, int]:
    """Return a preset page size in pixels for portrait or landscape output."""
    if preset_id not in PAPER_PRESETS:
        raise ValueError(f"Unknown paper preset: {preset_id}")
    if orientation not in {"portrait", "landscape"}:
        raise ValueError(f"Unknown orientation: {orientation}")
    if not isinstance(dpi, int) or not 36 <= dpi <= 1200:
        raise ValueError("DPI must be an integer between 36 and 1200")

    preset = PAPER_PRESETS[preset_id]
    if "pixels" in preset:
        width, height = preset["pixels"]
    else:
        width_mm, height_mm = preset["millimeters"]
        width = mm_to_pixels(width_mm, dpi)
        height = mm_to_pixels(height_mm, dpi)

    if orientation == "landscape":
        width, height = height, width
    return int(width), int(height)


def panel_rectangles(
    layout_id: str,
    page_width: int,
    page_height: int,
    margin: int,
    gutter: int,
) -> tuple[tuple[int, int, int, int], ...]:
    """Lay out comic panels inside a page without overlap or edge overflow."""
    if layout_id not in PANEL_LAYOUTS:
        raise ValueError(f"Unknown panel layout: {layout_id}")
    values = (page_width, page_height, margin, gutter)
    if any(not isinstance(value, int) for value in values):
        raise TypeError("Page geometry values must be integers")
    if page_width <= 0 or page_height <= 0 or margin < 0 or gutter < 0:
        raise ValueError("Page dimensions must be positive and spacing non-negative")

    layout = PANEL_LAYOUTS[layout_id]
    columns, rows = layout["grid"]
    inner_width = page_width - (2 * margin)
    inner_height = page_height - (2 * margin)
    available_width = inner_width - (gutter * (columns - 1))
    available_height = inner_height - (gutter * (rows - 1))
    if available_width < columns or available_height < rows:
        raise ValueError("Margins and gutters leave no room for the selected layout")

    cell_width = available_width / columns
    cell_height = available_height / rows
    rectangles = []
    for column, row, column_span, row_span in layout["cells"]:
        left = margin + column * (cell_width + gutter)
        top = margin + row * (cell_height + gutter)
        right = left + column_span * cell_width + (column_span - 1) * gutter
        bottom = top + row_span * cell_height + (row_span - 1) * gutter
        x = int(round(left))
        y = int(round(top))
        width = int(round(right)) - x
        height = int(round(bottom)) - y
        if width <= 0 or height <= 0:
            raise ValueError("A panel collapsed to an invalid size")
        rectangles.append((x, y, width, height))

    return tuple(rectangles)


def validate_tone_settings(
    style: str,
    spacing: int,
    mark_size: float,
    angle: float,
    opacity: float,
) -> tuple[str, int, float, float, float]:
    """Validate and normalize screentone controls used by the UI and renderer."""
    if style not in TONE_STYLES:
        raise ValueError(f"Unknown screentone style: {style}")
    if not isinstance(spacing, int) or not 4 <= spacing <= 80:
        raise ValueError("Spacing must be an integer between 4 and 80 pixels")
    if not isfinite(mark_size) or not 0.5 <= mark_size <= spacing:
        raise ValueError("Mark size must be between 0.5 and the pattern spacing")
    if not isfinite(angle) or not -180.0 <= angle <= 180.0:
        raise ValueError("Angle must be between -180 and 180 degrees")
    if not isfinite(opacity) or not 1.0 <= opacity <= 100.0:
        raise ValueError("Opacity must be between 1 and 100 percent")
    return style, spacing, float(mark_size), float(angle), float(opacity)
