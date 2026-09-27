"""Apply the saved PhotoGIMP mode to toolrc once GIMP has exited.

GIMP rewrites toolrc when it quits, so the work-mode plug-in starts this helper
as a detached process. It waits for the GIMP process to end, then shows only
the tools of the saved mode in the left toolbox for the next session. When the
user asked to restart GIMP from the mode selector, it also starts GIMP again.

Usage: apply_toolbox.py <gimp-pid> <gimp-config-dir>
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from workspace_core import normalize_mode, toolbox_for_mode  # noqa: E402

MODE_FILE_NAME = "photogimp-workspace-mode"
RESTART_FILE_NAME = "photogimp-restart"
RESTART_TIMEOUT_SECONDS = 300


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


def pending_relaunch(config_dir: Path, now: float) -> str | None:
    """Return the GIMP binary to start again if a restart was just requested.

    The request expires so that a quit cancelled over unsaved images does not
    reopen GIMP when it is eventually closed much later.
    """
    request = config_dir / RESTART_FILE_NAME
    try:
        timestamp, executable = request.read_text(encoding="utf-8").splitlines()[:2]
        request.unlink()
    except (OSError, ValueError):
        return None
    try:
        requested_at = float(timestamp)
    except ValueError:
        return None
    if not 0 <= now - requested_at <= RESTART_TIMEOUT_SECONDS:
        return None
    return executable if Path(executable).is_file() else None


def relaunch(executable: str) -> None:
    options: dict = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "close_fds": True,
    }
    if sys.platform == "win32":
        options["creationflags"] = (
            subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        options["start_new_session"] = True
    subprocess.Popen([executable], **options)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    wait_for_exit(int(argv[1]))
    # Let GIMP finish flushing its own configuration files.
    time.sleep(1)
    config_dir = Path(argv[2])
    apply(config_dir)
    executable = pending_relaunch(config_dir, time.time())
    if executable is not None:
        relaunch(executable)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
