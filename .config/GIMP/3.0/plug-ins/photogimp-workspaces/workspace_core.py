"""Pure data and geometry helpers for the PhotoGIMP workspace plug-in."""

from __future__ import annotations

from math import isfinite


MODE_DEFINITIONS = {
    "designer": {
        "label": "Designer gráfico",
        "icon": "designer.svg",
        "tools": (
            ("Mover", "V", "gimp-tool-move"),
            ("Seleção retangular", "M", "gimp-tool-rectangle-select"),
            ("Caminhos", "P", "gimp-tool-path"),
            ("Texto", "T", "gimp-tool-text"),
            ("Gradiente", "G", "gimp-tool-gradient"),
            ("Formas geométricas", "U", "gimp-tool-rectangle-select"),
            ("Transformação", "Ctrl+T", "gimp-tool-unified-transform"),
            ("Curvas", "Ctrl+M", "gimp-tool-curves"),
        ),
    },
    "artist": {
        "label": "Artista digital",
        "icon": "artist.svg",
        "tools": (
            ("Pincel", "B", "gimp-tool-paintbrush"),
            ("MyPaint", "Y", "gimp-tool-mypaint-brush"),
            ("Lápis", "Shift+B", "gimp-tool-pencil"),
            ("Borracha", "E", "gimp-tool-eraser"),
            ("Conta-gotas", "I", "gimp-tool-color-picker"),
            ("Borrar", "Shift+Alt+O", "gimp-tool-smudge"),
            ("Subexpor / superexpor", "O", "gimp-tool-dodge"),
            ("Zoom", "Z", "gimp-tool-zoom"),
        ),
    },
    "comic": {
        "label": "Quadrinista",
        "icon": "comic.svg",
        "tools": (
            ("Tinta", "K", "gimp-tool-ink"),
            ("Pincel", "B", "gimp-tool-paintbrush"),
            ("Borracha", "E", "gimp-tool-eraser"),
            ("Preenchimento", "Shift+G", "gimp-tool-bucket-fill"),
            ("Caminhos", "P", "gimp-tool-path"),
            ("Texto", "T", "gimp-tool-text"),
            ("Formas geométricas", "U", "gimp-tool-rectangle-select"),
            ("Zoom", "Z", "gimp-tool-zoom"),
        ),
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
