#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PhotoGIMP work modes, comic page layouts, and screentone generator."""

from __future__ import annotations

import ctypes
from math import ceil, hypot, pi
from pathlib import Path
import sys

import gi

gi.require_version("Gimp", "3.0")
gi.require_version("GimpUi", "3.0")
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
gi.require_foreign("cairo")

import cairo
from gi.repository import Gdk, GdkPixbuf, Gio, Gimp, GimpUi, GLib, Gtk


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from workspace_core import (  # noqa: E402
    MODE_DEFINITIONS,
    PANEL_LAYOUTS,
    PAPER_PRESETS,
    TONE_STYLES,
    mm_to_pixels,
    mode_switcher_position,
    page_size_pixels,
    panel_rectangles,
    validate_tone_settings,
)


PLUGIN_BINARY = "photogimp-workspaces"
WORKSPACE_PROCEDURE = "plug-in-photogimp-workspaces"
PAGE_PROCEDURE = "plug-in-photogimp-comic-page"
TONE_PROCEDURE = "plug-in-photogimp-screentone"
ICON_DIR = SCRIPT_DIR / "icons"

CSS = b"""
.photogimp-root { padding: 8px; }
.photogimp-global-switcher {
  background-color: @theme_bg_color;
  border: 1px solid alpha(@theme_fg_color, 0.18);
  padding: 2px 5px;
}
.photogimp-mode-caption { font-weight: 600; margin-right: 4px; }
.photogimp-mode-select { min-width: 205px; }
.photogimp-tool { min-width: 210px; min-height: 42px; padding: 6px 9px; }
.photogimp-tool-name { font-weight: 600; }
.photogimp-shortcut { color: #66727d; font-size: 0.88em; }
.photogimp-section { font-weight: 700; margin-top: 6px; }
.photogimp-action { min-height: 44px; padding: 7px 12px; }
"""


def _load_css() -> None:
    provider = Gtk.CssProvider()
    provider.load_from_data(CSS)
    screen = Gdk.Screen.get_default()
    if screen is not None:
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )


def _native_handle_value(handle: GLib.Bytes | None) -> int | None:
    if handle is None:
        return None
    data = bytes(handle.get_data())
    pointer_size = ctypes.sizeof(ctypes.c_void_p)
    if len(data) < pointer_size:
        return None
    value = int.from_bytes(data[:pointer_size], byteorder=sys.byteorder)
    return value or None


def _gimp_window_handle() -> int | None:
    if sys.platform != "win32":
        return None

    display = Gimp.default_display()
    if display is not None and display.is_valid():
        value = _native_handle_value(display.get_window_handle())
        if value is not None:
            return value

    from ctypes import wintypes

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.GetForegroundWindow.restype = wintypes.HWND
    foreground = user32.GetForegroundWindow()
    return int(foreground) if foreground else None


def _win32_window_geometry(
    handle: int,
) -> tuple[tuple[int, int, int, int], bool, int] | None:
    if sys.platform != "win32":
        return None

    from ctypes import wintypes

    hwnd = wintypes.HWND(handle)
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.IsWindow.argtypes = [wintypes.HWND]
    user32.IsWindow.restype = wintypes.BOOL
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.IsWindowVisible.restype = wintypes.BOOL
    user32.IsIconic.argtypes = [wintypes.HWND]
    user32.IsIconic.restype = wintypes.BOOL
    user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    user32.GetWindowRect.restype = wintypes.BOOL
    user32.GetSystemMetrics.argtypes = [ctypes.c_int]
    user32.GetSystemMetrics.restype = ctypes.c_int
    if not user32.IsWindow(hwnd):
        return None

    visible = bool(user32.IsWindowVisible(hwnd)) and not bool(user32.IsIconic(hwnd))
    rect = wintypes.RECT()
    has_rect = False
    try:
        dwmapi = ctypes.WinDLL("dwmapi")
        dwmapi.DwmGetWindowAttribute.argtypes = [
            wintypes.HWND,
            wintypes.DWORD,
            ctypes.c_void_p,
            wintypes.DWORD,
        ]
        dwmapi.DwmGetWindowAttribute.restype = ctypes.c_long
        has_rect = (
            dwmapi.DwmGetWindowAttribute(
                hwnd, 9, ctypes.byref(rect), ctypes.sizeof(rect)
            )
            == 0
        )
    except OSError:
        has_rect = False
    if not has_rect and not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        return None

    bounds = (rect.left, rect.top, rect.right, rect.bottom)
    titlebar_height = max(
        24,
        user32.GetSystemMetrics(4) + user32.GetSystemMetrics(33),
    )
    return bounds, visible, titlebar_height


def _monitor_workarea() -> tuple[int, int, int, int] | None:
    display = Gdk.Display.get_default()
    if display is None or display.get_n_monitors() == 0:
        return None
    monitor = display.get_primary_monitor() or display.get_monitor(0)
    area = monitor.get_workarea()
    return area.x, area.y, area.x + area.width, area.y + area.height


def _svg_pixbuf(filename: str, size: int) -> GdkPixbuf.Pixbuf | None:
    path = ICON_DIR / filename
    try:
        return GdkPixbuf.Pixbuf.new_from_file_at_scale(
            str(path), size, size, True
        )
    except GLib.Error:
        return None


def _svg_image(filename: str, size: int) -> Gtk.Image:
    pixbuf = _svg_pixbuf(filename, size)
    if pixbuf is None:
        return Gtk.Image.new_from_icon_name(
            "image-missing", Gtk.IconSize.LARGE_TOOLBAR
        )
    return Gtk.Image.new_from_pixbuf(pixbuf)


def _icon_button(label: str, icon: str, tooltip: str) -> Gtk.Button:
    button = Gtk.Button()
    button.get_style_context().add_class("photogimp-action")
    button.set_tooltip_text(tooltip)
    content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=9)
    content.pack_start(_svg_image(icon, 28), False, False, 0)
    content.pack_start(Gtk.Label(label=label), False, False, 0)
    button.add(content)
    return button


def _show_error(parent: Gtk.Window | None, title: str, error: Exception) -> None:
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        modal=True,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.CLOSE,
        text=title,
    )
    dialog.format_secondary_text(str(error))
    dialog.run()
    dialog.destroy()


def _paint_tone(
    context: cairo.Context,
    width: int,
    height: int,
    style: str,
    spacing: int,
    mark_size: float,
    angle: float,
    alpha: float = 1.0,
) -> None:
    tile = cairo.ImageSurface(cairo.FORMAT_ARGB32, spacing, spacing)
    tile_context = cairo.Context(tile)
    tile_context.set_operator(cairo.OPERATOR_CLEAR)
    tile_context.paint()
    tile_context.set_operator(cairo.OPERATOR_OVER)
    tile_context.set_source_rgba(0.055, 0.065, 0.075, alpha)
    tile_context.set_antialias(cairo.ANTIALIAS_BEST)

    center = spacing / 2.0
    if style == "dots":
        tile_context.arc(center, center, mark_size / 2.0, 0, 2 * pi)
        tile_context.fill()
    else:
        tile_context.set_line_width(mark_size)
        tile_context.move_to(0, center)
        tile_context.line_to(spacing, center)
        if style == "crosshatch":
            tile_context.move_to(center, 0)
            tile_context.line_to(center, spacing)
        tile_context.stroke()

    tile.flush()
    pattern = cairo.SurfacePattern(tile)
    pattern.set_extend(cairo.EXTEND_REPEAT)
    extent = int(ceil(hypot(width, height))) + (2 * spacing)

    context.save()
    context.translate(width / 2.0, height / 2.0)
    context.rotate(angle * pi / 180.0)
    context.rectangle(-extent / 2.0, -extent / 2.0, extent, extent)
    context.set_source(pattern)
    context.fill()
    context.restore()


def _surface_layer(
    image: Gimp.Image,
    name: str,
    surface: cairo.ImageSurface,
) -> Gimp.Layer:
    surface.flush()
    layer = Gimp.Layer.new_from_surface(image, name, surface, 0.0, 0.0)
    if layer is None or not image.insert_layer(layer, None, 0):
        raise RuntimeError(f"Não foi possível criar a camada ‘{name}’.")
    return layer


def _blank_layer(image: Gimp.Image, name: str) -> Gimp.Layer:
    layer = Gimp.Layer.new(
        image,
        name,
        image.get_width(),
        image.get_height(),
        Gimp.ImageType.RGBA_IMAGE,
        100.0,
        Gimp.LayerMode.NORMAL,
    )
    if layer is None or not layer.fill(Gimp.FillType.TRANSPARENT):
        raise RuntimeError(f"Não foi possível preparar a camada ‘{name}’.")
    if not image.insert_layer(layer, None, 0):
        raise RuntimeError(f"Não foi possível inserir a camada ‘{name}’.")
    return layer


def create_comic_page(settings: dict) -> Gimp.Image:
    width, height = page_size_pixels(
        settings["preset"], settings["dpi"], settings["orientation"]
    )
    margin = mm_to_pixels(settings["margin_mm"], settings["dpi"])
    gutter = mm_to_pixels(settings["gutter_mm"], settings["dpi"])
    panels = panel_rectangles(
        settings["layout"], width, height, margin, gutter
    )

    image = Gimp.Image.new(width, height, Gimp.ImageBaseType.RGB)
    if image is None:
        raise RuntimeError("O GIMP não conseguiu criar a nova imagem.")

    image.undo_disable()
    try:
        image.set_resolution(float(settings["dpi"]), float(settings["dpi"]))

        paper = Gimp.Layer.new(
            image,
            "Papel",
            width,
            height,
            Gimp.ImageType.RGB_IMAGE,
            100.0,
            Gimp.LayerMode.NORMAL,
        )
        if paper is None or not paper.fill(Gimp.FillType.WHITE):
            raise RuntimeError("Não foi possível criar o papel da página.")
        if not image.insert_layer(paper, None, 0):
            raise RuntimeError("Não foi possível inserir o papel da página.")

        panel_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        panel_context = cairo.Context(panel_surface)
        panel_context.set_operator(cairo.OPERATOR_CLEAR)
        panel_context.paint()
        panel_context.set_operator(cairo.OPERATOR_OVER)
        panel_context.set_source_rgb(0.04, 0.045, 0.05)
        panel_context.set_line_width(float(settings["border_width"]))
        half_stroke = settings["border_width"] / 2.0
        for x, y, panel_width, panel_height in panels:
            panel_context.rectangle(
                x + half_stroke,
                y + half_stroke,
                panel_width - settings["border_width"],
                panel_height - settings["border_width"],
            )
        panel_context.stroke()
        _surface_layer(image, "Quadros", panel_surface)

        _blank_layer(image, "Retículas")
        sketch = _blank_layer(image, "Esboço")
        ink = _blank_layer(image, "Tinta")
        _blank_layer(image, "Balões")
        _blank_layer(image, "Texto")
        sketch.set_opacity(45.0)

        image.add_vguide(margin)
        image.add_vguide(width - margin)
        image.add_hguide(margin)
        image.add_hguide(height - margin)
        image.set_selected_layers([ink])
    except Exception:
        image.undo_enable()
        image.delete()
        raise

    image.undo_enable()
    display = Gimp.Display.new(image)
    if display is None:
        image.delete()
        raise RuntimeError("A página foi criada, mas o GIMP não pôde exibi-la.")
    Gimp.displays_flush()
    return image


def apply_screentone(image: Gimp.Image, settings: dict) -> Gimp.Layer:
    style, spacing, mark_size, angle, opacity = validate_tone_settings(
        settings["style"],
        settings["spacing"],
        settings["mark_size"],
        settings["angle"],
        settings["opacity"],
    )
    width = image.get_width()
    height = image.get_height()
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)
    context.set_operator(cairo.OPERATOR_CLEAR)
    context.paint()
    context.set_operator(cairo.OPERATOR_OVER)
    _paint_tone(context, width, height, style, spacing, mark_size, angle)

    layer = None
    image.undo_group_start()
    try:
        label = TONE_STYLES[style]
        layer = _surface_layer(
            image,
            f"Retícula — {label} {spacing}px {angle:g}°",
            surface,
        )
        layer.set_mode(Gimp.LayerMode.MULTIPLY)
        layer.set_opacity(opacity)
        if not Gimp.Selection.is_empty(image):
            mask = layer.create_mask(Gimp.AddMaskType.SELECTION)
            if mask is not None:
                layer.add_mask(mask)
        image.set_selected_layers([layer])
    except Exception:
        if layer is not None and layer.is_valid():
            image.remove_layer(layer)
        raise
    finally:
        image.undo_group_end()

    Gimp.displays_flush()
    return layer


class PageDialog(Gtk.Dialog):
    __gtype_name__ = "PhotoGimpComicPageDialog"

    def __init__(self, parent: Gtk.Window | None):
        super().__init__(title="Nova página de quadrinhos")
        if parent is not None:
            self.set_transient_for(parent)
        else:
            GimpUi.window_set_transient(self)
        self.set_modal(True)
        self.set_default_size(650, 460)
        self.add_button("_Cancelar", Gtk.ResponseType.CANCEL)
        self.add_button("_Criar página", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        body = self.get_content_area()
        body.set_border_width(14)
        body.set_spacing(12)
        columns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        body.pack_start(columns, True, True, 0)

        controls = Gtk.Grid(column_spacing=10, row_spacing=10)
        controls.set_valign(Gtk.Align.START)
        columns.pack_start(controls, True, True, 0)

        self.preset = Gtk.ComboBoxText()
        for preset_id, preset in PAPER_PRESETS.items():
            self.preset.append(preset_id, preset["label"])
        self.preset.set_active_id("b5")

        self.orientation = Gtk.ComboBoxText()
        self.orientation.append("portrait", "Vertical")
        self.orientation.append("landscape", "Horizontal")
        self.orientation.set_active_id("portrait")

        self.layout = Gtk.ComboBoxText()
        for layout_id, layout in PANEL_LAYOUTS.items():
            self.layout.append(layout_id, layout["label"])
        self.layout.set_active_id("four_grid")

        self.dpi = Gtk.SpinButton.new_with_range(72, 600, 1)
        self.dpi.set_value(300)
        self.margin = Gtk.SpinButton.new_with_range(3, 40, 0.5)
        self.margin.set_value(12)
        self.margin.set_digits(1)
        self.gutter = Gtk.SpinButton.new_with_range(1, 20, 0.5)
        self.gutter.set_value(5)
        self.gutter.set_digits(1)
        self.border = Gtk.SpinButton.new_with_range(1, 20, 1)
        self.border.set_value(4)

        rows = (
            ("Formato", self.preset),
            ("Orientação", self.orientation),
            ("Quadros", self.layout),
            ("Resolução (dpi)", self.dpi),
            ("Margem (mm)", self.margin),
            ("Espaço (mm)", self.gutter),
            ("Contorno (px)", self.border),
        )
        for row, (label_text, widget) in enumerate(rows):
            label = Gtk.Label(label=label_text, xalign=0)
            controls.attach(label, 0, row, 1, 1)
            controls.attach(widget, 1, row, 1, 1)

        preview_frame = Gtk.Frame()
        preview_frame.set_shadow_type(Gtk.ShadowType.IN)
        columns.pack_start(preview_frame, False, False, 0)
        self.preview = Gtk.DrawingArea()
        self.preview.set_size_request(250, 340)
        self.preview.connect("draw", self._draw_preview)
        preview_frame.add(self.preview)

        for combo in (self.preset, self.orientation, self.layout):
            combo.connect("changed", self._queue_preview)
        for spin in (self.dpi, self.margin, self.gutter, self.border):
            spin.connect("value-changed", self._queue_preview)
        self.show_all()

    def _queue_preview(self, _widget) -> None:
        self.preview.queue_draw()

    def settings(self) -> dict:
        return {
            "preset": self.preset.get_active_id(),
            "orientation": self.orientation.get_active_id(),
            "layout": self.layout.get_active_id(),
            "dpi": self.dpi.get_value_as_int(),
            "margin_mm": self.margin.get_value(),
            "gutter_mm": self.gutter.get_value(),
            "border_width": self.border.get_value_as_int(),
        }

    def _draw_preview(self, widget: Gtk.DrawingArea, context: cairo.Context) -> bool:
        allocation = widget.get_allocation()
        context.set_source_rgb(0.12, 0.14, 0.16)
        context.paint()
        try:
            settings = self.settings()
            page_width, page_height = page_size_pixels(
                settings["preset"], settings["dpi"], settings["orientation"]
            )
            margin = mm_to_pixels(settings["margin_mm"], settings["dpi"])
            gutter = mm_to_pixels(settings["gutter_mm"], settings["dpi"])
            rectangles = panel_rectangles(
                settings["layout"], page_width, page_height, margin, gutter
            )
        except (TypeError, ValueError):
            return False

        padding = 14.0
        scale = min(
            (allocation.width - 2 * padding) / page_width,
            (allocation.height - 2 * padding) / page_height,
        )
        offset_x = (allocation.width - page_width * scale) / 2.0
        offset_y = (allocation.height - page_height * scale) / 2.0
        context.set_source_rgb(0.98, 0.98, 0.97)
        context.rectangle(
            offset_x, offset_y, page_width * scale, page_height * scale
        )
        context.fill()
        context.set_source_rgb(0.07, 0.08, 0.09)
        context.set_line_width(2.0)
        for x, y, width, height in rectangles:
            context.rectangle(
                offset_x + x * scale,
                offset_y + y * scale,
                width * scale,
                height * scale,
            )
        context.stroke()
        return False


class ToneDialog(Gtk.Dialog):
    __gtype_name__ = "PhotoGimpScreentoneDialog"

    def __init__(self, parent: Gtk.Window | None):
        super().__init__(title="Criar retícula")
        if parent is not None:
            self.set_transient_for(parent)
        else:
            GimpUi.window_set_transient(self)
        self.set_modal(True)
        self.set_default_size(570, 360)
        self.add_button("_Cancelar", Gtk.ResponseType.CANCEL)
        self.add_button("_Criar retícula", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        body = self.get_content_area()
        body.set_border_width(14)
        body.set_spacing(12)
        columns = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        body.pack_start(columns, True, True, 0)

        controls = Gtk.Grid(column_spacing=10, row_spacing=10)
        controls.set_valign(Gtk.Align.START)
        columns.pack_start(controls, True, True, 0)
        self.style = Gtk.ComboBoxText()
        for style_id, label in TONE_STYLES.items():
            self.style.append(style_id, label)
        self.style.set_active_id("dots")
        self.spacing = Gtk.SpinButton.new_with_range(4, 80, 1)
        self.spacing.set_value(12)
        self.mark_size = Gtk.SpinButton.new_with_range(0.5, 12, 0.5)
        self.mark_size.set_digits(1)
        self.mark_size.set_value(4)
        self.angle = Gtk.SpinButton.new_with_range(-180, 180, 1)
        self.angle.set_value(45)
        self.opacity = Gtk.SpinButton.new_with_range(1, 100, 1)
        self.opacity.set_value(35)

        rows = (
            ("Tipo", self.style),
            ("Espaçamento (px)", self.spacing),
            ("Tamanho (px)", self.mark_size),
            ("Ângulo (°)", self.angle),
            ("Opacidade (%)", self.opacity),
        )
        for row, (label_text, widget) in enumerate(rows):
            controls.attach(Gtk.Label(label=label_text, xalign=0), 0, row, 1, 1)
            controls.attach(widget, 1, row, 1, 1)

        preview_frame = Gtk.Frame()
        preview_frame.set_shadow_type(Gtk.ShadowType.IN)
        columns.pack_start(preview_frame, True, True, 0)
        self.preview = Gtk.DrawingArea()
        self.preview.set_size_request(280, 220)
        self.preview.connect("draw", self._draw_preview)
        preview_frame.add(self.preview)

        self.style.connect("changed", self._queue_preview)
        self.spacing.connect("value-changed", self._spacing_changed)
        for spin in (self.mark_size, self.angle, self.opacity):
            spin.connect("value-changed", self._queue_preview)
        self.show_all()

    def _spacing_changed(self, _widget) -> None:
        maximum = float(self.spacing.get_value_as_int())
        self.mark_size.get_adjustment().set_upper(maximum)
        if self.mark_size.get_value() > maximum:
            self.mark_size.set_value(maximum)
        self.preview.queue_draw()

    def _queue_preview(self, _widget) -> None:
        self.preview.queue_draw()

    def settings(self) -> dict:
        values = validate_tone_settings(
            self.style.get_active_id(),
            self.spacing.get_value_as_int(),
            self.mark_size.get_value(),
            self.angle.get_value(),
            self.opacity.get_value(),
        )
        style, spacing, mark_size, angle, opacity = values
        return {
            "style": style,
            "spacing": spacing,
            "mark_size": mark_size,
            "angle": angle,
            "opacity": opacity,
        }

    def _draw_preview(self, widget: Gtk.DrawingArea, context: cairo.Context) -> bool:
        allocation = widget.get_allocation()
        context.set_source_rgb(0.98, 0.98, 0.97)
        context.paint()
        try:
            settings = self.settings()
        except ValueError:
            return False
        _paint_tone(
            context,
            allocation.width,
            allocation.height,
            settings["style"],
            settings["spacing"],
            settings["mark_size"],
            settings["angle"],
            settings["opacity"] / 100.0,
        )
        return False


class WorkspaceModeSwitcher(Gtk.Window):
    __gtype_name__ = "PhotoGimpWorkspaceModeSwitcher"

    WIDTH = 286
    HEIGHT = 34

    def __init__(self, on_mode_changed):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_title("Modo de visualização do PhotoGIMP")
        self.set_role("photogimp-global-mode-switcher")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_focus_on_map(False)
        self.set_type_hint(Gdk.WindowTypeHint.TOOLBAR)
        self.set_default_size(self.WIDTH, self.HEIGHT)
        self.set_size_request(self.WIDTH, self.HEIGHT)
        self._on_mode_changed = on_mode_changed
        self._parent_handle = _gimp_window_handle()
        self._anchor_source = None

        display = Gimp.default_display()
        if display is not None and display.is_valid():
            GimpUi.window_set_transient_for_display(self, display)
        else:
            GimpUi.window_set_transient(self)

        shell = Gtk.EventBox()
        shell.get_style_context().add_class("photogimp-global-switcher")
        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        shell.add(content)
        caption = Gtk.Label(label="Modo", xalign=1)
        caption.get_style_context().add_class("photogimp-mode-caption")
        content.pack_start(caption, False, False, 0)

        self.mode_model = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        for mode_id, mode in MODE_DEFINITIONS.items():
            self.mode_model.append(
                [_svg_pixbuf(mode["icon"], 20), mode["label"], mode_id]
            )
        self.mode_select = Gtk.ComboBox.new_with_model(self.mode_model)
        self.mode_select.get_style_context().add_class("photogimp-mode-select")
        self.mode_select.set_id_column(2)
        icon_renderer = Gtk.CellRendererPixbuf()
        text_renderer = Gtk.CellRendererText()
        self.mode_select.pack_start(icon_renderer, False)
        self.mode_select.add_attribute(icon_renderer, "pixbuf", 0)
        self.mode_select.pack_start(text_renderer, True)
        self.mode_select.add_attribute(text_renderer, "text", 1)
        self.mode_select.set_tooltip_text("Mudar modo de visualização")
        self.mode_select.connect("changed", self._mode_changed)
        caption.set_mnemonic_widget(self.mode_select)
        content.pack_start(self.mode_select, True, True, 0)
        self.add(shell)

        self.connect("size-allocate", self._size_allocated)
        self.connect("destroy", self._destroyed)
        self.mode_select.set_active_id("designer")

    def show_anchored(self) -> None:
        self._move_to_anchor()
        self.show_all()
        self._anchor_source = GLib.timeout_add(200, self._sync_anchor)

    def _mode_changed(self, mode_select: Gtk.ComboBox) -> None:
        mode_id = mode_select.get_active_id()
        if mode_id in MODE_DEFINITIONS:
            self._on_mode_changed(mode_id)

    def _size_allocated(self, _window, _allocation) -> None:
        self._move_to_anchor()

    def _sync_anchor(self) -> bool:
        geometry = (
            _win32_window_geometry(self._parent_handle)
            if self._parent_handle is not None
            else None
        )
        if geometry is not None:
            _bounds, visible, _titlebar_height = geometry
            if not visible:
                self.hide()
                return GLib.SOURCE_CONTINUE
            if not self.get_visible():
                self.show_all()
        self._move_to_anchor(geometry)
        return GLib.SOURCE_CONTINUE

    def _move_to_anchor(
        self,
        geometry: tuple[tuple[int, int, int, int], bool, int] | None = None,
    ) -> None:
        if geometry is None and self._parent_handle is not None:
            geometry = _win32_window_geometry(self._parent_handle)
        if geometry is not None:
            bounds, _visible, titlebar_height = geometry
        else:
            bounds = _monitor_workarea()
            titlebar_height = 32
        if bounds is None:
            return

        width, height = self.get_size()
        size = (max(width, self.WIDTH), max(height, self.HEIGHT))
        position = mode_switcher_position(bounds, size, titlebar_height)
        if self.get_position() != position:
            self.move(*position)

    def _destroyed(self, _window) -> None:
        if self._anchor_source is not None:
            GLib.source_remove(self._anchor_source)
            self._anchor_source = None


class WorkspacePalette(Gtk.Dialog):
    __gtype_name__ = "PhotoGimpWorkspacePalette"

    def __init__(self, image: Gimp.Image | None):
        super().__init__(title="PhotoGIMP — Ferramentas do modo")
        GimpUi.window_set_transient(self)
        self.set_role("photogimp-workspaces")
        self.set_modal(False)
        self.set_default_size(540, 430)
        self.add_button("_Fechar", Gtk.ResponseType.CLOSE)
        self.image = image
        self.active_mode = None

        body = self.get_content_area()
        body.set_border_width(12)
        body.set_spacing(10)
        body.get_style_context().add_class("photogimp-root")

        self.heading = Gtk.Label(label="Ferramentas", xalign=0)
        self.heading.get_style_context().add_class("photogimp-section")
        body.pack_start(self.heading, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_shadow_type(Gtk.ShadowType.NONE)
        body.pack_start(scroll, True, True, 0)
        self.tools = Gtk.FlowBox()
        self.tools.set_selection_mode(Gtk.SelectionMode.NONE)
        self.tools.set_column_spacing(7)
        self.tools.set_row_spacing(7)
        self.tools.set_min_children_per_line(2)
        self.tools.set_max_children_per_line(2)
        scroll.add(self.tools)

        self.comic_actions = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=8
        )
        self.comic_actions.set_homogeneous(True)
        body.pack_start(self.comic_actions, False, False, 0)
        self.page_button = _icon_button(
            "Nova página", "comic-page.svg", "Criar página de quadrinhos"
        )
        self.page_button.connect("clicked", self._create_page)
        self.comic_actions.pack_start(self.page_button, True, True, 0)
        self.tone_button = _icon_button(
            "Criar retícula", "screentone.svg", "Adicionar retícula em uma camada"
        )
        self.tone_button.connect("clicked", self._create_tone)
        self.comic_actions.pack_start(self.tone_button, True, True, 0)

        self.show_all()
        self.set_mode("designer")
        self._update_tone_sensitivity()

    def set_mode(self, mode_id: str) -> None:
        if mode_id not in MODE_DEFINITIONS or mode_id == self.active_mode:
            return
        self.active_mode = mode_id
        self.heading.set_text(f"Ferramentas — {MODE_DEFINITIONS[mode_id]['label']}")
        self._render_tools(mode_id)
        self.comic_actions.set_visible(mode_id == "comic")

    def _render_tools(self, mode_id: str) -> None:
        for child in self.tools.get_children():
            self.tools.remove(child)
        for label_text, shortcut, icon_name in MODE_DEFINITIONS[mode_id]["tools"]:
            tile = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=9)
            tile.get_style_context().add_class("photogimp-tool")
            icon = Gtk.Image.new_from_icon_name(
                icon_name, Gtk.IconSize.LARGE_TOOLBAR
            )
            tile.pack_start(icon, False, False, 0)
            name = Gtk.Label(label=label_text, xalign=0)
            name.set_line_wrap(True)
            name.get_style_context().add_class("photogimp-tool-name")
            tile.pack_start(name, True, True, 0)
            key = Gtk.Label(label=shortcut, xalign=1)
            key.get_style_context().add_class("photogimp-shortcut")
            tile.pack_end(key, False, False, 0)
            self.tools.add(tile)
        self.tools.show_all()

    def _update_tone_sensitivity(self) -> None:
        can_create = (
            self.image is not None
            and self.image.is_valid()
            and self.image.get_base_type() == Gimp.ImageBaseType.RGB
        )
        self.tone_button.set_sensitive(can_create)

    def _create_page(self, _button) -> None:
        dialog = PageDialog(self)
        response = dialog.run()
        settings = dialog.settings() if response == Gtk.ResponseType.OK else None
        dialog.destroy()
        if settings is None:
            return
        try:
            Gimp.progress_init("Criando página de quadrinhos")
            self.image = create_comic_page(settings)
            Gimp.progress_update(1.0)
            self._update_tone_sensitivity()
        except Exception as error:
            _show_error(self, "Não foi possível criar a página", error)

    def _create_tone(self, _button) -> None:
        self._update_tone_sensitivity()
        if not self.tone_button.get_sensitive():
            return
        dialog = ToneDialog(self)
        response = dialog.run()
        settings = dialog.settings() if response == Gtk.ResponseType.OK else None
        dialog.destroy()
        if settings is None:
            return
        try:
            Gimp.progress_init("Criando retícula")
            apply_screentone(self.image, settings)
            Gimp.progress_update(1.0)
        except Exception as error:
            _show_error(self, "Não foi possível criar a retícula", error)


def _interactive_error(procedure: Gimp.Procedure):
    return procedure.new_return_values(
        Gimp.PDBStatusType.CALLING_ERROR,
        GLib.Error("Este comando do PhotoGIMP requer o modo interativo."),
    )


def workspace_run(procedure, run_mode, image, drawables, config, data):
    if run_mode != Gimp.RunMode.INTERACTIVE:
        return _interactive_error(procedure)
    GimpUi.init(PLUGIN_BINARY)
    _load_css()
    palette = WorkspacePalette(image)
    switcher = WorkspaceModeSwitcher(palette.set_mode)
    switcher.show_anchored()
    try:
        palette.run()
    finally:
        switcher.destroy()
        palette.destroy()
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)


def page_run(procedure, run_mode, image, drawables, config, data):
    if run_mode != Gimp.RunMode.INTERACTIVE:
        return _interactive_error(procedure)
    GimpUi.init(PLUGIN_BINARY)
    _load_css()
    dialog = PageDialog(None)
    response = dialog.run()
    settings = dialog.settings() if response == Gtk.ResponseType.OK else None
    dialog.destroy()
    if settings is None:
        return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)
    try:
        Gimp.progress_init("Criando página de quadrinhos")
        create_comic_page(settings)
        Gimp.progress_update(1.0)
    except Exception as error:
        return procedure.new_return_values(
            Gimp.PDBStatusType.EXECUTION_ERROR, GLib.Error(str(error))
        )
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)


def tone_run(procedure, run_mode, image, drawables, config, data):
    if run_mode != Gimp.RunMode.INTERACTIVE:
        return _interactive_error(procedure)
    if image is None or image.get_base_type() != Gimp.ImageBaseType.RGB:
        return procedure.new_return_values(
            Gimp.PDBStatusType.CALLING_ERROR,
            GLib.Error("A retícula requer uma imagem RGB aberta."),
        )
    GimpUi.init(PLUGIN_BINARY)
    _load_css()
    dialog = ToneDialog(None)
    response = dialog.run()
    settings = dialog.settings() if response == Gtk.ResponseType.OK else None
    dialog.destroy()
    if settings is None:
        return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)
    try:
        Gimp.progress_init("Criando retícula")
        apply_screentone(image, settings)
        Gimp.progress_update(1.0)
    except Exception as error:
        return procedure.new_return_values(
            Gimp.PDBStatusType.EXECUTION_ERROR, GLib.Error(str(error))
        )
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)


class PhotoGimpWorkspaces(Gimp.PlugIn):
    def do_query_procedures(self):
        return [WORKSPACE_PROCEDURE, PAGE_PROCEDURE, TONE_PROCEDURE]

    def do_create_procedure(self, name):
        callbacks = {
            WORKSPACE_PROCEDURE: workspace_run,
            PAGE_PROCEDURE: page_run,
            TONE_PROCEDURE: tone_run,
        }
        if name not in callbacks:
            return None

        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, callbacks[name], None
        )
        procedure.set_attribution("PhotoGIMP contributors", "PhotoGIMP", "2026")

        if name == WORKSPACE_PROCEDURE:
            procedure.set_menu_label("_Modos de visualização...")
            procedure.add_menu_path("<Image>/PhotoGIMP")
            procedure.set_icon_file(
                Gio.File.new_for_path(str(ICON_DIR / "designer.svg"))
            )
            procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
            procedure.set_documentation(
                "Alterna os modos de trabalho do PhotoGIMP",
                "Exibe ferramentas para design gráfico, arte digital e quadrinhos.",
                None,
            )
        elif name == PAGE_PROCEDURE:
            procedure.set_menu_label("Nova página de _quadrinhos...")
            procedure.add_menu_path("<Image>/PhotoGIMP")
            procedure.add_menu_path("<Image>/File/Create/PhotoGIMP")
            procedure.set_icon_file(
                Gio.File.new_for_path(str(ICON_DIR / "comic-page.svg"))
            )
            procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
            procedure.set_documentation(
                "Cria uma página de quadrinhos",
                "Cria uma página RGB com quadros, guias e camadas organizadas.",
                None,
            )
        else:
            procedure.set_menu_label("Criar _retícula...")
            procedure.add_menu_path("<Image>/PhotoGIMP")
            procedure.set_icon_file(
                Gio.File.new_for_path(str(ICON_DIR / "screentone.svg"))
            )
            procedure.set_image_types("RGB*")
            procedure.set_sensitivity_mask(
                Gimp.ProcedureSensitivityMask.DRAWABLE
                | Gimp.ProcedureSensitivityMask.DRAWABLES
                | Gimp.ProcedureSensitivityMask.NO_DRAWABLES
            )
            procedure.set_documentation(
                "Cria uma camada de retícula",
                "Gera pontos, linhas ou trama cruzada e respeita a seleção ativa.",
                None,
            )
        return procedure


Gimp.main(PhotoGimpWorkspaces.__gtype__, sys.argv)
