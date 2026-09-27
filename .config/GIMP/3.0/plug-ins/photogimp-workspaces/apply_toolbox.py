"""Apply the saved PhotoGIMP mode to toolrc once GIMP has exited.

GIMP rewrites toolrc when it quits, so the work-mode plug-in starts this helper
as a detached process. It waits for the GIMP process to end, then shows only
the tools of the saved mode in the left toolbox for the next session.

Usage: apply_toolbox.py <gimp-pid> <gimp-config-dir>
"""

from __future__ import annotations

import os
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workspace_core import normalize_mode, toolbox_for_mode  # noqa: E402

MODE_FILE_NAME = "photogimp-workspace-mode"


def wait_for_exit(pid: int) -> None:
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel32.OpenProcess.restype = wintypes.HANDLE
        kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel32.WaitForSingleObject.restype = wintypes.DWORD
        kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        synchronize = 0x00100000
        handle = kernel32.OpenProcess(synchronize, False, pid)
        if handle:
            kernel32.WaitForSingleObject(handle, 0xFFFFFFFF)
            kernel32.CloseHandle(handle)
        return

    while True:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        except PermissionError:
            pass
        time.sleep(1)


def apply(config_dir: Path) -> None:
    try:
        mode = normalize_mode((config_dir / MODE_FILE_NAME).read_text(encoding="utf-8"))
    except OSError:
        return
    toolrc = config_dir / "toolrc"
    try:
        current = toolrc.read_text(encoding="utf-8")
    except OSError:
        return
    updated = toolbox_for_mode(current, mode)
    if updated == current:
        return
    temporary = toolrc.with_name("toolrc.photogimp-tmp")
    temporary.write_text(updated, encoding="utf-8", newline="")
    os.replace(temporary, toolrc)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    wait_for_exit(int(argv[1]))
    # Let GIMP finish flushing its own configuration files.
    time.sleep(1)
    apply(Path(argv[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
