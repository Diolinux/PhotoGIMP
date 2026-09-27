#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PhotoGIMP work modes, comic page layouts, and screentone generator."""

from __future__ import annotations

import ctypes
from math import ceil, hypot, pi
import os
from pathlib import Path
import subprocess
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
    next_mode,
    normalize_mode,
    page_size_pixels,
    panel_rectangles,
    parse_shortcut,
    primary_tool,
    validate_tone_settings,
)


PLUGIN_BINARY = "photogimp-workspaces"
EXTENSION_PROCEDURE = "extension-photogimp-workspaces"
NEXT_MODE_PROCEDURE = "photogimp-workspaces-next-mode"
WORKSPACE_PROCEDURE = "plug-in-photogimp-workspaces"
PAGE_PROCEDURE = "plug-in-photogimp-comic-page"
TONE_PROCEDURE = "plug-in-photogimp-screentone"
ICON_DIR = SCRIPT_DIR / "icons"
MODE_FILE_NAME = "photogimp-workspace-mode"
SWITCHER_TITLE = "Modo de visualização do PhotoGIMP"

CSS = b"""
.photogimp-global-switcher {
  background-color: @theme_bg_color;
  border: 1px solid alpha(@theme_fg_color, 0.18);
  padding: 2px 5px;
}
.photogimp-mode-caption { font-weight: 600; margin-right: 4px; }
.photogimp-mode-select { min-width: 205px; }
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


def _mode_file() -> Path:
    return Path(Gimp.directory()) / MODE_FILE_NAME


def _load_mode() -> str:
    try:
        return normalize_mode(_mode_file().read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return normalize_mode(None)


def _save_mode(mode_id: str) -> None:
    try:
        _mode_file().write_text(mode_id, encoding="utf-8")
    except OSError:
        pass


# --- Windows integration -----------------------------------------------------
#
# GIMP does not let Python plug-ins add widgets to its main window, so the mode
# switcher is a borderless window owned by the GIMP main window. On Windows the
# owner relationship keeps it above GIMP (and hides it when GIMP is minimized)
# without floating above other applications.

GWL_STYLE = -16
GWLP_HWNDPARENT = -8
GW_OWNER = 4
WS_CAPTION = 0x00C00000
KEYEVENTF_KEYUP = 0x0002
VIRTUAL_MODIFIERS = {"Ctrl": 0x11, "Shift": 0x10, "Alt": 0x12}

_USER32 = None
_WNDENUMPROC = None
_SET_WINDOW_LONG = None


def _user32():
    global _USER32, _WNDENUMPROC, _SET_WINDOW_LONG
    if _USER32 is not None:
        return _USER32

    from ctypes import wintypes

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    _WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows.argtypes = [_WNDENUMPROC, wintypes.LPARAM]
    user32.EnumWindows.restype = wintypes.BOOL
    user32.GetWindowThreadProcessId.argtypes = [
        wintypes.HWND,
        ctypes.POINTER(wintypes.DWORD),
    ]
    user32.GetWindowThreadProcessId.restype = wintypes.DWORD
    user32.GetWindow.argtypes = [wintypes.HWND, ctypes.c_uint]
    user32.GetWindow.restype = wintypes.HWND
    user32.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.GetWindowLongW.restype = ctypes.c_long
    user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
    user32.GetWindowTextLengthW.restype = ctypes.c_int
    user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.GetWindowTextW.restype = ctypes.c_int
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
    user32.SetForegroundWindow.argtypes = [wintypes.HWND]
    user32.SetForegroundWindow.restype = wintypes.BOOL
    user32.keybd_event.argtypes = [
        wintypes.BYTE,
        wintypes.BYTE,
        wintypes.DWORD,
        ctypes.c_size_t,
    ]
    user32.keybd_event.restype = None
    user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
    user32.GetAsyncKeyState.restype = ctypes.c_short
    # SetWindowLongPtrW only exists as an export in 64-bit user32.
    set_window_long = getattr(user32, "SetWindowLongPtrW", None) or user32.SetWindowLongW
    set_window_long.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_void_p]
    set_window_long.restype = ctypes.c_void_p
    _SET_WINDOW_LONG = set_window_long
    _USER32 = user32
    return user32


def _native_handle_value(handle: GLib.Bytes | None) -> int | None:
    if handle is None:
        return None
    data = bytes(handle.get_data())
    pointer_size = ctypes.sizeof(ctypes.c_void_p)
    if len(data) < pointer_size:
        return None
    value = int.from_bytes(data[:pointer_size], byteorder=sys.byteorder)
    return value or None


def _win32_process_windows(pid: int) -> list[int]:
    from ctypes import wintypes

    user32 = _user32()
    found = []

    def collect(hwnd, _lparam):
        owner_pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner_pid))
        if hwnd and owner_pid.value == pid:
            found.append(int(hwnd))
        return True

    user32.EnumWindows(_WNDENUMPROC(collect), 0)
    return found


def _win32_window_title(hwnd: int) -> str:
    user32 = _user32()
    length = user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value


def _win32_find_gimp_window() -> int | None:
    """Return the GIMP image window: the parent process's largest main window."""
    if sys.platform != "win32":
        return None

    try:
        display = Gimp.default_display()
        if display is not None and display.is_valid():
            value = _native_handle_value(display.get_window_handle())
            if value is not None:
                return value
    except Exception:
        pass

    from ctypes import wintypes

    user32 = _user32()
    best, best_area = None, 0
    for hwnd in _win32_process_windows(os.getppid()):
        if not user32.IsWindowVisible(hwnd) or user32.GetWindow(hwnd, GW_OWNER):
            continue
        # Skips the splash screen and other undecorated helper windows.
        if not user32.GetWindowLongW(hwnd, GWL_STYLE) & WS_CAPTION:
            continue
        rect = wintypes.RECT()
        if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            continue
        area = (rect.right - rect.left) * (rect.bottom - rect.top)
        if area > best_area:
            best, best_area = hwnd, area
    return best


def _win32_own_window(title: str) -> int | None:
    for hwnd in _win32_process_windows(os.getpid()):
        if _win32_window_title(hwnd) == title:
            return hwnd
    return None


def _win32_set_owner(hwnd: int, owner: int) -> None:
    _user32()
    _SET_WINDOW_LONG(hwnd, GWLP_HWNDPARENT, owner)


def _win32_send_shortcut(hwnd: int, shortcut: str) -> bool:
    """Focus the GIMP window and replay a PhotoGIMP keyboard shortcut."""
    modifiers, key = parse_shortcut(shortcut)
    user32 = _user32()
    if not user32.IsWindow(hwnd) or not user32.SetForegroundWindow(hwnd):
        return False
    codes = [VIRTUAL_MODIFIERS[modifier] for modifier in modifiers] + [ord(key)]

    started = GLib.get_monotonic_time()

    def press() -> bool:
        held = any(
            user32.GetAsyncKeyState(code) & 0x8000
            for code in VIRTUAL_MODIFIERS.values()
        )
        if held and GLib.get_monotonic_time() - started < 2_000_000:
            return GLib.SOURCE_CONTINUE
        for code in codes:
            user32.keybd_event(code, 0, 0, 0)
        for code in reversed(codes):
            user32.keybd_event(code, 0, KEYEVENTF_KEYUP, 0)
        return GLib.SOURCE_REMOVE

    # Give Windows a moment to move keyboard focus to GIMP.
    GLib.timeout_add(80, press)
    return True


def _win32_window_geometry(
    handle: int,
) -> tuple[tuple[int, int, int, int], bool, int] | None:
    if sys.platform != "win32":
        return None

    from ctypes import wintypes

    hwnd = wintypes.HWND(handle)
    user32 = _user32()
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

    # A GIMP window can be larger than its monitor; keep the switcher on screen.
    class MONITORINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("rcMonitor", wintypes.RECT),
            ("rcWork", wintypes.RECT),
            ("dwFlags", wintypes.DWORD),
        ]

    user32.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
    user32.MonitorFromWindow.restype = wintypes.HANDLE
    user32.GetMonitorInfoW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MONITORINFO)]
    user32.GetMonitorInfoW.restype = wintypes.BOOL
    monitor = user32.MonitorFromWindow(hwnd, 2)  # MONITOR_DEFAULTTONEAREST
    info = MONITORINFO(cbSize=ctypes.sizeof(MONITORINFO))
    if monitor and user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
        work = info.rcWork
        clipped = (
            max(bounds[0], work.left),
            max(bounds[1], work.top),
            min(bounds[2], work.right),
            min(bounds[3], work.bottom),
        )
        if clipped[0] < clipped[2] and clipped[1] < clipped[3]:
            bounds = clipped

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
    """Borderless mode selector kept at the top-right of the GIMP main window."""

    __gtype_name__ = "PhotoGimpWorkspaceModeSwitcher"

    WIDTH = 270
    HEIGHT = 34

    def __init__(self, host: "WorkspaceHost"):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_title(SWITCHER_TITLE)
        self.set_role("photogimp-global-mode-switcher")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_focus_on_map(False)
        self.set_type_hint(Gdk.WindowTypeHint.TOOLBAR)
        self.set_default_size(self.WIDTH, self.HEIGHT)
        self.set_size_request(self.WIDTH, self.HEIGHT)
        if sys.platform != "win32":
            # Without a native owner the selector would fall behind GIMP.
            self.set_keep_above(True)
        self.connect("delete-event", lambda *_args: True)
        self._host = host

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
        self.mode_select.set_tooltip_text(
            "Mudar modo de trabalho (Ctrl+Shift+Espaço). A barra de ferramentas "
            "da esquerda é reorganizada na próxima vez que o GIMP abrir."
        )
        self.mode_select.set_active_id(host.mode)
        self._handler = self.mode_select.connect("changed", self._mode_changed)
        caption.set_mnemonic_widget(self.mode_select)
        content.pack_start(self.mode_select, True, True, 0)
        self.add(shell)

    def _mode_changed(self, mode_select: Gtk.ComboBox) -> None:
        mode_id = mode_select.get_active_id()
        if mode_id in MODE_DEFINITIONS:
            self._host.set_mode(mode_id)

    def show_mode(self, mode_id: str) -> None:
        """Reflect a mode chosen elsewhere (the shortcut) without re-triggering."""
        with self.mode_select.handler_block(self._handler):
            self.mode_select.set_active_id(mode_id)

    def move_to_anchor(
        self, bounds: tuple[int, int, int, int], titlebar_height: int
    ) -> None:
        width, height = self.get_size()
        size = (max(width, self.WIDTH), max(height, self.HEIGHT))
        position = mode_switcher_position(bounds, size, titlebar_height)
        if self.get_position() != position:
            self.move(*position)


class WorkspaceHost:
    """Owns the always-visible mode switcher for one GIMP session."""

    SYNC_INTERVAL_MS = 250

    def __init__(self):
        self.mode = _load_mode()
        self.gimp_window: int | None = None
        self._owner: int | None = None
        self._visible = True
        self._toolbox_helper_started = False
        self._restart_notice_shown = False
        self.switcher = WorkspaceModeSwitcher(self)

    def start(self) -> None:
        self.switcher.show_all()
        self._sync()
        GLib.timeout_add(self.SYNC_INTERVAL_MS, self._sync)

    def set_mode(self, mode_id: str) -> None:
        mode_id = normalize_mode(mode_id)
        if mode_id == self.mode:
            return
        self.mode = mode_id
        _save_mode(mode_id)
        self.switcher.show_mode(mode_id)
        self._schedule_toolbox_update()
        if not self._restart_notice_shown:
            # The tool shortcut must reach GIMP, not the notice, so it is sent
            # once the notice is dismissed.
            self._notify_restart(self._activate_primary_tool)
        else:
            self._activate_primary_tool()

    def next_mode_run(self, procedure, *_args):
        self.set_mode(next_mode(self.mode))
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)

    def _activate_primary_tool(self) -> None:
        """Select the mode's main tool in the left toolbox right away."""
        if sys.platform != "win32" or self.gimp_window is None:
            return
        _label, shortcut, _icon, _action = primary_tool(self.mode)
        try:
            _win32_send_shortcut(self.gimp_window, shortcut)
        except (OSError, ValueError) as error:
            print(f"PhotoGIMP workspaces: {error}", file=sys.stderr)

    def _schedule_toolbox_update(self) -> None:
        """Start the helper that rewrites toolrc after GIMP saves it on exit."""
        if self._toolbox_helper_started:
            return
        helper = SCRIPT_DIR / "apply_toolbox.py"
        arguments = [sys.executable, str(helper), str(os.getppid()), Gimp.directory()]
        options: dict = {
            "stdin": subprocess.DEVNULL,
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
            "close_fds": True,
        }
        if sys.platform == "win32":
            options["creationflags"] = (
                subprocess.DETACHED_PROCESS
                | subprocess.CREATE_NEW_PROCESS_GROUP
                | subprocess.CREATE_NO_WINDOW
            )
        else:
            options["start_new_session"] = True
        try:
            subprocess.Popen(arguments, **options)
            self._toolbox_helper_started = True
        except OSError as error:
            print(f"PhotoGIMP workspaces: {error}", file=sys.stderr)

    def _notify_restart(self, on_close) -> None:
        """Explain once per session when the toolbox change takes effect."""
        self._restart_notice_shown = True
        dialog = Gtk.MessageDialog(
            transient_for=self.switcher,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Modo de trabalho alterado",
        )
        dialog.set_title("PhotoGIMP")
        dialog.set_position(Gtk.WindowPosition.CENTER)
        dialog.format_secondary_text(
            "A ferramenta principal do modo será selecionada agora. A barra de "
            "ferramentas da esquerda mostrará apenas as ferramentas deste modo "
            "na próxima vez que o GIMP for aberto."
        )

        def closed(widget, _response) -> None:
            widget.destroy()
            on_close()

        dialog.connect("response", closed)
        dialog.show_all()
        dialog.present()

    # --- Anchoring ------------------------------------------------------

    def _bounds(self) -> tuple[tuple[int, int, int, int], int] | None:
        if sys.platform == "win32":
            geometry = None
            if self.gimp_window is not None:
                geometry = _win32_window_geometry(self.gimp_window)
            if geometry is None:
                self.gimp_window = _win32_find_gimp_window()
                self._owner = None
                if self.gimp_window is not None:
                    geometry = _win32_window_geometry(self.gimp_window)
            if geometry is None:
                return None
            bounds, visible, titlebar_height = geometry
            self._visible = visible
            return bounds, titlebar_height

        bounds = _monitor_workarea()
        return (bounds, 32) if bounds is not None else None

    def _own_switcher(self) -> None:
        """Make GIMP the native owner of the switcher (Windows only)."""
        if sys.platform != "win32" or self.gimp_window is None:
            return
        if self._owner == self.gimp_window:
            return
        hwnd = _win32_own_window(SWITCHER_TITLE)
        if hwnd is not None:
            _win32_set_owner(hwnd, self.gimp_window)
            self._owner = self.gimp_window

    def _sync(self) -> bool:
        try:
            anchor = self._bounds()
            if anchor is None or not self._visible:
                # GIMP is still starting, minimized, or its window is gone.
                self.switcher.hide()
                return GLib.SOURCE_CONTINUE
            if not self.switcher.get_visible():
                self.switcher.show_all()
            self._own_switcher()
            bounds, titlebar_height = anchor
            self.switcher.move_to_anchor(bounds, titlebar_height)
        except Exception as error:  # Keep the session alive on odd window states.
            print(f"PhotoGIMP workspaces: {error}", file=sys.stderr)
        return GLib.SOURCE_CONTINUE


def _interactive_error(procedure: Gimp.Procedure):
    return procedure.new_return_values(
        Gimp.PDBStatusType.CALLING_ERROR,
        GLib.Error("Este comando do PhotoGIMP requer o modo interativo."),
    )


def extension_run(procedure, *_args):
    """Started by GIMP at launch; keeps the mode switcher on screen."""
    plug_in = procedure.get_plug_in()
    GimpUi.init(PLUGIN_BINARY)
    _load_css()
    host = WorkspaceHost()

    next_mode_procedure = Gimp.Procedure.new(
        plug_in,
        NEXT_MODE_PROCEDURE,
        Gimp.PDBProcType.TEMPORARY,
        host.next_mode_run,
        None,
    )
    next_mode_procedure.set_attribution("PhotoGIMP contributors", "PhotoGIMP", "2026")
    next_mode_procedure.set_documentation(
        "Passa para o próximo modo de trabalho do PhotoGIMP", None, None
    )
    plug_in.add_temp_procedure(next_mode_procedure)

    procedure.persistent_ready()
    plug_in.persistent_enable()
    host.start()
    Gtk.main()
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)


def workspace_run(procedure, run_mode, image, drawables, config, data):
    if run_mode != Gimp.RunMode.INTERACTIVE:
        return _interactive_error(procedure)

    pdb = Gimp.get_pdb()
    if pdb.lookup_procedure(NEXT_MODE_PROCEDURE) is None:
        # The switcher normally starts with GIMP; start it now if it did not.
        extension = pdb.lookup_procedure(EXTENSION_PROCEDURE)
        if extension is not None:
            extension.run(extension.create_config())
    next_mode_procedure = pdb.lookup_procedure(NEXT_MODE_PROCEDURE)
    if next_mode_procedure is None:
        return procedure.new_return_values(
            Gimp.PDBStatusType.EXECUTION_ERROR,
            GLib.Error("O seletor de modos do PhotoGIMP não está em execução."),
        )
    next_mode_procedure.run(next_mode_procedure.create_config())
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
    try:
        settings = dialog.settings() if response == Gtk.ResponseType.OK else None
    except ValueError as error:
        dialog.destroy()
        return procedure.new_return_values(
            Gimp.PDBStatusType.CALLING_ERROR, GLib.Error(str(error))
        )
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
    def do_set_i18n(self, name):
        # The UI strings are not translated through gettext catalogs.
        return False

    def do_query_procedures(self):
        return [
            EXTENSION_PROCEDURE,
            WORKSPACE_PROCEDURE,
            PAGE_PROCEDURE,
            TONE_PROCEDURE,
        ]

    def do_create_procedure(self, name):
        if name == EXTENSION_PROCEDURE:
            # A persistent procedure without arguments is launched by GIMP at
            # startup, which is what keeps the mode switcher always visible.
            procedure = Gimp.Procedure.new(
                self, name, Gimp.PDBProcType.PERSISTENT, extension_run, None
            )
            procedure.set_attribution("PhotoGIMP contributors", "PhotoGIMP", "2026")
            procedure.set_documentation(
                "Seletor de modos do PhotoGIMP",
                "Mantém o seletor de modos no canto superior direito da janela "
                "principal do GIMP.",
                None,
            )
            return procedure

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
            procedure.set_menu_label("Próximo _modo de trabalho")
            procedure.add_menu_path("<Image>/PhotoGIMP")
            procedure.set_icon_file(
                Gio.File.new_for_path(str(ICON_DIR / "designer.svg"))
            )
            procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
            procedure.set_documentation(
                "Passa para o próximo modo de trabalho do PhotoGIMP",
                "Alterna entre Designer gráfico, Artista digital e Quadrinista, "
                "como o seletor fixo no canto superior direito da janela principal.",
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
