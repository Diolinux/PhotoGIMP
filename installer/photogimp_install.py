#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""PhotoGIMP interactive installer (stdlib only, Python 3.9+).

Detects an existing GIMP, backs up settings, applies PhotoGIMP configuration,
and supports verified restore/uninstall.
"""

from __future__ import annotations

import argparse
import base64
import contextlib
import hashlib
import json
import os
import platform
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

SCRIPT_VERSION = "1.2.0"
JOURNAL_NAME = ".photogimp-install-journal.json"
UNSUPPORTED_KINDS = frozenset({"snap", "portable"})
BACKUP_CONTROL_FILES = frozenset({"backup-meta.json", "backup-manifest.json"})
BACKUP_FORMAT_VERSION = 3
BACKUP_PROFILE_DIR = "profile"
BACKUP_CONTROL_DIR = "control"
PAYLOAD_MANIFEST_NAME = "payload-manifest.json"
GIMP_DOWNLOAD_URL = "https://www.gimp.org/downloads/"
FLATHUB_GIMP_ID = "org.gimp.GIMP"

# Payload is authored for this config folder name only (GIMP 3.0.x series).
PAYLOAD_CONFIG_VERSION = "3.0"
SUPPORTED_CONFIG_FOLDERS = frozenset({PAYLOAD_CONFIG_VERSION})

CORE_FILES = (
    "shortcutsrc",
    "toolrc",
    "sessionrc",
    "gimprc",
    "contextrc",
)
CORE_DIRS = (
    "splashes",
    "tool-options",
)
# Files/dirs the installer may write (used for surgical uninstall)
MANAGED_FILES = CORE_FILES + ("theme.css",)
MANAGED_DIRS = CORE_DIRS
MANAGED_TOPS = frozenset(MANAGED_FILES + MANAGED_DIRS)
PAYLOAD_EXCLUSIONS = {
    "filters/": "author-specific last-used filter state, not PhotoGIMP UI configuration",
    "plug-in-settings/": "author-specific import/export dialog history",
}
EXIT_OK = 0
EXIT_ERROR = 1
EXIT_PREFLIGHT = 2
EXIT_CANCELLED = 3

PROCESS_RUNNING = "running"
PROCESS_NOT_RUNNING = "not-running"
PROCESS_UNKNOWN = "unknown"

_held_locks: set[str] = set()


def safe_managed_relative_path(value: str) -> bool:
    """Return True for a normalized payload path under a managed top-level item."""
    path = Path(value)
    if not value or path.is_absolute() or ".." in path.parts or "." in path.parts:
        return False
    return path.parts[0] in MANAGED_TOPS


def select_number(answer: str, items: list) -> Optional[object]:
    """Select a 1-based item; reject zero, negatives, and out-of-range input."""
    try:
        index = int(answer)
    except ValueError:
        return None
    if index < 1 or index > len(items):
        return None
    return items[index - 1]


# ---------------------------------------------------------------------------
# Terminal helpers
# ---------------------------------------------------------------------------


_prompt_eof = False


def _is_tty() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def require_interactive(action: str) -> Optional[int]:
    """Return EXIT_PREFLIGHT if stdin is not a TTY (blocks headless EOF consent)."""
    if _is_tty():
        return None
    error(
        f"Refusing to {action} without an interactive terminal. "
        "Pipe/EOF input cannot approve destructive changes. "
        "Run from a real terminal (or use status which is read-only)."
    )
    return EXIT_PREFLIGHT


def info(msg: str) -> None:
    print(msg)


def warn(msg: str) -> None:
    print(f"Warning: {msg}", file=sys.stderr)


def error(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)


def prompt(msg: str, default: str = "") -> str:
    """Prompt the user. On EOF, returns empty string (cancel), never the default."""
    global _prompt_eof
    _prompt_eof = False
    suffix = f" [{default}]" if default else ""
    try:
        value = input(f"{msg}{suffix}: ").strip()
    except EOFError:
        _prompt_eof = True
        print()
        return ""  # cancel — do not treat EOF as accepting default
    return value or default


def confirm(msg: str, default: bool = False) -> bool:
    """Yes/no prompt. On EOF returns False (cancel), never default-yes."""
    yn = "Y/n" if default else "y/N"
    try:
        answer = input(f"{msg} ({yn}): ").strip().lower()
    except EOFError:
        print()
        return False
    if not answer:
        return default
    return answer in ("y", "yes")


def pause(msg: str = "Press Enter to continue...") -> None:
    try:
        input(msg)
    except EOFError:
        print()


def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)


def run(
    args: list[str],
    *,
    check: bool = False,
    capture: bool = True,
    env: Optional[dict] = None,
    timeout: Optional[float] = 60.0,
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            args,
            check=check,
            text=True,
            capture_output=capture,
            env=env,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout="",
            stderr=f"timeout after {timeout}s: {' '.join(args)}",
        )


# ---------------------------------------------------------------------------
# Paths & state
# ---------------------------------------------------------------------------


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def payload_dir() -> Path:
    return repo_root() / ".config" / "GIMP" / "3.0"


def payload_manifest_path() -> Path:
    return Path(__file__).resolve().parent / PAYLOAD_MANIFEST_NAME


def linux_branding_root() -> Path:
    return repo_root() / ".local"


def data_home() -> Path:
    system = platform.system()
    if system == "Windows":
        return _absolute_environment_path(
            "LOCALAPPDATA", user_home() / "AppData" / "Local"
        ) / "PhotoGIMP"
    if os.environ.get("XDG_DATA_HOME"):
        return _absolute_environment_path(
            "XDG_DATA_HOME", user_home() / ".local" / "share"
        ) / "photogimp"
    return user_home() / ".local" / "share" / "photogimp"


def xdg_config_home() -> Path:
    return _absolute_environment_path(
        "XDG_CONFIG_HOME", user_home() / ".config"
    )


def xdg_data_home() -> Path:
    return _absolute_environment_path(
        "XDG_DATA_HOME", user_home() / ".local" / "share"
    )


def _absolute_environment_path(name: str, fallback: Path) -> Path:
    value = os.environ.get(name)
    path = Path(value).expanduser() if value else fallback.expanduser()
    if not path.is_absolute():
        raise ValueError(
            f"{name} must be an absolute path, got {value!r}. "
            "Unset it or provide the absolute path used by the desktop user."
        )
    return path.resolve(strict=False)


def user_home() -> Path:
    home = Path.home().expanduser()
    if not home.is_absolute():
        raise ValueError(
            f"The current user home must be absolute, got {str(home)!r}. "
            "Fix HOME/USERPROFILE before running the installer."
        )
    return home.resolve(strict=False)


def validate_environment_paths() -> Optional[str]:
    try:
        data = data_home()
        _reject_symlink_directory(data, "PhotoGIMP data directory")
        if is_windows():
            _absolute_environment_path(
                "APPDATA", user_home() / "AppData" / "Roaming"
            )
        elif is_linux():
            xdg_config_home()
            xdg_data_home()
    except (OSError, ValueError) as exc:
        return str(exc)
    return None


def is_elevated() -> bool:
    if os.name == "posix" and hasattr(os, "geteuid"):
        return os.geteuid() == 0
    if is_windows():
        try:
            import ctypes

            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except (AttributeError, OSError):
            return False
    return False


def preflight_execution_context() -> int:
    problem = validate_environment_paths()
    if problem:
        error(problem)
        return EXIT_PREFLIGHT
    if is_elevated():
        error(
            "Refusing elevated execution for user-profile operations. "
            "Run the installer as the desktop user. Install GIMP separately with "
            "the platform's trusted package mechanism if needed."
        )
        return EXIT_PREFLIGHT
    return EXIT_OK


def backups_dir() -> Path:
    return data_home() / "backups"


def state_path() -> Path:
    return data_home() / "state.json"


def journal_path(config_dir: Path) -> Path:
    canonical = str(config_dir.expanduser().resolve(strict=False))
    key = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return data_home() / "transactions" / f"install-{key}.json"


def legacy_journal_path(config_dir: Path) -> Path:
    return config_dir / JOURNAL_NAME


def _reject_symlink_directory(path: Path, label: str) -> None:
    if _is_link_or_reparse(path):
        raise OSError(f"{label} must not be a link or reparse point: {path}")
    if path.exists() and not path.is_dir():
        raise OSError(f"{label} is not a directory: {path}")


def _ensure_directory_durable(path: Path, *, mode: int = 0o700) -> None:
    existed = path.exists()
    path.mkdir(parents=True, exist_ok=True, mode=mode)
    if not existed:
        _fsync_directory(path)
        _fsync_directory(path.parent)


def _acquire_file_lock(fd: int) -> None:
    if is_windows():
        import msvcrt

        if os.fstat(fd).st_size == 0:
            os.write(fd, b"\0")
            os.fsync(fd)
        os.lseek(fd, 0, os.SEEK_SET)
        try:
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            raise OSError("operation lock is held by another process") from exc
    else:
        import fcntl

        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise OSError("operation lock is held by another process") from exc


def _release_file_lock(fd: int) -> None:
    if is_windows():
        import msvcrt

        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    else:
        import fcntl

        fcntl.flock(fd, fcntl.LOCK_UN)


@contextlib.contextmanager
def operation_lock(scope: str, target: Path):
    """Serialize registry and per-profile mutations across installer processes."""
    root = data_home()
    _reject_symlink_directory(root, "PhotoGIMP data directory")
    _ensure_directory_durable(root)
    locks = root / "locks"
    _reject_symlink_directory(locks, "PhotoGIMP lock directory")
    _ensure_directory_durable(locks)
    canonical = str(target.expanduser().resolve(strict=False))
    key = hashlib.sha256(f"{scope}\0{canonical}".encode("utf-8")).hexdigest()
    path = locks / f"{key}.lock"
    lock_key = str(path)
    if lock_key in _held_locks:
        yield
        return
    payload = json.dumps(
        {
            "pid": os.getpid(),
            "scope": scope,
            "target": canonical,
            "created_at": iso_now(),
        },
        indent=2,
    ) + "\n"
    if _is_link_or_reparse(path):
        raise OSError(f"Operation lock path must not be a link: {path}")
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o600)
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise OSError(f"Operation lock is not a regular file: {path}")
    try:
        _acquire_file_lock(fd)
    except OSError as exc:
        os.close(fd)
        raise OSError(f"Another PhotoGIMP operation is active for {canonical}: {path}") from exc
    os.ftruncate(fd, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    os.write(fd, payload.encode("utf-8"))
    os.fsync(fd)
    try:
        _held_locks.add(lock_key)
        yield
    finally:
        _held_locks.discard(lock_key)
        try:
            _release_file_lock(fd)
        finally:
            os.close(fd)


@dataclass
class InstallState:
    backup_id: str = ""
    config_path: str = ""
    installed_at: str = ""
    config_version: str = PAYLOAD_CONFIG_VERSION
    platform: str = ""
    gimp_kind: str = ""
    gimp_binary: str = ""
    gimp_app_path: str = ""
    gimp_version: str = ""
    branding_installed: bool = False
    desktop_backup: str = ""
    installed_hashes: dict = field(default_factory=dict)  # relpath -> sha256
    script_version: str = SCRIPT_VERSION

    def key(self) -> str:
        try:
            return str(Path(self.config_path).resolve()) if self.config_path else ""
        except OSError:
            return self.config_path


def _state_from_dict(data: dict) -> InstallState:
    if "config_version" not in data and "payload_version" in data:
        data = dict(data)
        data["config_version"] = data.pop("payload_version")
    known = set(InstallState.__dataclass_fields__)
    clean = {k: v for k, v in data.items() if k in known}
    string_fields = {
        "backup_id",
        "config_path",
        "installed_at",
        "config_version",
        "platform",
        "gimp_kind",
        "gimp_binary",
        "gimp_app_path",
        "gimp_version",
        "desktop_backup",
        "script_version",
    }
    for name in string_fields:
        if not isinstance(clean.get(name, ""), str):
            clean[name] = ""
    if not isinstance(clean.get("branding_installed", False), bool):
        clean["branding_installed"] = False
    hashes = clean.get("installed_hashes", {})
    if not isinstance(hashes, dict):
        hashes = {}
    clean["installed_hashes"] = {
        rel: digest
        for rel, digest in hashes.items()
        if isinstance(rel, str)
        and isinstance(digest, str)
        and re.fullmatch(r"[0-9a-f]{64}", digest)
        and safe_managed_relative_path(rel)
    }
    return InstallState(**clean)


def _state_record_problem(data: dict) -> Optional[str]:
    state = _state_from_dict(data)
    if not state.config_path or not Path(state.config_path).is_absolute():
        return "install state config_path must be absolute"
    if Path(state.config_path).name not in SUPPORTED_CONFIG_FOLDERS:
        return "install state config_path has an unsupported version folder"
    if state.backup_id and (
        Path(state.backup_id).name != state.backup_id
        or "/" in state.backup_id
        or "\\" in state.backup_id
    ):
        return "install state contains an unsafe backup id"
    if state.gimp_kind not in {"native", "flatpak", "brew"}:
        return "install state contains an unsupported GIMP kind"
    return None


@dataclass
class InstallRegistry:
    """Per-profile install records keyed by resolved config_path."""

    installs: dict = field(default_factory=dict)  # key -> InstallState fields dict
    errors: list[str] = field(default_factory=list)

    @classmethod
    def load(cls) -> "InstallRegistry":
        path = state_path()
        if not path.is_file():
            return cls()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return cls(errors=[f"Invalid install registry {path}: {exc}"])
        # Migrate legacy singleton format
        if isinstance(data, dict) and "installs" not in data and data.get("config_path"):
            st = _state_from_dict(data)
            problem = _state_record_problem(data)
            if problem:
                return cls(errors=[f"Invalid legacy install state: {problem}"])
            key = st.key() or st.config_path
            return cls(installs={key: asdict(st)})
        installs = {}
        errors: list[str] = []
        if isinstance(data, dict):
            raw = data.get("installs") or {}
            if isinstance(raw, dict):
                for k, v in raw.items():
                    if isinstance(k, str) and isinstance(v, dict):
                        problem = _state_record_problem(v)
                        if problem:
                            errors.append(f"Invalid install record {k!r}: {problem}")
                        else:
                            state = _state_from_dict(v)
                            if k not in {state.config_path, state.key()}:
                                errors.append(
                                    f"Invalid install record {k!r}: key does not match config_path"
                                )
                            else:
                                installs[k] = v
                    else:
                        errors.append("Install registry contains an invalid record")
            else:
                errors.append("Install registry 'installs' must be an object")
        else:
            errors.append("Install registry root must be an object")
        return cls(installs=installs, errors=errors)

    def _save_unlocked(self) -> None:
        if self.errors:
            raise OSError("Refusing to overwrite invalid install registry: " + "; ".join(self.errors))
        path = state_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_json(path, {"version": 2, "installs": self.installs})

    def save(self) -> None:
        with operation_lock("registry", state_path()):
            self._save_unlocked()

    def upsert(self, state: InstallState) -> None:
        key = state.key() or state.config_path
        if not key:
            return
        with operation_lock("registry", state_path()):
            fresh = InstallRegistry.load()
            if fresh.errors:
                raise OSError(
                    "Refusing to overwrite invalid install registry: "
                    + "; ".join(fresh.errors)
                )
            fresh.installs[key] = asdict(state)
            fresh._save_unlocked()
            self.installs = fresh.installs

    def remove(self, config_path: str) -> None:
        try:
            key = str(Path(config_path).resolve())
        except OSError:
            key = config_path
        with operation_lock("registry", state_path()):
            fresh = InstallRegistry.load()
            if fresh.errors:
                raise OSError(
                    "Refusing to overwrite invalid install registry: "
                    + "; ".join(fresh.errors)
                )
            fresh.installs.pop(key, None)
            fresh.installs.pop(config_path, None)
            fresh._save_unlocked()
            self.installs = fresh.installs

    def get(self, config_path: str) -> Optional[InstallState]:
        try:
            key = str(Path(config_path).resolve())
        except OSError:
            key = config_path
        data = self.installs.get(key) or self.installs.get(config_path)
        if not data:
            return None
        return _state_from_dict(data)

    def all_states(self) -> list[InstallState]:
        return [_state_from_dict(v) for v in self.installs.values() if isinstance(v, dict)]

    def latest(self) -> Optional[InstallState]:
        states = self.all_states()
        if not states:
            return None
        states.sort(key=lambda s: s.installed_at or "", reverse=True)
        return states[0]


@dataclass
class GimpInfo:
    found: bool
    kind: str  # none | native | flatpak | brew | snap | unknown
    binary: Optional[str] = None
    app_path: Optional[str] = None
    version: Optional[str] = None  # e.g. "3.0.4" when probed
    notes: list[str] = field(default_factory=list)

    def label(self) -> str:
        parts = [self.kind]
        if self.version:
            parts.append(f"v{self.version}")
        if self.app_path:
            parts.append(self.app_path)
        elif self.binary:
            parts.append(self.binary)
        if self.notes:
            parts.append("; ".join(self.notes))
        return " — ".join(parts)

    def config_folder_name(self) -> Optional[str]:
        """Map probed version to GIMP user-config folder name (major.minor)."""
        if not self.version:
            return None
        m = re.match(r"^(\d+)\.(\d+)", self.version)
        if not m:
            return None
        return f"{m.group(1)}.{m.group(2)}"


@dataclass
class RecoveryOutcome:
    message: str
    finalized_install: bool = False


# ---------------------------------------------------------------------------
# Platform / GIMP detection
# ---------------------------------------------------------------------------


def is_windows() -> bool:
    return platform.system() == "Windows"


def is_macos() -> bool:
    return platform.system() == "Darwin"


def is_linux() -> bool:
    return platform.system() == "Linux"


def _trusted_system_tool(name: str) -> Optional[str]:
    if is_windows():
        try:
            import ctypes

            buffer = ctypes.create_unicode_buffer(32768)
            length = ctypes.windll.kernel32.GetWindowsDirectoryW(buffer, len(buffer))
            if 0 < length < len(buffer):
                candidate = Path(buffer.value) / "System32" / f"{name}.exe"
                if candidate.is_absolute() and candidate.is_file():
                    return str(candidate.resolve(strict=False))
        except (AttributeError, OSError, ValueError):
            return None
        return None
    for root in (Path("/usr/bin"), Path("/bin")):
        candidate = root / name
        if candidate.is_file():
            return str(candidate)
    return None


def gimp_process_state() -> str:
    """Return running, not-running, or unknown when inspection cannot be trusted."""
    if is_windows():
        tasklist = _trusted_system_tool("tasklist")
        if not tasklist:
            return PROCESS_UNKNOWN
        try:
            result = run([tasklist, "/V", "/FO", "CSV", "/NH"])
            if result.returncode != 0:
                return PROCESS_UNKNOWN
            out = (result.stdout or "").lower()
            if re.search(r'"gimp[^"]*\.exe"', out):
                return PROCESS_RUNNING
            if "gnu image manipulation program" in out:
                return PROCESS_RUNNING
        except OSError:
            return PROCESS_UNKNOWN
        return PROCESS_NOT_RUNNING

    inspected = False
    pgrep = _trusted_system_tool("pgrep")
    for args in (
        ["-x", "gimp"],
        ["-x", "gimp-2.10"],
        ["-x", "gimp-2.99"],
        ["-x", "gimp-3"],
        ["-x", "gimp-3.0"],
        ["-f", "GIMP\\.app/Contents/MacOS/gimp"],
        ["-f", "flatpak run.*org\\.gimp\\.GIMP"],
    ):
        if not pgrep:
            break
        try:
            result = run([pgrep, *args])
            if result.returncode == 0 and (result.stdout or "").strip():
                return PROCESS_RUNNING
            if result.returncode in {0, 1}:
                inspected = True
        except OSError:
            break

    ps = _trusted_system_tool("ps")
    if not ps:
        return PROCESS_NOT_RUNNING if inspected else PROCESS_UNKNOWN
    try:
        result = run([ps, "ax", "-o", "pid=,command="])
    except OSError:
        return PROCESS_NOT_RUNNING if inspected else PROCESS_UNKNOWN
    if result.returncode != 0:
        return PROCESS_NOT_RUNNING if inspected else PROCESS_UNKNOWN
    inspected = True

    for line in (result.stdout or "").splitlines():
        lower = line.lower().strip()
        if not lower or "photogimp_install" in lower:
            continue
        try:
            _pid, command = lower.split(maxsplit=1)
        except ValueError:
            continue
        # Search commands and the shell wrappers that launched them often
        # contain the word "gimp" in arguments; they are not GIMP processes.
        if re.search(r"\b(grep|rg|pgrep)\b", command):
            continue
        executable = command.split(maxsplit=1)[0].strip('"\'')
        basename = Path(executable).name
        if "gimp.app" in executable or executable.startswith("/applications/gimp"):
            return PROCESS_RUNNING
        if "org.gimp.gimp" in command and basename in {
            "flatpak",
            "bwrap",
            "gimp",
            "gimp-3",
            "gimp-3.0",
        }:
            return PROCESS_RUNNING
        # Native binary names: gimp, gimp-3.0, gimp-2.99, gimp-console, ...
        if re.fullmatch(
            r"gimp|gimp-console|gimp-2\.10|gimp-2\.99|gimp-3(?:\.\d+)?",
            basename,
        ):
            return PROCESS_RUNNING
    return PROCESS_NOT_RUNNING if inspected else PROCESS_UNKNOWN


def gimp_process_running() -> bool:
    """Compatibility wrapper for callers that only need a positive match."""
    return gimp_process_state() == PROCESS_RUNNING


def detect_gimp_macos() -> GimpInfo:
    notes: list[str] = []
    apps = sorted(Path("/Applications").glob("GIMP*.app"))
    if apps:
        app = apps[-1]
        binary = app / "Contents" / "MacOS" / "gimp"
        if not binary.is_file() or not os.access(binary, os.X_OK):
            return GimpInfo(
                found=False,
                kind="none",
                notes=[f"Ignoring non-runnable GIMP app bundle: {app}"],
            )
        return GimpInfo(
            found=True,
            kind="native",
            binary=str(binary),
            app_path=str(app),
            notes=notes,
        )

    binary = which("gimp")
    if binary:
        return GimpInfo(found=True, kind="native", binary=binary, notes=notes)

    return GimpInfo(found=False, kind="none", notes=notes)


def detect_all_gimp_windows() -> list[GimpInfo]:
    """Enumerate every Windows GIMP install (2.x and 3.x), not just the first hit."""
    found: list[GimpInfo] = []
    seen_exe: set[str] = set()

    candidates: list[Path] = []
    for env_key in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        base = os.environ.get(env_key)
        if not base:
            continue
        root = Path(base)
        if env_key != "LOCALAPPDATA":
            candidates.extend(root.glob("GIMP*"))
        programs = root / "Programs"
        if programs.is_dir():
            candidates.extend(programs.glob("GIMP*"))

    for path in candidates:
        if not path.is_dir():
            continue
        try:
            exes = list(path.rglob("gimp*.exe"))
        except OSError:
            continue
        for exe in exes:
            name = exe.name.lower()
            if not re.fullmatch(r"gimp(?:-\d+\.\d+)?\.exe", name):
                continue
            # Prefer main GUI binary over console helper when both exist
            if "console" in name:
                continue
            key = str(exe.resolve()) if exe.exists() else str(exe)
            if key in seen_exe:
                continue
            seen_exe.add(key)
            portable_data = _portable_data_dir(exe)
            found.append(
                GimpInfo(
                    found=True,
                    kind="portable" if portable_data else "native",
                    binary=str(exe),
                    app_path=str(path),
                    notes=(
                        [
                            "Portable GIMP — install not supported",
                            f"portable data: {portable_data}",
                        ]
                        if portable_data
                        else [f"Windows install under {path.name}"]
                    ),
                )
            )

    binary = which("gimp")
    if binary:
        key = str(Path(binary).resolve()) if Path(binary).exists() else binary
        if key not in seen_exe:
            exe = Path(binary)
            portable_data = _portable_data_dir(exe)
            if portable_data:
                seen_exe.add(key)
                found.append(
                    GimpInfo(
                        found=True,
                        kind="portable",
                        binary=binary,
                        app_path=str(exe.parent),
                        notes=[
                            "Portable GIMP — install not supported",
                            f"portable data: {portable_data}",
                        ],
                    )
                )
            else:
                seen_exe.add(key)
                found.append(GimpInfo(found=True, kind="native", binary=binary))

    # Portable-style trees: gimp.exe with adjacent Data/ or portable-ish layout
    # outside Program Files — report as unsupported kind, never as installable native
    portable_hits = _detect_windows_portable_candidates(seen_exe)
    found.extend(portable_hits)

    return found


def _detect_windows_portable_candidates(
    seen_exe: set[str], search_roots: Optional[list[Path]] = None
) -> list[GimpInfo]:
    """Find portable-looking GIMP trees; mark kind=portable (install refused)."""
    hits: list[GimpInfo] = []
    if not is_windows():
        return hits
    if search_roots is None:
        search_roots = []
        home = user_home()
        for rel in (
            Path("Downloads"),
            Path("Desktop"),
            Path("Documents"),
            Path("PortableApps"),
            Path("Apps"),
        ):
            search_roots.append(home / rel)
    # Search common user-owned locations only.
    for root in search_roots:
        if not root.is_dir():
            continue
        try:
            for exe in root.glob("**/gimp*.exe"):
                name = exe.name.lower()
                if not name.startswith("gimp") or "unins" in name or "console" in name:
                    continue
                try:
                    key = str(exe.resolve())
                except OSError:
                    key = str(exe)
                if key in seen_exe:
                    continue
                data_dir = _portable_data_dir(exe)
                if not data_dir:
                    continue
                seen_exe.add(key)
                hits.append(
                    GimpInfo(
                        found=True,
                        kind="portable",
                        binary=str(exe),
                        app_path=str(exe.parent),
                        notes=[
                            "Portable GIMP (Data/ next to binary) — install not supported",
                            f"portable data: {data_dir}",
                        ],
                    )
                )
        except OSError:
            continue
    return hits


def _portable_data_dir(exe: Path) -> Optional[Path]:
    """Return a nearby PortableApps-style Data directory, bounded to 4 parents."""
    current = exe.parent
    for _ in range(4):
        candidate = current / "Data"
        if candidate.is_dir():
            return candidate
        if current.parent == current:
            break
        current = current.parent
    return None


def detect_gimp_windows() -> GimpInfo:
    installs = detect_all_gimp_windows()
    natives = [g for g in installs if g.kind != "portable"]
    if natives:
        return natives[0]
    return installs[0] if installs else GimpInfo(found=False, kind="none")


def flatpak_gimp_installed() -> bool:
    return any(
        path.is_dir()
        for path in (
            xdg_data_home() / "flatpak" / "app" / FLATHUB_GIMP_ID,
            Path("/var/lib/flatpak/app") / FLATHUB_GIMP_ID,
        )
    )


def detect_all_gimp_installs() -> list[GimpInfo]:
    """Return every distinct GIMP install we can find (may be empty)."""
    found: list[GimpInfo] = []
    seen: set[tuple[str, str]] = set()

    def add(info: GimpInfo) -> None:
        if not info.found:
            return
        identity = info.binary or info.app_path or info.kind
        if info.binary and info.binary not in {"flatpak", "snap"}:
            try:
                identity = str(Path(info.binary).resolve(strict=False))
            except OSError:
                identity = info.binary
        key = (
            "flatpak" if info.kind == "flatpak" else "snap" if info.kind == "snap" else "binary",
            identity,
        )
        if key in seen:
            return
        seen.add(key)
        found.append(info)

    if is_macos():
        apps = sorted(Path("/Applications").glob("GIMP*.app"))
        for app in apps:
            binary = app / "Contents" / "MacOS" / "gimp"
            if not binary.is_file() or not os.access(binary, os.X_OK):
                continue
            add(
                GimpInfo(
                    found=True,
                    kind="native",
                    binary=str(binary),
                    app_path=str(app),
                )
            )
        binary = which("gimp")
        if binary:
            add(GimpInfo(found=True, kind="native", binary=binary))
    elif is_windows():
        for item in detect_all_gimp_windows():
            add(item)
    elif is_linux():
        if flatpak_gimp_installed():
            flatpak_binary = which("flatpak")
            add(
                GimpInfo(
                    found=True,
                    kind="flatpak",
                    binary=flatpak_binary,
                    notes=["Flatpak app org.gimp.GIMP"],
                )
            )
        for name in ("gimp", "gimp-3", "gimp-3.0", "gimp-2.99"):
            binary = which(name)
            if binary:
                if _is_snap_executable(binary):
                    add(
                        GimpInfo(
                            found=True,
                            kind="snap",
                            binary=binary,
                            notes=["Snap wrapper — install not supported"],
                        )
                    )
                else:
                    add(GimpInfo(found=True, kind="native", binary=binary))
        # Snap: list for status, but install refuses unless explicitly supported later
        snap_cfg = user_home() / "snap" / "gimp" / "current" / ".config" / "GIMP"
        if snap_cfg.parent.parent.is_dir() or Path("/snap/bin/gimp").exists():
            add(
                GimpInfo(
                    found=True,
                    kind="snap",
                    binary="/snap/bin/gimp",
                    notes=[
                        "Snap package 'gimp' (install not supported — use Flatpak/native)",
                        f"config may be under {snap_cfg}",
                    ],
                )
            )
    return found


def _is_snap_executable(binary: str) -> bool:
    normalized = binary.replace("\\", "/")
    if normalized.startswith("/snap/") or normalized.startswith("/var/lib/snapd/"):
        return True
    try:
        resolved = str(Path(binary).resolve(strict=False)).replace("\\", "/")
    except OSError:
        return False
    return resolved.startswith("/snap/") or resolved.startswith("/var/lib/snapd/")


def detect_gimp() -> GimpInfo:
    installs = detect_all_gimp_installs()
    if not installs:
        return GimpInfo(
            found=False,
            kind="none",
            notes=[f"Unsupported OS: {platform.system()}"]
            if platform.system() not in {"Darwin", "Windows", "Linux"}
            else [],
        )
    return installs[0]


def choose_gimp_install(
    installs: list[GimpInfo],
    *,
    for_install: bool = False,
) -> Optional[GimpInfo]:
    """Pick which GIMP install to target when several are present."""
    if not installs:
        return None

    supported = [g for g in installs if g.kind not in UNSUPPORTED_KINDS]
    unsupported = [g for g in installs if g.kind in UNSUPPORTED_KINDS]

    if for_install:
        if unsupported:
            info("Detected but not installable:")
            for g in unsupported:
                info(f"  - {g.label()} [UNSUPPORTED]")
        candidates = supported
    else:
        candidates = list(installs)

    if not candidates:
        error("No installable GIMP found (Snap/Portable are not supported).")
        return None

    if len(candidates) == 1 and not for_install:
        return candidates[0]
    if len(candidates) == 1 and for_install:
        g = candidates[0]
        info(f"Detected one install candidate: {g.label()}")
        if not confirm("Select and probe this exact GIMP candidate?", False):
            info("Cancelled (candidate not selected).")
            return None
        return g

    info("Multiple GIMP installs detected. PhotoGIMP must target one config tree:")
    for i, g in enumerate(candidates, 1):
        tag = ""
        if g.kind in UNSUPPORTED_KINDS:
            tag = " [UNSUPPORTED]"
        info(f"  {i}) {g.label()}{tag}")
    answer = prompt("Choose install number (empty cancels)", "")
    if not answer:
        info("Cancelled (no install selected).")
        return None
    chosen = select_number(answer, candidates)
    if chosen is None:
        error("Invalid selection.")
        return None
    if for_install and chosen.kind in UNSUPPORTED_KINDS:
        error(f"{chosen.kind} GIMP cannot be used for install.")
        return None
    return chosen


def gimp_config_root(gimp: GimpInfo) -> Path:
    if is_windows():
        return _absolute_environment_path(
            "APPDATA", user_home() / "AppData" / "Roaming"
        ) / "GIMP"
    if is_macos():
        return user_home() / "Library" / "Application Support" / "GIMP"
    # Linux
    if gimp.kind == "flatpak":
        return user_home() / ".var" / "app" / FLATHUB_GIMP_ID / "config" / "GIMP"
    if gimp.kind == "snap":
        # Common Snap layout; may vary by channel revision
        return user_home() / "snap" / "gimp" / "current" / ".config" / "GIMP"
    return xdg_config_home() / "GIMP"


def _parse_version_dir(name: str) -> Optional[tuple[int, ...]]:
    if not re.fullmatch(r"\d+\.\d+", name):
        return None
    return tuple(int(x) for x in name.split("."))


def list_version_dirs(config_root: Path, *, min_major: int = 3) -> list[Path]:
    if not config_root.is_dir():
        return []
    versions: list[tuple[tuple[int, ...], Path]] = []
    for child in config_root.iterdir():
        if not child.is_dir():
            continue
        parts = _parse_version_dir(child.name)
        if parts is None:
            continue
        if parts[0] >= min_major:
            versions.append((parts, child))
    versions.sort(key=lambda item: item[0], reverse=True)
    return [path for _, path in versions]


def list_legacy_version_dirs(config_root: Path) -> list[Path]:
    """GIMP 2.x (and other <3) config folders PhotoGIMP cannot use."""
    if not config_root.is_dir():
        return []
    legacy: list[tuple[tuple[int, ...], Path]] = []
    for child in config_root.iterdir():
        if not child.is_dir():
            continue
        parts = _parse_version_dir(child.name)
        if parts is None:
            continue
        if parts[0] < 3:
            legacy.append((parts, child))
    legacy.sort(key=lambda item: item[0], reverse=True)
    return [path for _, path in legacy]


def probe_gimp_version(gimp: GimpInfo) -> Optional[str]:
    """Best-effort version string from the selected install (e.g. '3.0.4')."""
    if gimp.version:
        return gimp.version

    # Flatpak metadata
    if gimp.kind == "flatpak":
        flatpak = which("flatpak")
        if flatpak:
            result = run([flatpak, "info", "--show-version", FLATHUB_GIMP_ID])
            if result.returncode == 0:
                version = (result.stdout or "").strip()
                if re.fullmatch(r"\d+\.\d+(?:\.\d+)?", version):
                    return version

    # CLI --version
    candidates: list[list[str]] = []
    if gimp.kind == "flatpak":
        flatpak = gimp.binary or which("flatpak")
        if flatpak:
            candidates.append(
                [flatpak, "run", "--command=gimp", FLATHUB_GIMP_ID, "--version"]
            )
    elif gimp.binary and gimp.binary not in {"flatpak", "snap"}:
        candidates.append([gimp.binary, "--version"])
    elif which("gimp"):
        candidates.append(["gimp", "--version"])

    for cmd in candidates:
        try:
            result = run(cmd)
        except OSError:
            continue
        if result.returncode != 0:
            continue
        text = (result.stdout or "") + (result.stderr or "")
        m = re.search(
            r"(?:\bGIMP|GNU Image Manipulation Program)(?: version)?\s+"
            r"(\d+\.\d+(?:\.\d+)?)\b",
            text,
            re.I,
        )
        if m:
            return m.group(1)
    return None


def enrich_gimp_version(gimp: GimpInfo) -> GimpInfo:
    ver = probe_gimp_version(gimp)
    if ver and not gimp.version:
        gimp.version = ver
    return gimp


def resolve_config_dir(gimp: GimpInfo, preferred: Optional[str] = None) -> Path:
    """Resolve config dir bound to the selected install when possible.

    Policy (fail-closed for multi-version ambiguity):
    - Prefer probed version → major.minor folder.
    - Only allow folders in SUPPORTED_CONFIG_FOLDERS for install binding.
    - Never silently pick a newer on-disk folder than the probed binary.
    """
    root = gimp_config_root(gimp)
    if preferred:
        parts = _parse_version_dir(preferred)
        if parts is None or parts[0] < 3:
            raise ValueError(
                f"Refusing preferred config version {preferred!r}; PhotoGIMP needs 3.x"
            )
        if preferred not in SUPPORTED_CONFIG_FOLDERS:
            raise ValueError(
                f"Config folder {preferred!r} is not in supported set "
                f"{sorted(SUPPORTED_CONFIG_FOLDERS)} for this PhotoGIMP payload"
            )
        return root / preferred

    gimp = enrich_gimp_version(gimp)
    folder = gimp.config_folder_name()
    if folder:
        if folder not in SUPPORTED_CONFIG_FOLDERS:
            # Still return the path so callers can validate and error clearly
            return root / folder
        return root / folder

    # Unprobed: only safe if exactly one supported folder exists on disk
    existing = [p for p in list_version_dirs(root) if p.name in SUPPORTED_CONFIG_FOLDERS]
    if len(existing) == 1:
        return existing[0]
    # Ambiguous or empty without version: still return payload path so validate can refuse
    return root / PAYLOAD_CONFIG_VERSION


def path_is_within(child: Path, parent: Path) -> bool:
    """True if child is the same as or nested under parent (after resolve)."""
    try:
        child_r = child.resolve()
        parent_r = parent.resolve()
        child_r.relative_to(parent_r)
        return True
    except (ValueError, OSError):
        return False


def validate_path_containment(config_dir: Path, root: Path) -> Optional[str]:
    """Reject symlinks or paths that escape the GIMP config root."""
    if _is_link_or_reparse(root):
        return f"GIMP config root is linked; refusing ambiguous target routing: {root}"
    # Reject profile path that is itself a symlink (writes would follow outside root)
    if config_dir.exists() and _is_link_or_reparse(config_dir):
        try:
            target = config_dir.resolve()
        except OSError as exc:
            return f"Cannot resolve config symlink {config_dir}: {exc}"
        if not path_is_within(target, root):
            return (
                f"Config path is a symlink escaping the GIMP root:\n"
                f"  {config_dir} -> {target}\n"
                f"  expected under {root}\n"
                "Remove or fix the symlink before installing."
            )
        return (
            f"Config path is a symlink ({config_dir} -> {target}). "
            "Refusing to install through profile symlinks; use a real directory."
        )

    try:
        resolved_root = root.expanduser().resolve(strict=False)
        resolved_config = config_dir.expanduser().resolve(strict=False)
        resolved_config.relative_to(resolved_root)
    except ValueError:
        return f"Config path {resolved_config} is outside GIMP root {resolved_root}"
    except OSError as exc:
        return f"Cannot resolve config path {config_dir}: {exc}"
    current = root
    try:
        relative = config_dir.relative_to(root)
    except ValueError:
        return f"Config path {config_dir} is not lexically under GIMP root {root}"
    for part in relative.parts:
        current = current / part
        if _is_link_or_reparse(current):
            return f"Linked profile component is not supported: {current}"
    return None


def validate_gimp3_config_target(gimp: GimpInfo, config_dir: Path) -> Optional[str]:
    """Return an error message if the target is unsafe/wrong for PhotoGIMP."""
    if gimp.kind == "snap":
        return (
            "Snap GIMP is detected but not supported for install. "
            "Use Flatpak (org.gimp.GIMP) or a native package, then re-run."
        )
    if gimp.kind == "portable":
        return (
            "Portable GIMP is not supported. Use an installed GIMP from "
            "Program Files / the official installer, then re-run."
        )

    root = gimp_config_root(gimp)

    try:
        if config_dir.resolve(strict=False) == payload_dir().resolve(strict=False):
            return (
                "Refusing to use the repository payload as the live GIMP profile. "
                "Fix the configured profile root and re-run."
            )
    except OSError as exc:
        return f"Cannot compare target with payload source: {exc}"

    if config_dir.exists() and not config_dir.is_dir() and not _is_link_or_reparse(config_dir):
        return (
            f"Config path exists but is not a directory: {config_dir}. "
            "Remove or rename that path, then re-run."
        )
    if root.exists() and not root.is_dir():
        return f"GIMP config root exists but is not a directory: {root}"
    if os.name == "posix":
        try:
            for owned in (root, config_dir):
                if owned.exists() and owned.lstat().st_uid != os.geteuid():
                    return f"Profile path is not owned by the current user: {owned}"
        except OSError as exc:
            return f"Cannot validate profile ownership: {exc}"

    # Payload compatibility: only supported config folder names
    if config_dir.name not in SUPPORTED_CONFIG_FOLDERS:
        gimp = enrich_gimp_version(gimp)
        return (
            f"PhotoGIMP payload supports config folder(s) "
            f"{sorted(SUPPORTED_CONFIG_FOLDERS)} only; refusing {config_dir.name}. "
            f"Detected GIMP version: {gimp.version or 'unknown'}. "
            "Install/use GIMP 3.0.x, or wait for a matching PhotoGIMP payload."
        )

    # If we know the binary version, it must match the folder
    gimp = enrich_gimp_version(gimp)
    bound = gimp.config_folder_name()
    if bound and bound != config_dir.name:
        return (
            f"Selected GIMP reports version {gimp.version} (config folder {bound}), "
            f"but target is {config_dir}. Refusing mismatched profile."
        )

    # Fail closed: require a successful version probe (no directory-only binding)
    if not gimp.version:
        return (
            "Cannot determine GIMP version for the selected install "
            f"({gimp.binary or gimp.app_path or gimp.kind}). "
            "Refusing to guess a config folder. Ensure the binary is runnable "
            "(e.g. gimp --version), open GIMP once, then re-run. "
            f"Candidate path was {config_dir}."
        )

    containment = validate_path_containment(config_dir, root)
    if containment:
        return containment

    legacy = list_legacy_version_dirs(root)
    modern = list_version_dirs(root)

    if not modern and legacy:
        names = ", ".join(p.name for p in legacy)
        return (
            f"Only GIMP 2.x config folder(s) found under {root} ({names}). "
            "PhotoGIMP requires GIMP 3.0.x and will not install into a 2.x profile. "
            "Install/upgrade to GIMP 3, open it once, then re-run this installer."
        )

    parts = _parse_version_dir(config_dir.name)
    if parts is not None and parts[0] < 3:
        return (
            f"Refusing to use config folder {config_dir} (GIMP {config_dir.name}). "
            "PhotoGIMP only supports GIMP 3.0.x."
        )

    # Require proof GIMP has initialized this profile (not an empty mkdir)
    if config_dir.is_dir():
        marker = config_dir / "gimprc"
        if not marker.is_file():
            return (
                f"Config folder {config_dir} exists but has no gimprc — "
                "GIMP has not finished initializing this profile. "
                "Open the selected GIMP once, fully quit, then re-run."
            )
    return None


def explain_target(gimp: GimpInfo, config_dir: Path) -> None:
    """Print why this config path was chosen for the detected GIMP install."""
    root = gimp_config_root(gimp)
    info("Target binding:")
    info(f"  GIMP kind:     {gimp.kind}")
    if gimp.binary:
        info(f"  GIMP binary:   {gimp.binary}")
    if gimp.app_path:
        info(f"  GIMP app:      {gimp.app_path}")
    info(f"  Config root:   {root}")
    info(f"  Config dir:    {config_dir}")
    if gimp.kind == "flatpak":
        info("  Note: Flatpak GIMP reads ~/.var/app/org.gimp.GIMP/config/GIMP/<ver>/")
        native = user_home() / ".config" / "GIMP"
        if native.is_dir():
            info(f"  Also present:  {native} (native GIMP only — not used for Flatpak)")
    elif is_linux():
        flat = user_home() / ".var" / "app" / FLATHUB_GIMP_ID / "config" / "GIMP"
        if flat.is_dir():
            info(f"  Also present:  {flat} (Flatpak only — not used for native)")


# ---------------------------------------------------------------------------
# GIMP prerequisite
# ---------------------------------------------------------------------------


def open_gimp_download_page() -> None:
    info(f"Official GIMP downloads: {GIMP_DOWNLOAD_URL}")
    info("The installer does not launch browsers or package managers.")


def ensure_gimp_installed() -> Optional[GimpInfo]:
    """Detect an existing GIMP and require explicit candidate selection.

    Returns the chosen GimpInfo, or None if cancelled / still missing.
    """
    installs = detect_all_gimp_installs()
    if not installs:
        info("GIMP was not detected on this system.")
        open_gimp_download_page()
        info("Install GIMP, open it once, fully quit it, then re-run this installer.")
        return GimpInfo(found=False, kind="none")

    chosen = choose_gimp_install(installs, for_install=True)
    if chosen is None:
        info("Cancelled.")
        return None
    return chosen


# ---------------------------------------------------------------------------
# Backup / restore
# ---------------------------------------------------------------------------


def utc_now_stamp() -> str:
    # Microseconds avoid same-second collisions (pre-install + pre-restore, etc.)
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def allocate_backup_dir(config_version: str) -> tuple[str, Path]:
    """Return a unique (backup_id, path) under backups_dir(); never reuses a path."""
    root = backups_dir()
    _reject_symlink_directory(data_home(), "PhotoGIMP data directory")
    _ensure_directory_durable(data_home())
    _reject_symlink_directory(root, "PhotoGIMP backup directory")
    created_root = not root.exists()
    root.mkdir(parents=False, exist_ok=True, mode=0o700)
    _fsync_directory(root.parent)
    if os.name == "posix" and created_root:
        root.chmod(0o700)
    base = f"{config_version}-{utc_now_stamp()}"
    for suffix in range(0, 1000):
        backup_id = base if suffix == 0 else f"{base}-{suffix}"
        dest = root / backup_id
        if dest.exists():
            continue
        try:
            dest.mkdir(parents=False, exist_ok=False, mode=0o700)
            if os.name == "posix":
                dest.chmod(0o700)
            (dest / ".incomplete").write_text("backup in progress\n", encoding="utf-8")
            (dest / BACKUP_PROFILE_DIR).mkdir(mode=0o700)
            (dest / BACKUP_CONTROL_DIR).mkdir(mode=0o700)
            _fsync_directory(dest)
            _fsync_directory(root)
            return backup_id, dest
        except FileExistsError:
            continue
    raise RuntimeError(f"Could not allocate a unique backup directory under {root}")


def create_backup(
    config_dir: Path,
    *,
    reason: str,
    gimp: GimpInfo,
) -> Optional[Path]:
    try:
        with operation_lock("profile", config_dir):
            return _create_backup_locked(config_dir, reason=reason, gimp=gimp)
    except OSError as exc:
        error(f"Cannot create a safe backup: {exc}")
        return None


def _create_backup_locked(
    config_dir: Path,
    *,
    reason: str,
    gimp: GimpInfo,
) -> Optional[Path]:
    if not config_dir.is_dir():
        warn(f"Nothing to back up (missing {config_dir})")
        return None

    try:
        backup_id, dest = allocate_backup_dir(config_dir.name)
    except (OSError, RuntimeError) as exc:
        error(str(exc))
        return None

    info(f"Backing up {config_dir} -> {dest}")
    root_resolved = config_dir.resolve()
    profile = dest / BACKUP_PROFILE_DIR
    control = dest / BACKUP_CONTROL_DIR
    try:
        source_entries = _tree_entries(config_dir)
        _copy_config_tree_safely(config_dir, profile, root_resolved)
        copy_problems = _verify_tree_entries(profile, source_entries)
        if copy_problems:
            raise OSError("Backup copy is not equivalent: " + "; ".join(copy_problems))
        entries = source_entries
    except OSError as exc:
        error(f"Backup copy failed: {exc}")
        shutil.rmtree(dest, ignore_errors=True)
        return None

    meta = {
        "id": backup_id,
        "timestamp": iso_now(),
        "source": str(config_dir.resolve(strict=False)),
        "config_root": str(config_dir.parent.resolve(strict=False)),
        "reason": reason,
        "gimp_kind": gimp.kind,
        "gimp_binary": gimp.binary or "",
        "gimp_app_path": gimp.app_path or "",
        "gimp_version": gimp.version or "",
        "platform": platform.system(),
        "script_version": SCRIPT_VERSION,
        "sealed": True,
        "entry_count": len(entries),
        "format_version": BACKUP_FORMAT_VERSION,
    }
    try:
        meta_path = control / "metadata.json"
        manifest_path = control / "manifest.json"
        meta_path.write_text(
            json.dumps(meta, indent=2) + "\n", encoding="utf-8"
        )
        manifest = {
            "entries": entries,
            "metadata_sha256": file_sha256(meta_path),
            "sealed": True,
            "version": BACKUP_FORMAT_VERSION,
        }
        manifest_path.write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        _fsync_tree(dest)
        (dest / ".incomplete").unlink(missing_ok=True)
        _fsync_directory(dest)
        _fsync_directory(dest.parent)
        # Re-verify seal
        problems = verify_backup_integrity(dest)
        if problems:
            raise OSError("; ".join(problems))
    except OSError as exc:
        error(f"Backup seal failed: {exc}")
        shutil.rmtree(dest, ignore_errors=True)
        return None

    file_count = sum(1 for value in entries.values() if value.get("type") == "file")
    info(f"Backup created: {backup_id} ({file_count} files sealed)")
    return dest


def _copy_config_tree_safely(
    src: Path, dest: Path, root_resolved: Path
) -> None:
    """Copy a profile exactly enough for user-level restore without following links."""
    source_stat = src.lstat()
    if _is_link_or_reparse(src, source_stat):
        raise OSError(f"Linked profile directory is not supported: {src}")
    if os.name == "posix" and source_stat.st_uid != os.geteuid():
        raise OSError(f"Profile entry is not owned by the current user: {src}")
    for item in sorted(src.iterdir(), key=lambda value: value.name):
        target = dest / item.name
        item_stat = item.lstat()
        if _is_link_or_reparse(item, item_stat):
            raise OSError(
                f"Symlink found in GIMP config: {item}. "
                "Refusing an incomplete/non-equivalent backup. Replace the link "
                "with real files or back it up manually."
            )
        if os.name == "posix" and item_stat.st_uid != os.geteuid():
            raise OSError(f"Profile entry is not owned by the current user: {item}")
        if stat.S_ISDIR(item_stat.st_mode):
            target.mkdir(exist_ok=True)
            _copy_config_tree_safely(item, target, root_resolved)
            shutil.copystat(item, target, follow_symlinks=False)
            _copy_xattrs(item, target)
        elif stat.S_ISREG(item_stat.st_mode):
            if not path_is_within(item, root_resolved):
                raise OSError(f"Path escapes config root during backup: {item}")
            shutil.copy2(item, target)
            _copy_xattrs(item, target)
        else:
            raise OSError(f"Unsupported special filesystem entry in profile: {item}")
    shutil.copystat(src, dest, follow_symlinks=False)
    _copy_xattrs(src, dest)


def _copy_xattrs(src: Path, dest: Path) -> None:
    if not all(hasattr(os, name) for name in ("listxattr", "getxattr", "setxattr")):
        return
    try:
        names = os.listxattr(src, follow_symlinks=False)
        for name in names:
            value = os.getxattr(src, name, follow_symlinks=False)
            os.setxattr(dest, name, value, follow_symlinks=False)
    except OSError as exc:
        raise OSError(f"Cannot preserve extended attributes for {src}: {exc}") from exc


def _is_link_or_reparse(path: Path, item_stat: Optional[os.stat_result] = None) -> bool:
    try:
        value = item_stat or path.lstat()
    except FileNotFoundError:
        return False
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(value.st_mode) or bool(
        getattr(value, "st_file_attributes", 0) & reparse_flag
    )


def _entry_metadata(path: Path, root: Path) -> dict:
    item_stat = path.lstat()
    if _is_link_or_reparse(path, item_stat):
        raise OSError(f"Link or reparse point is not supported in a sealed tree: {path}")
    if stat.S_ISDIR(item_stat.st_mode):
        entry_type = "directory"
    elif stat.S_ISREG(item_stat.st_mode):
        entry_type = "file"
    else:
        raise OSError(f"Unsupported special filesystem entry: {path}")
    result = {
        "type": entry_type,
        "mode": stat.S_IMODE(item_stat.st_mode),
        "mtime_ns": item_stat.st_mtime_ns,
    }
    if os.name == "posix":
        result["uid"] = item_stat.st_uid
        result["gid"] = item_stat.st_gid
    if entry_type == "file":
        result["sha256"] = file_sha256(path)
        result["size"] = item_stat.st_size
    if all(hasattr(os, name) for name in ("listxattr", "getxattr")):
        try:
            result["xattrs"] = {
                name: base64.b64encode(
                    os.getxattr(path, name, follow_symlinks=False)
                ).decode("ascii")
                for name in sorted(os.listxattr(path, follow_symlinks=False))
            }
        except OSError as exc:
            raise OSError(f"Cannot inventory extended attributes for {path}: {exc}") from exc
    return result


def _tree_entries(root: Path) -> dict[str, dict]:
    if _is_link_or_reparse(root) or not root.is_dir():
        raise OSError(f"Sealed tree root must be a real directory: {root}")
    entries = {".": _entry_metadata(root, root)}
    for path in sorted(root.rglob("*"), key=lambda value: value.as_posix()):
        rel = path.relative_to(root).as_posix()
        entries[rel] = _entry_metadata(path, root)
    return entries


def _validate_manifest_relpath(rel: str) -> bool:
    if rel == ".":
        return True
    path = Path(rel)
    return bool(rel) and not path.is_absolute() and "." not in path.parts and ".." not in path.parts


def _verify_tree_entries(root: Path, expected: dict) -> list[str]:
    if not isinstance(expected, dict) or "." not in expected:
        return ["backup manifest missing root directory entry"]
    if any(not isinstance(rel, str) or not _validate_manifest_relpath(rel) for rel in expected):
        return ["backup manifest contains an unsafe path"]
    try:
        actual = _tree_entries(root)
    except OSError as exc:
        return [str(exc)]
    problems: list[str] = []
    for rel in sorted(set(expected) - set(actual)):
        problems.append(f"missing sealed entry: {rel}")
    for rel in sorted(set(actual) - set(expected)):
        problems.append(f"unexpected entry in backup: {rel}")
    for rel in sorted(set(expected) & set(actual)):
        wanted = expected[rel]
        found = actual[rel]
        wanted_type = wanted.get("type") if isinstance(wanted, dict) else None
        if not isinstance(wanted_type, str) or wanted_type not in {"file", "directory"}:
            problems.append(f"invalid manifest entry: {rel}")
            continue
        if wanted_type != found.get("type"):
            problems.append(f"entry type mismatch: {rel}")
            continue
        if wanted_type == "file":
            digest = wanted.get("sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                problems.append(f"invalid file digest in manifest: {rel}")
            elif digest != found.get("sha256"):
                problems.append(f"hash mismatch in backup: {rel}")
            if wanted.get("size") != found.get("size"):
                problems.append(f"file size mismatch in backup: {rel}")
        if wanted.get("mode") != found.get("mode"):
            problems.append(f"mode mismatch in backup: {rel}")
        if wanted.get("mtime_ns") != found.get("mtime_ns"):
            problems.append(f"timestamp mismatch in backup: {rel}")
        if os.name == "posix" and (
            wanted.get("uid") != found.get("uid")
            or wanted.get("gid") != found.get("gid")
        ):
            problems.append(f"ownership mismatch in backup: {rel}")
        if wanted.get("xattrs", {}) != found.get("xattrs", {}):
            problems.append(f"extended attribute mismatch in backup: {rel}")
    return problems


def backup_profile_root(backup: Path) -> Path:
    profile = backup / BACKUP_PROFILE_DIR
    control = backup / BACKUP_CONTROL_DIR
    if (
        profile.is_dir()
        and not _is_link_or_reparse(profile)
        and control.is_dir()
        and not _is_link_or_reparse(control)
    ):
        return profile
    return backup


def _load_backup_manifest(backup: Path) -> tuple[int, dict, Path, Path]:
    control = backup / BACKUP_CONTROL_DIR
    if control.is_dir():
        manifest_path = control / "manifest.json"
        meta_path = control / "metadata.json"
    else:
        manifest_path = backup / "backup-manifest.json"
        meta_path = backup / "backup-meta.json"
    if _is_link_or_reparse(manifest_path) or _is_link_or_reparse(meta_path):
        raise OSError("backup control files must not be links")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise OSError("backup manifest root must be an object")
    version = data.get("version")
    if not isinstance(version, int):
        raise OSError("backup manifest missing integer version")
    return version, data, manifest_path, meta_path


def verify_backup_integrity(backup: Path) -> list[str]:
    """Validate exact backup schema and all bytes that restore will consume."""
    if _is_link_or_reparse(backup) or not backup.is_dir():
        return ["backup root must be a real directory"]
    if (backup / ".incomplete").exists():
        return ["incomplete backup"]
    if not (backup / BACKUP_CONTROL_DIR / "manifest.json").is_file() and not (
        backup / "backup-manifest.json"
    ).is_file():
        return ["unsealed backup (no backup-manifest.json)"]
    try:
        version, data, _manifest_path, meta_path = _load_backup_manifest(backup)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid backup manifest: {exc}"]
    problems: list[str] = []
    if data.get("sealed") is not True:
        problems.append("backup manifest is not sealed")
    metadata_digest = data.get("metadata_sha256")
    if not isinstance(metadata_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", metadata_digest):
        problems.append("missing or invalid sealed backup metadata digest")
    elif not meta_path.is_file():
        problems.append("missing sealed backup metadata")
    else:
        try:
            if file_sha256(meta_path) != metadata_digest:
                problems.append("backup metadata hash mismatch")
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            required_meta = {
                "id",
                "timestamp",
                "source",
                "config_root",
                "reason",
                "gimp_kind",
                "gimp_version",
                "platform",
                "script_version",
                "sealed",
            }
            if not isinstance(meta, dict) or not required_meta.issubset(meta):
                problems.append("backup metadata has an invalid schema")
            elif (
                any(
                    not isinstance(meta.get(name), str)
                    for name in required_meta - {"sealed"}
                )
                or meta.get("id") != backup.name
                or meta.get("sealed") is not True
                or not isinstance(meta.get("source"), str)
                or not Path(meta["source"]).is_absolute()
                or Path(meta["source"]).name not in SUPPORTED_CONFIG_FOLDERS
                or meta.get("gimp_kind") not in {"native", "flatpak", "brew"}
                or meta.get("platform") != platform.system()
                or Path(meta["source"]).parent.resolve(strict=False)
                != Path(meta.get("config_root", "")).resolve(strict=False)
            ):
                problems.append("backup metadata identity is invalid")
        except OSError as exc:
            problems.append(f"cannot hash backup metadata: {exc}")
        except json.JSONDecodeError as exc:
            problems.append(f"invalid sealed backup metadata JSON: {exc}")
    if version == BACKUP_FORMAT_VERSION:
        if set(data) != {"version", "sealed", "metadata_sha256", "entries"}:
            problems.append("backup manifest has an invalid version 3 schema")
        entries = data.get("entries")
        problems.extend(_verify_tree_entries(backup / BACKUP_PROFILE_DIR, entries))
        control = backup / BACKUP_CONTROL_DIR
        if _is_link_or_reparse(control) or not control.is_dir():
            problems.append("backup control directory must be a real directory")
        else:
            control_entries = {path.name for path in control.iterdir()}
            if control_entries != {"manifest.json", "metadata.json"}:
                problems.append("backup control directory has unexpected entries")
            for path in control.iterdir():
                if _is_link_or_reparse(path) or not path.is_file():
                    problems.append(f"invalid backup control entry: {path.name}")
        allowed_top = {BACKUP_PROFILE_DIR, BACKUP_CONTROL_DIR}
        extras = {path.name for path in backup.iterdir()} - allowed_top
        if extras:
            problems.append("unexpected backup control entries: " + ", ".join(sorted(extras)))
    elif version == 2:
        files = data.get("files")
        if not isinstance(files, dict):
            problems.append("legacy backup manifest missing files map")
            return problems
        expected: set[str] = set()
        for rel, digest in files.items():
            if not isinstance(rel, str) or not _validate_manifest_relpath(rel) or rel == ".":
                problems.append("legacy backup manifest contains an unsafe path")
                continue
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                problems.append(f"invalid legacy digest: {rel}")
                continue
            expected.add(rel)
            path = backup / rel
            if _is_link_or_reparse(path) or not path.is_file():
                problems.append(f"missing or unsafe sealed file: {rel}")
            elif file_sha256(path) != digest:
                problems.append(f"hash mismatch in backup: {rel}")
        for path in backup.rglob("*"):
            if _is_link_or_reparse(path):
                problems.append(f"symlink in legacy backup: {path.relative_to(backup)}")
            elif path.is_file() and path.parent == backup and path.name in BACKUP_CONTROL_FILES:
                continue
            elif path.is_file() and path.relative_to(backup).as_posix() not in expected:
                problems.append(f"unexpected file in backup: {path.relative_to(backup)}")
    else:
        problems.append(f"unsupported backup format version: {version}")
    return problems


def list_backups() -> list[Path]:
    root = backups_dir()
    if _is_link_or_reparse(root):
        warn(f"Refusing symlinked backup root: {root}")
        return []
    if not root.is_dir():
        return []
    backups = [
        p
        for p in root.iterdir()
        if p.is_dir() and not _is_link_or_reparse(p) and not (p / ".incomplete").exists()
    ]
    backups.sort(key=lambda p: p.name, reverse=True)
    return backups


def read_backup_meta(backup: Path) -> dict:
    new_meta = backup / BACKUP_CONTROL_DIR / "metadata.json"
    meta_path = new_meta if new_meta.is_file() else backup / "backup-meta.json"
    if not meta_path.is_file():
        return {"id": backup.name, "source": "", "reason": "unknown"}
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {
            "id": backup.name,
            "source": "",
            "reason": "unknown",
        }
    except (OSError, json.JSONDecodeError):
        return {"id": backup.name, "source": "", "reason": "unknown"}


def _fsync_directory(path: Path) -> None:
    if os.name == "posix":
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
        return
    if is_windows():
        try:
            import ctypes
            from ctypes import wintypes

            create_file = ctypes.windll.kernel32.CreateFileW
            create_file.restype = wintypes.HANDLE
            create_file.argtypes = [
                wintypes.LPCWSTR,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.LPVOID,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.HANDLE,
            ]
            handle = create_file(
                str(path),
                0x40000000,
                0x00000001 | 0x00000002 | 0x00000004,
                None,
                3,
                0x02000000,
                None,
            )
            invalid = wintypes.HANDLE(-1).value
            if handle == invalid:
                raise ctypes.WinError()
            try:
                if not ctypes.windll.kernel32.FlushFileBuffers(handle):
                    raise ctypes.WinError()
            finally:
                ctypes.windll.kernel32.CloseHandle(handle)
        except (AttributeError, OSError) as exc:
            raise OSError(f"Cannot durably flush directory {path}: {exc}") from exc


def _fsync_file(path: Path) -> None:
    flags = os.O_RDWR if is_windows() else os.O_RDONLY
    restore_mode: Optional[int] = None
    try:
        try:
            fd = os.open(path, flags)
        except PermissionError:
            if not is_windows():
                raise
            restore_mode = stat.S_IMODE(path.stat().st_mode)
            path.chmod(restore_mode | stat.S_IWRITE)
            fd = os.open(path, flags)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        if restore_mode is not None:
            path.chmod(restore_mode)


def _fsync_tree(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        if _is_link_or_reparse(path):
            raise OSError(f"Cannot sync symlinked backup entry: {path}")
        if path.is_file():
            _fsync_file(path)
        elif path.is_dir():
            _fsync_directory(path)
    _fsync_directory(root)


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}-", dir=str(path.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        tmp.replace(path)
        _fsync_directory(path.parent)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def _replace_journal_path(dest: Path) -> Path:
    try:
        canonical = str(dest.resolve(strict=False))
    except (OSError, RuntimeError) as exc:
        raise OSError(f"Cannot resolve replacement target {dest}: {exc}") from exc
    key = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:20]
    return dest.parent / f".photogimp-replace-{key}.json"


def _validate_replace_record(data: dict, dest: Path) -> tuple[Path, Path, Path]:
    if (
        not isinstance(data, dict)
        or data.get("version") != 1
        or data.get("target") != str(dest.resolve(strict=False))
        or not isinstance(data.get("phase"), str)
        or data.get("phase")
        not in {"prepared", "old-moved", "activated", "new-committed"}
    ):
        raise OSError("Replacement journal target does not match requested profile")
    transaction_id = data.get("transaction_id")
    if not isinstance(transaction_id, str) or not re.fullmatch(
        r"[0-9a-f]{32}", transaction_id
    ):
        raise OSError("Replacement journal has an invalid transaction id")
    raw_new = data.get("new_path")
    raw_old = data.get("old_path")
    raw_retired = data.get("retired_path")
    if not all(isinstance(value, str) for value in (raw_new, raw_old, raw_retired)):
        raise OSError("Replacement journal temporary paths must be strings")
    final_tmp = Path(raw_new)
    old_tmp = Path(raw_old)
    retired_tmp = Path(raw_retired)
    parent = dest.parent.resolve(strict=False)
    for candidate, expected_name in (
        (final_tmp, f".photogimp-new-{transaction_id}"),
        (old_tmp, f".photogimp-old-{transaction_id}"),
        (retired_tmp, f".photogimp-retired-{transaction_id}"),
    ):
        if candidate.parent.resolve(strict=False) != parent or candidate.name != expected_name:
            raise OSError("Replacement journal contains an unsafe temporary path")
        if _is_link_or_reparse(candidate):
            raise OSError(f"Replacement temporary path must not be a link: {candidate}")
        if candidate.exists() and not candidate.is_dir():
            raise OSError(f"Replacement temporary path is not a directory: {candidate}")
    return final_tmp, old_tmp, retired_tmp


def _directory_identity(path: Path) -> dict[str, int]:
    item_stat = path.lstat()
    if _is_link_or_reparse(path, item_stat) or not stat.S_ISDIR(item_stat.st_mode):
        raise OSError(f"Expected a real directory for identity check: {path}")
    return {"device": item_stat.st_dev, "inode": item_stat.st_ino}


def _tree_matches(path: Path, entries: object) -> bool:
    return (
        isinstance(entries, dict)
        and path.is_dir()
        and not _is_link_or_reparse(path)
        and not _verify_tree_entries(path, entries)
    )


def recover_replace_transaction(dest: Path) -> Optional[str]:
    journal = _replace_journal_path(dest)
    if _is_link_or_reparse(journal):
        raise OSError(f"Replacement journal must not be a link: {journal}")
    if not journal.is_file():
        return None
    try:
        data = json.loads(journal.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise OSError(f"Invalid replacement journal {journal}: {exc}") from exc
    try:
        final_tmp, old_tmp, retired_tmp = _validate_replace_record(data, dest)
    except (TypeError, ValueError, RuntimeError) as exc:
        raise OSError(f"Invalid replacement journal values: {exc}") from exc
    expected = data.get("expected_entries")
    original = data.get("original_entries")
    new_identity = data.get("new_identity")
    had_dest = data.get("had_dest")
    original_identity = data.get("original_identity")
    if not isinstance(expected, dict) or "." not in expected:
        raise OSError("Replacement journal has invalid expected tree entries")
    if (
        not isinstance(new_identity, dict)
        or not isinstance(new_identity.get("device"), int)
        or not isinstance(new_identity.get("inode"), int)
    ):
        raise OSError("Replacement journal has invalid new directory identity")
    if not isinstance(had_dest, bool):
        raise OSError("Replacement journal has invalid destination state")
    if had_dest:
        if not isinstance(original, dict) or "." not in original:
            raise OSError("Replacement journal has invalid original tree entries")
        if (
            not isinstance(original_identity, dict)
            or not isinstance(original_identity.get("device"), int)
            or not isinstance(original_identity.get("inode"), int)
        ):
            raise OSError("Replacement journal has invalid original directory identity")
    elif original is not None or original_identity is not None:
        raise OSError("Replacement journal records an original for an absent destination")

    if _is_link_or_reparse(dest):
        raise OSError(f"Cannot recover through linked target {dest}")
    final_present = final_tmp.exists()
    old_present = old_tmp.exists()
    retired_present = retired_tmp.exists()
    final_new_identity = (
        final_present and _directory_identity(final_tmp) == new_identity
    )
    if final_present and not (
        final_new_identity or _tree_matches(final_tmp, expected)
    ):
        raise OSError(f"Replacement new tree is missing or changed: {final_tmp}")
    if old_present and (
        not had_dest or _directory_identity(old_tmp) != original_identity
    ):
        raise OSError(f"Replacement old tree identity is not trusted: {old_tmp}")
    if retired_present and (
        not had_dest or _directory_identity(retired_tmp) != original_identity
    ):
        raise OSError(f"Replacement retired tree identity is not trusted: {retired_tmp}")
    if old_present and retired_present:
        raise OSError("Replacement journal has both old and retired original trees")

    phase = data["phase"]
    dest_new_identity = dest.is_dir() and _directory_identity(dest) == new_identity
    dest_original = had_dest and _tree_matches(dest, original)
    dest_original_identity = (
        had_dest and dest.is_dir() and _directory_identity(dest) == original_identity
    )
    old_original = old_present and _tree_matches(old_tmp, original)

    if phase == "new-committed" and dest_new_identity:
        _require_gimp_closed("finalizing replacement recovery")
        if old_present:
            old_tmp.rename(retired_tmp)
            retired_present = True
        _fsync_directory(dest.parent)
        journal.unlink()
        _fsync_directory(dest.parent)
        staged_note = f" Staged tree retained at {final_tmp}." if final_present else ""
        if retired_present:
            return (
                f"Finalized replacement; preserved the displaced profile at {retired_tmp}."
                + staged_note
            )
        return "Finalized a verified replacement profile." + staged_note

    if retired_present:
        raise OSError(
            f"Replacement has a retired original before commit completed: {retired_tmp}"
        )

    if old_present:
        _require_gimp_closed("rolling back replacement recovery")
        preserved_new: Optional[Path] = None
        if not dest.exists():
            old_tmp.rename(dest)
        elif dest_new_identity:
            if final_present:
                raise OSError("Both activated and staged replacement trees are present")
            dest.rename(final_tmp)
            preserved_new = final_tmp
            old_tmp.rename(dest)
        elif dest_original and old_original:
            old_tmp.rename(retired_tmp)
        else:
            raise OSError(
                "Replacement target and preserved original are both present but ambiguous"
            )
        _fsync_directory(dest.parent)
        journal.unlink()
        _fsync_directory(dest.parent)
        retained = preserved_new or (final_tmp if final_present else None)
        retained_note = f" Replacement tree retained at {retained}." if retained else ""
        return (
            "Recovered interrupted tree replacement by restoring the original profile."
            + retained_note
        )

    if phase == "prepared":
        _require_gimp_closed("clearing prepared replacement recovery")
        _fsync_directory(dest.parent)
        journal.unlink()
        _fsync_directory(dest.parent)
        retained_note = f" Staged tree retained at {final_tmp}." if final_present else ""
        return (
            "Cleared an interrupted replacement before the original profile moved."
            + retained_note
        )

    if had_dest and dest_original_identity:
        _require_gimp_closed("finalizing replacement rollback")
        _fsync_directory(dest.parent)
        journal.unlink()
        _fsync_directory(dest.parent)
        retained_note = f" Staged tree retained at {final_tmp}." if final_present else ""
        return "Finalized an interrupted rollback to the original profile." + retained_note

    if not had_dest and (dest_new_identity or not dest.exists()):
        _require_gimp_closed("finalizing replacement of an empty profile")
        _fsync_directory(dest.parent)
        journal.unlink()
        _fsync_directory(dest.parent)
        retained_note = f" Staged tree retained at {final_tmp}." if final_present else ""
        return "Finalized replacement of a previously absent profile." + retained_note

    raise OSError(
        f"Cannot safely recover replacement journal {journal}; preserve it and inspect "
        f"target={dest}, old={old_tmp}, new={final_tmp}."
    )


def replace_tree_atomic(
    src: Path,
    dest: Path,
    *,
    expected_dest_entries: Optional[dict] = None,
    expected_dest_exists: Optional[bool] = None,
) -> None:
    """Replace dest using a durable journal and retain the displaced live tree."""
    if _is_link_or_reparse(dest):
        raise NotADirectoryError(
            f"Refusing to replace linked config path: {dest}. "
            "Use a real directory under the GIMP config root."
        )

    parent = dest.parent
    try:
        resolved_parent = parent.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise NotADirectoryError(f"Cannot resolve replacement parent {parent}: {exc}") from exc
    if parent.absolute() != resolved_parent:
        raise NotADirectoryError(
            f"Refusing replacement through a linked parent path: {parent}"
        )
    parent.mkdir(parents=True, exist_ok=True)
    if _is_link_or_reparse(parent):
        raise NotADirectoryError(f"Replacement parent must be a real directory: {parent}")
    prior_recovery = recover_replace_transaction(dest)
    if prior_recovery:
        info(prior_recovery)
    expected = _tree_entries(src)
    if expected_dest_exists is None:
        had_dest = dest.exists()
        original = _tree_entries(dest) if dest.is_dir() else None
    else:
        had_dest = expected_dest_exists
        original = expected_dest_entries
        if had_dest and not isinstance(original, dict):
            raise OSError("Approved destination snapshot is missing")
        if not had_dest and original is not None:
            raise OSError("Approved absent destination unexpectedly has a snapshot")

    if had_dest:
        approved_problems = _verify_tree_entries(dest, original)
        if approved_problems:
            raise OSError(
                "Destination changed before replacement staging: "
                + "; ".join(approved_problems[:5])
            )
        original_identity = _directory_identity(dest)
    else:
        if dest.exists():
            raise OSError("Destination appeared before replacement staging")
        original_identity = None

    transaction_id = secrets.token_hex(16)
    final_tmp = parent / f".photogimp-new-{transaction_id}"
    old_tmp = parent / f".photogimp-old-{transaction_id}"
    retired_tmp = parent / f".photogimp-retired-{transaction_id}"

    with tempfile.TemporaryDirectory(dir=str(parent), prefix=".photogimp-tmp-") as tmp:
        staged = Path(tmp) / "tree"
        shutil.copytree(src, staged, symlinks=True)
        stage_problems = _verify_tree_entries(staged, expected)
        if stage_problems:
            raise OSError("Staged tree verification failed: " + "; ".join(stage_problems))
        # Move staged out of the TemporaryDirectory before it is cleaned up
        staged.rename(final_tmp)
    _fsync_tree(final_tmp)
    _fsync_directory(parent)
    new_identity = _directory_identity(final_tmp)

    journal = _replace_journal_path(dest)
    record = {
        "version": 1,
        "transaction_id": transaction_id,
        "target": str(dest.resolve(strict=False)),
        "new_path": str(final_tmp.resolve(strict=False)),
        "old_path": str(old_tmp.resolve(strict=False)),
        "retired_path": str(retired_tmp.resolve(strict=False)),
        "had_dest": had_dest,
        "phase": "prepared",
        "expected_entries": expected,
        "new_identity": new_identity,
        "original_entries": original,
        "original_identity": original_identity,
        "created_at": iso_now(),
    }
    _atomic_write_json(journal, record)
    try:
        _require_gimp_closed("committing profile replacement")
        if had_dest:
            current_problems = _verify_tree_entries(dest, original)
            if current_problems or _directory_identity(dest) != original_identity:
                raise OSError(
                    "Destination changed immediately before replacement: "
                    + "; ".join(current_problems[:5])
                )
            dest.rename(old_tmp)
            record["phase"] = "old-moved"
            _atomic_write_json(journal, record)
            _fsync_directory(parent)
            moved_problems = _verify_tree_entries(old_tmp, original)
            if moved_problems or _directory_identity(old_tmp) != original_identity:
                raise OSError(
                    "Original profile changed while replacement began: "
                    + "; ".join(moved_problems[:5])
                )
        elif dest.exists():
            raise OSError("Destination appeared immediately before replacement")
        final_tmp.rename(dest)
        record["phase"] = "activated"
        _atomic_write_json(journal, record)
        _fsync_directory(parent)
        final_problems = _verify_tree_entries(dest, expected)
        if final_problems:
            raise OSError("Activated tree verification failed: " + "; ".join(final_problems))
        _fsync_tree(dest)
        record["phase"] = "new-committed"
        _atomic_write_json(journal, record)
        if old_tmp.exists():
            _require_gimp_closed("preserving the displaced original profile")
            if _directory_identity(old_tmp) != original_identity:
                raise OSError("Original profile identity changed during replacement")
            old_tmp.rename(retired_tmp)
            warn(f"Preserved the displaced profile at {retired_tmp}")
        _fsync_directory(parent)
        journal.unlink()
        _fsync_directory(parent)
    except BaseException:
        try:
            recover_replace_transaction(dest)
        except OSError as recovery_error:
            error(f"Automatic replacement rollback failed: {recovery_error}")
        raise


def _legacy_stage_ignore(source_root: Path):
    source_resolved = source_root.resolve(strict=False)

    def ignore(directory: str, names: list[str]) -> set[str]:
        if Path(directory).resolve(strict=False) != source_resolved:
            return set()
        return set(names) & (set(BACKUP_CONTROL_FILES) | {JOURNAL_NAME, ".incomplete"})

    return ignore


def _verify_tree_against_backup(tree: Path, backup: Path) -> list[str]:
    try:
        version, data, _manifest_path, _meta_path = _load_backup_manifest(backup)
    except (OSError, json.JSONDecodeError) as exc:
        return [str(exc)]
    if version == BACKUP_FORMAT_VERSION:
        return _verify_tree_entries(tree, data.get("entries"))
    if version != 2:
        return [f"unsupported backup format version: {version}"]
    files = data.get("files") or {}
    try:
        actual_entries = _tree_entries(tree)
    except OSError as exc:
        return [str(exc)]
    actual_files = {
        rel for rel, value in actual_entries.items() if value.get("type") == "file"
    }
    expected_files = set(files)
    problems: list[str] = []
    for rel in sorted(expected_files - actual_files):
        problems.append(f"missing restored file: {rel}")
    for rel in sorted(actual_files - expected_files):
        problems.append(f"unexpected restored file: {rel}")
    for rel in sorted(expected_files & actual_files):
        if file_sha256(tree / rel) != files[rel]:
            problems.append(f"restored hash mismatch: {rel}")
    return problems


def _stage_verified_backup(backup: Path, parent: Path) -> Path:
    stage_root = Path(tempfile.mkdtemp(prefix=".photogimp-restore-stage-", dir=str(parent)))
    staged = stage_root / "profile"
    source = backup_profile_root(backup)
    try:
        ignore = _legacy_stage_ignore(source) if source == backup else None
        shutil.copytree(source, staged, symlinks=True, ignore=ignore)
        problems = _verify_tree_against_backup(staged, backup)
        if problems:
            raise OSError("Staged backup verification failed: " + "; ".join(problems))
        return staged
    except BaseException:
        shutil.rmtree(stage_root, ignore_errors=True)
        raise


def gimp_info_from_backup_meta(meta: dict) -> GimpInfo:
    """Rebuild a GimpInfo for safety-backup / path binding from backup metadata."""
    kind = meta.get("gimp_kind") or "native"
    return GimpInfo(
        found=True,
        kind=kind,
        binary=meta.get("gimp_binary") or None,
        app_path=meta.get("gimp_app_path") or None,
        version=meta.get("gimp_version") or None,
        notes=["from backup metadata"],
    )


def restore_backup(
    backup: Path,
    config_dir: Path,
    *,
    gimp: Optional[GimpInfo] = None,
    allow_unsealed: bool = False,
) -> None:
    with operation_lock("profile", config_dir):
        _restore_backup_locked(
            backup,
            config_dir,
            gimp=gimp,
            allow_unsealed=allow_unsealed,
        )


def _restore_backup_locked(
    backup: Path,
    config_dir: Path,
    *,
    gimp: Optional[GimpInfo] = None,
    allow_unsealed: bool = False,
) -> None:
    if not backup.is_dir():
        raise FileNotFoundError(f"Backup not found: {backup}")

    if config_dir.exists() and not config_dir.is_dir():
        raise NotADirectoryError(
            f"Config path exists but is not a directory: {config_dir}"
        )

    seal_problems = verify_backup_integrity(backup)
    if seal_problems:
        raise OSError("Backup failed integrity check: " + "; ".join(seal_problems))

    parent = config_dir.parent
    parent.mkdir(parents=True, exist_ok=True)

    # Safety copy of *this* target config, using the caller's GimpInfo when known
    if gimp is None:
        meta = read_backup_meta(backup)
        gimp = gimp_info_from_backup_meta(meta)

    containment = validate_path_containment(config_dir, gimp_config_root(gimp))
    if containment:
        raise OSError(containment)

    live_entries = _tree_entries(config_dir) if config_dir.is_dir() else None
    if config_dir.is_dir() and any(
        p.name not in {JOURNAL_NAME} for p in config_dir.iterdir()
    ):
        safety = create_backup(config_dir, reason="pre-restore", gimp=gimp)
        if safety is None:
            raise OSError(
                "Required pre-restore safety backup failed; aborting without changes."
            )

    if gimp_process_state() != PROCESS_NOT_RUNNING:
        raise OSError("GIMP process state changed before restore; refusing mutation")
    if live_entries is not None:
        live_problems = _verify_tree_entries(config_dir, live_entries)
        if live_problems:
            raise OSError(
                "Profile changed after the restore safety snapshot; refusing replacement: "
                + "; ".join(live_problems[:5])
            )
    info(f"Restoring {backup.name} -> {config_dir}")
    _replace_from_verified_backup(
        backup,
        config_dir,
        expected_dest_entries=live_entries,
        expected_dest_exists=live_entries is not None,
    )
    info("Restore complete.")


# ---------------------------------------------------------------------------
# Payload install
# ---------------------------------------------------------------------------


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_payload_manifest(gimp: GimpInfo) -> dict[str, str]:
    """Relative path → sha256 for every file this install will write."""
    source = ensure_payload()
    contract = validate_payload_contract(source)
    result: dict[str, str] = {}
    for rel, entry in contract["payload"].items():
        policy = entry["policy"]
        if policy == "install" or (policy == "flatpak" and gimp.kind == "flatpak"):
            result[rel] = entry["sha256"]
    return result


def validate_payload_contract(source: Optional[Path] = None) -> dict:
    """Validate the source tree against an independent exact inventory and hashes."""
    root = source or payload_dir()
    manifest_path = payload_manifest_path()
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Authoritative payload manifest missing: {manifest_path}")
    try:
        contract = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FileNotFoundError(f"Invalid payload manifest {manifest_path}: {exc}") from exc
    if (
        not isinstance(contract, dict)
        or contract.get("version") != 1
        or contract.get("config_version") != PAYLOAD_CONFIG_VERSION
        or not isinstance(contract.get("payload"), dict)
        or not isinstance(contract.get("branding"), dict)
    ):
        raise FileNotFoundError("Payload manifest has an unsupported schema")
    expected = contract["payload"]
    for rel, entry in expected.items():
        if not isinstance(rel, str) or not _validate_manifest_relpath(rel) or rel == ".":
            raise FileNotFoundError(f"Unsafe path in payload manifest: {rel!r}")
        if not isinstance(entry, dict) or entry.get("policy") not in {
            "install",
            "flatpak",
            "excluded",
        }:
            raise FileNotFoundError(f"Invalid payload policy for {rel}")
        digest = entry.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise FileNotFoundError(f"Invalid payload digest for {rel}")
        if any(rel.startswith(prefix) for prefix in PAYLOAD_EXCLUSIONS):
            if entry["policy"] != "excluded":
                raise FileNotFoundError(f"Author-generated state must remain excluded: {rel}")
        elif rel == "theme.css":
            if entry["policy"] != "flatpak":
                raise FileNotFoundError("theme.css must remain Flatpak-only")
        elif rel in CORE_FILES or any(rel.startswith(name + "/") for name in CORE_DIRS):
            if entry["policy"] != "install":
                raise FileNotFoundError(f"Required PhotoGIMP payload must be installed: {rel}")
    actual: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if _is_link_or_reparse(path):
            raise FileNotFoundError(f"Payload must not contain symlinks: {path}")
        if path.is_file():
            actual[path.relative_to(root).as_posix()] = file_sha256(path)
        elif not path.is_dir():
            raise FileNotFoundError(f"Payload contains unsupported entry: {path}")
    missing = sorted(set(expected) - set(actual))
    unknown = sorted(set(actual) - set(expected))
    changed = sorted(rel for rel in set(actual) & set(expected) if actual[rel] != expected[rel]["sha256"])
    if missing or unknown or changed:
        raise FileNotFoundError(
            "Payload does not match the authoritative manifest: "
            f"missing={missing}, unexpected={unknown}, hash_mismatch={changed}"
        )
    install_entries = {rel for rel, entry in expected.items() if entry["policy"] == "install"}
    for required in CORE_FILES:
        if required not in install_entries:
            raise FileNotFoundError(f"Required payload file not install-managed: {required}")
    for directory in CORE_DIRS:
        if not any(rel.startswith(directory + "/") for rel in install_entries):
            raise FileNotFoundError(f"Required payload directory has no managed files: {directory}/")
    branding_expected = contract["branding"]
    branding_root = linux_branding_root()
    if any(
        not isinstance(rel, str)
        or not _validate_manifest_relpath(rel)
        or not isinstance(digest, str)
        or not re.fullmatch(r"[0-9a-f]{64}", digest)
        for rel, digest in branding_expected.items()
    ):
        raise FileNotFoundError("Branding manifest contains an invalid entry")
    branding_actual: dict[str, str] = {}
    for path in sorted(branding_root.rglob("*")):
        if _is_link_or_reparse(path) or (not path.is_file() and not path.is_dir()):
            raise FileNotFoundError(f"Branding payload contains an unsafe entry: {path}")
        if path.is_file():
            branding_actual[path.relative_to(branding_root).as_posix()] = file_sha256(path)
    if branding_actual != branding_expected:
        missing_branding = sorted(set(branding_expected) - set(branding_actual))
        extra_branding = sorted(set(branding_actual) - set(branding_expected))
        changed_branding = sorted(
            rel
            for rel in set(branding_actual) & set(branding_expected)
            if branding_actual[rel] != branding_expected[rel]
        )
        raise FileNotFoundError(
            "Branding payload does not match the authoritative manifest: "
            f"missing={missing_branding}, unexpected={extra_branding}, "
            f"hash_mismatch={changed_branding}"
        )
    return contract


def ensure_payload() -> Path:
    path = payload_dir()
    if not path.is_dir():
        raise FileNotFoundError(
            f"PhotoGIMP payload not found at {path}. "
            "Run this script from a full PhotoGIMP source tree or release extract."
        )
    missing = [name for name in CORE_FILES if not (path / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Payload incomplete; missing: {', '.join(missing)}")
    for name in CORE_DIRS:
        if not (path / name).is_dir():
            raise FileNotFoundError(f"Payload incomplete; missing directory {name}/")
    validate_payload_contract(path)
    return path


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".photogimp-", dir=str(dest.parent))
    os.close(fd)
    tmp_path = Path(tmp_name)
    try:
        shutil.copy2(src, tmp_path)
        _fsync_file(tmp_path)
        tmp_path.replace(dest)
        _fsync_directory(dest.parent)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def copy_tree(src: Path, dest: Path) -> None:
    replace_tree_atomic(src, dest)


def write_install_journal(
    config_dir: Path,
    *,
    backup_id: str,
    tops: list[str],
    phase: str,
    installed_hashes: Optional[dict[str, str]] = None,
    baseline_backup_id: str = "",
    gimp: Optional[GimpInfo] = None,
) -> None:
    if phase not in {"prepared", "activating", "committing", "committed"}:
        raise ValueError(f"Invalid journal phase: {phase}")
    if backup_id and (Path(backup_id).name != backup_id or "/" in backup_id or "\\" in backup_id):
        raise ValueError("Invalid journal backup id")
    if baseline_backup_id and (
        Path(baseline_backup_id).name != baseline_backup_id
        or "/" in baseline_backup_id
        or "\\" in baseline_backup_id
    ):
        raise ValueError("Invalid journal baseline backup id")
    if not tops or any(top not in MANAGED_TOPS for top in tops):
        raise ValueError("Invalid journal managed items")
    hashes = installed_hashes or {}
    if any(
        not safe_managed_relative_path(rel)
        or not isinstance(digest, str)
        or not re.fullmatch(r"[0-9a-f]{64}", digest)
        for rel, digest in hashes.items()
    ):
        raise ValueError("Invalid journal installed hashes")
    payload = {
        "phase": phase,
        "backup_id": backup_id,
        "baseline_backup_id": baseline_backup_id or backup_id,
        "config_path": str(config_dir.resolve(strict=False)),
        "tops": tops,
        "installed_hashes": hashes,
        "started_at": iso_now(),
        "script_version": SCRIPT_VERSION,
        "gimp_kind": gimp.kind if gimp else "",
        "gimp_binary": (gimp.binary or "") if gimp else "",
        "gimp_app_path": (gimp.app_path or "") if gimp else "",
        "gimp_version": (gimp.version or "") if gimp else "",
    }
    path = journal_path(config_dir)
    _reject_symlink_directory(data_home(), "PhotoGIMP data directory")
    _ensure_directory_durable(data_home())
    _reject_symlink_directory(path.parent, "PhotoGIMP transaction directory")
    _ensure_directory_durable(path.parent)
    _atomic_write_json(path, payload)


def clear_install_journal(config_dir: Path) -> None:
    for path in (journal_path(config_dir), legacy_journal_path(config_dir)):
        if path.is_file():
            path.unlink(missing_ok=True)
            _fsync_directory(path.parent)


def _load_install_journal(config_dir: Path) -> dict:
    path = journal_path(config_dir)
    if not path.is_file() and legacy_journal_path(config_dir).is_file():
        path = legacy_journal_path(config_dir)
    if _is_link_or_reparse(path):
        raise OSError(f"Install journal must not be a link: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise OSError(f"Invalid install journal {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise OSError(f"Invalid install journal schema: {path}")
    phase = data.get("phase")
    backup_id = data.get("backup_id", "")
    baseline_backup_id = data.get("baseline_backup_id", backup_id)
    tops = data.get("tops")
    hashes = data.get("installed_hashes", {})
    if phase not in {"prepared", "activating", "committing", "committed"}:
        raise OSError(f"Invalid install journal phase: {phase!r}")
    if not isinstance(backup_id, str) or (
        backup_id
        and (Path(backup_id).name != backup_id or "/" in backup_id or "\\" in backup_id)
    ):
        raise OSError("Invalid install journal backup id")
    if not isinstance(baseline_backup_id, str) or (
        baseline_backup_id
        and (
            Path(baseline_backup_id).name != baseline_backup_id
            or "/" in baseline_backup_id
            or "\\" in baseline_backup_id
        )
    ):
        raise OSError("Invalid install journal baseline backup id")
    recorded_config = data.get("config_path")
    if recorded_config is not None:
        if (
            not isinstance(recorded_config, str)
            or not recorded_config
            or Path(recorded_config).resolve(strict=False)
            != config_dir.resolve(strict=False)
        ):
            raise OSError("Install journal belongs to a different config path")
    if not isinstance(tops, list) or not tops or any(
        not isinstance(top, str) or top not in MANAGED_TOPS for top in tops
    ):
        raise OSError("Invalid install journal managed items")
    if not isinstance(hashes, dict) or any(
        not isinstance(rel, str)
        or not safe_managed_relative_path(rel)
        or not isinstance(digest, str)
        or not re.fullmatch(r"[0-9a-f]{64}", digest)
        for rel, digest in hashes.items()
    ):
        raise OSError("Invalid install journal installed hashes")
    return data


def _backup_from_id(backup_id: str) -> Path:
    if not backup_id or Path(backup_id).name != backup_id or "/" in backup_id or "\\" in backup_id:
        raise OSError("Invalid backup id")
    raw_root = backups_dir()
    if _is_link_or_reparse(raw_root):
        raise OSError(f"Backup root must not be a link: {raw_root}")
    root = raw_root.resolve()
    candidate = (root / backup_id).resolve()
    if candidate.parent != root:
        raise OSError("Backup id escapes backup root")
    return candidate


def _replace_from_verified_backup(
    backup: Path,
    config_dir: Path,
    *,
    expected_dest_entries: Optional[dict] = None,
    expected_dest_exists: Optional[bool] = None,
) -> None:
    problems = verify_backup_integrity(backup)
    if problems:
        raise OSError("Backup failed integrity check: " + "; ".join(problems))
    staged = _stage_verified_backup(backup, config_dir.parent)
    stage_root = staged.parent
    try:
        replace_tree_atomic(
            staged,
            config_dir,
            expected_dest_entries=expected_dest_entries,
            expected_dest_exists=expected_dest_exists,
        )
        final_problems = _verify_tree_against_backup(config_dir, backup)
        if final_problems:
            raise OSError(
                "Final restored tree verification failed: "
                + "; ".join(final_problems)
            )
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)


def recover_incomplete_install(config_dir: Path) -> Optional[RecoveryOutcome]:
    """If a prior install was interrupted, restore from journal backup.

    Returns a human message if recovery ran, else None.
    """
    path = journal_path(config_dir)
    if not path.is_file() and not legacy_journal_path(config_dir).is_file():
        return None
    data = _load_install_journal(config_dir)

    backup_id = data.get("backup_id") or ""
    phase = data.get("phase") or "unknown"
    info(f"Found incomplete install journal (phase={phase}).")
    if phase == "prepared":
        clear_install_journal(config_dir)
        return RecoveryOutcome(
            "Cleared a pre-activation install journal; current profile changes were preserved."
        )

    # Activation may have completed before the durable phase update.
    if phase in {"activating", "committed"}:
        hashes = data.get("installed_hashes") or {}
        if hashes:
            meta = read_backup_meta(_backup_from_id(backup_id)) if backup_id else {}
            st = InstallRegistry.load().get(str(config_dir))
            gimp = GimpInfo(
                found=True,
                kind=(meta.get("gimp_kind") or (st.gimp_kind if st else "native")),
                binary=(meta.get("gimp_binary") or (st.gimp_binary if st else None)),
                version=(meta.get("gimp_version") or (st.gimp_version if st else None)),
            )
            problems = verify_install(config_dir, hashes, gimp)
            if not problems:
                baseline_id = data.get("baseline_backup_id") or backup_id
                if not baseline_id:
                    raise OSError("Committed install journal has no uninstall baseline")
                baseline = _backup_from_id(baseline_id)
                baseline_problems = verify_backup_integrity(baseline)
                if baseline_problems or not _backup_matches_config(baseline, config_dir):
                    raise OSError(
                        "Committed install baseline is invalid or belongs to another profile: "
                        + "; ".join(baseline_problems)
                    )
                registry = InstallRegistry.load()
                if registry.errors:
                    raise OSError("Cannot finalize install into an invalid registry")
                registry.upsert(
                    InstallState(
                        backup_id=baseline_id,
                        config_path=str(config_dir.resolve(strict=False)),
                        installed_at=iso_now(),
                        config_version=config_dir.name,
                        platform=platform.system(),
                        gimp_kind=data.get("gimp_kind") or gimp.kind,
                        gimp_binary=data.get("gimp_binary") or gimp.binary or "",
                        gimp_app_path=data.get("gimp_app_path") or "",
                        gimp_version=data.get("gimp_version") or gimp.version or "",
                        installed_hashes=hashes,
                    )
                )
                clear_install_journal(config_dir)
                return RecoveryOutcome(
                    "Finalized a previously committed install and preserved its "
                    "original uninstall baseline.",
                    finalized_install=True,
                )
        if backup_id:
            backup = _backup_from_id(backup_id)
            backup_problems = verify_backup_integrity(backup)
            if backup_problems or not _backup_matches_config(backup, config_dir):
                raise OSError(
                    "Install recovery backup is invalid or belongs to another profile: "
                    + "; ".join(backup_problems)
                )
            live_problems = _verify_tree_against_backup(config_dir, backup)
            if not live_problems:
                clear_install_journal(config_dir)
                return RecoveryOutcome(
                    "Confirmed the interrupted activation had already rolled back to its backup."
                )
        raise OSError(
            "Interrupted install target matches neither the sealed backup nor the committed "
            "payload. Refusing to overwrite ambiguous concurrent changes; journal retained."
        )

    # Version 1.1 and older used "committing" while replacing files in place.
    if backup_id:
        backup = _backup_from_id(backup_id)
        if backup.is_dir():
            if not _backup_matches_config(backup, config_dir):
                raise OSError(
                    f"Recovery backup {backup_id!r} belongs to a different profile"
                )
            _require_gimp_closed("restoring an interrupted legacy install")
            live_entries = _tree_entries(config_dir) if config_dir.is_dir() else None
            if config_dir.is_dir() and any(config_dir.iterdir()):
                recovery_gimp = GimpInfo(
                    found=True,
                    kind=data.get("gimp_kind") or "native",
                    binary=data.get("gimp_binary") or None,
                    app_path=data.get("gimp_app_path") or None,
                    version=data.get("gimp_version") or None,
                )
                safety = create_backup(
                    config_dir,
                    reason="pre-recovery-legacy-install",
                    gimp=recovery_gimp,
                )
                if safety is None:
                    raise OSError(
                        "Cannot preserve the current profile before legacy install recovery"
                    )
            _require_gimp_closed("committing interrupted legacy install recovery")
            if live_entries is not None:
                live_problems = _verify_tree_entries(config_dir, live_entries)
                if live_problems:
                    raise OSError(
                        "Profile changed during legacy install recovery: "
                        + "; ".join(live_problems[:5])
                    )
            info(f"Recovering by restoring backup {backup_id}...")
            try:
                _replace_from_verified_backup(
                    backup,
                    config_dir,
                    expected_dest_entries=live_entries,
                    expected_dest_exists=live_entries is not None,
                )
                clear_install_journal(config_dir)
                return RecoveryOutcome(
                    f"Recovered incomplete install using backup {backup_id}."
                )
            except OSError as exc:
                raise OSError(
                    f"Recovery failed: {exc}. Manual restore from {backup}."
                ) from exc
        raise OSError(
            f"Incomplete install journal present but backup {backup_id!r} missing. "
            f"Inspect {config_dir}."
        )
    # A legacy empty-profile journal has no independent hashes that distinguish
    # installer output from concurrent user work. Only clear it when no managed
    # artifacts exist; otherwise retain everything for explicit inspection.
    remaining = [
        str(config_dir / top)
        for top in data.get("tops") or []
        if (config_dir / top).exists()
    ]
    if remaining:
        raise OSError(
            "Legacy empty-profile recovery is ambiguous; no files were removed. "
            "Inspect these managed paths and the retained journal: " + ", ".join(remaining)
        )
    clear_install_journal(config_dir)
    return RecoveryOutcome("Cleared an empty legacy journal with no managed artifacts.")


def install_payload(
    config_dir: Path,
    gimp: GimpInfo,
    *,
    backup_id: str = "",
    baseline_backup_id: str = "",
) -> dict[str, str]:
    """Build a complete verified profile from the sealed backup, then atomically replace."""
    if config_dir.exists() and not config_dir.is_dir():
        raise NotADirectoryError(
            f"Config path exists but is not a directory: {config_dir}"
        )

    source = ensure_payload()
    manifest = build_payload_manifest(gimp)
    approved_dest_exists = config_dir.is_dir()
    approved_dest_entries: Optional[dict] = None
    config_dir.parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(
        tempfile.mkdtemp(prefix=".photogimp-install-stage-", dir=str(config_dir.parent))
    )
    stage = stage_root / "profile"
    if backup_id:
        backup = _backup_from_id(backup_id)
        problems = verify_backup_integrity(backup)
        if problems:
            shutil.rmtree(stage_root, ignore_errors=True)
            raise OSError("Install backup failed integrity check: " + "; ".join(problems))
        if not _backup_matches_config(backup, config_dir):
            shutil.rmtree(stage_root, ignore_errors=True)
            raise OSError("Install backup belongs to a different profile")
        version, backup_manifest, _manifest_path, _meta_path = _load_backup_manifest(backup)
        if version != BACKUP_FORMAT_VERSION or not isinstance(
            backup_manifest.get("entries"), dict
        ):
            shutil.rmtree(stage_root, ignore_errors=True)
            raise OSError("Install transaction requires a format v3 exact backup")
        approved_dest_entries = backup_manifest["entries"]
        if config_dir.is_dir():
            live_problems = _verify_tree_against_backup(config_dir, backup)
            if live_problems:
                shutil.rmtree(stage_root, ignore_errors=True)
                raise OSError(
                    "Profile changed after backup; refusing to overwrite concurrent changes: "
                    + "; ".join(live_problems[:5])
                )
        staged_backup = _stage_verified_backup(backup, config_dir.parent)
        shutil.move(str(staged_backup), str(stage))
        shutil.rmtree(staged_backup.parent, ignore_errors=True)
    else:
        if config_dir.is_dir() and any(config_dir.iterdir()):
            shutil.rmtree(stage_root, ignore_errors=True)
            raise OSError("Refusing to install into a nonempty profile without a sealed backup")
        if config_dir.is_dir():
            approved_dest_entries = _tree_entries(config_dir)
        stage.mkdir()

    tops: list[str] = []
    for rel in manifest:
        top = rel.split("/", 1)[0]
        if top not in tops:
            tops.append(top)

    try:
        for rel, _digest in manifest.items():
            src = source / rel
            dest = stage / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

        for rel, digest in manifest.items():
            staged = stage / rel
            if not staged.is_file():
                raise OSError(f"Staging missing {rel}")
            if file_sha256(staged) != digest:
                raise OSError(f"Staging hash mismatch for {rel}")

        write_install_journal(
            config_dir,
            backup_id=backup_id,
            baseline_backup_id=baseline_backup_id,
            tops=tops,
            phase="prepared",
            installed_hashes=manifest,
            gimp=gimp,
        )

        if backup_id and config_dir.is_dir():
            process_state = gimp_process_state()
            if process_state != PROCESS_NOT_RUNNING:
                raise OSError(
                    f"GIMP process state became {process_state!r} before commit; "
                    "refusing profile replacement"
                )
            backup = _backup_from_id(backup_id)
            live_problems = _verify_tree_against_backup(config_dir, backup)
            if live_problems:
                raise OSError(
                    "Profile changed immediately before commit; refusing replacement: "
                    + "; ".join(live_problems[:5])
                )
        write_install_journal(
            config_dir,
            backup_id=backup_id,
            baseline_backup_id=baseline_backup_id,
            tops=tops,
            phase="activating",
            installed_hashes=manifest,
            gimp=gimp,
        )
        replace_tree_atomic(
            stage,
            config_dir,
            expected_dest_entries=approved_dest_entries,
            expected_dest_exists=approved_dest_exists,
        )

        write_install_journal(
            config_dir,
            backup_id=backup_id,
            baseline_backup_id=baseline_backup_id,
            tops=tops,
            phase="committed",
            installed_hashes=manifest,
            gimp=gimp,
        )
        info(f"  committed {len(tops)} top-level items ({len(manifest)} files)")
    except BaseException:
        # Leave journal for recovery; stage cleaned below
        raise
    finally:
        if stage_root.exists():
            shutil.rmtree(stage_root, ignore_errors=True)

    # Commit finished; caller still runs hash verify. Journal phase=committed means
    # recovery should prefer verify-OK over blind rollback.
    return manifest


def verify_install(
    config_dir: Path,
    expected_hashes: dict[str, str],
    gimp: GimpInfo,
) -> list[str]:
    """Return list of verification problems (empty means OK)."""
    problems: list[str] = []
    if not config_dir.is_dir():
        return [f"config dir missing after install: {config_dir}"]

    for rel, digest in expected_hashes.items():
        path = config_dir / rel
        if _is_link_or_reparse(path):
            problems.append(f"symlinked managed file: {path}")
            continue
        if not path.is_file():
            problems.append(f"missing file: {path}")
            continue
        try:
            if file_sha256(path) != digest:
                problems.append(f"hash mismatch: {path}")
        except OSError as exc:
            problems.append(f"hash failed for {path}: {exc}")

    expected_root = gimp_config_root(gimp).resolve()
    try:
        config_dir.resolve().relative_to(expected_root)
    except ValueError:
        problems.append(
            f"config dir {config_dir} is not under expected root {expected_root} "
            f"for GIMP kind {gimp.kind}"
        )
    if config_dir.name not in SUPPORTED_CONFIG_FOLDERS:
        problems.append(
            f"config folder {config_dir.name} not in supported set "
            f"{sorted(SUPPORTED_CONFIG_FOLDERS)}"
        )
    return problems


def remove_photogimp_managed_files(
    config_dir: Path,
    *,
    expected_hashes: Optional[dict] = None,
) -> list[str]:
    """Remove PhotoGIMP-owned files only.

    If expected_hashes is provided, remove a file only when its sha256 still
    matches what this installer wrote (provenance). Without hashes, refuse to
    delete (caller must use backup restore instead).
    """
    removed: list[str] = []
    if not config_dir.is_dir():
        return removed
    if not expected_hashes:
        warn(
            "No install provenance hashes; refusing filename-only removal. "
            "Restore a matching pre-install backup instead."
        )
        return removed

    # Files
    for rel, digest in expected_hashes.items():
        path = config_dir / rel
        if _is_link_or_reparse(path):
            warn(f"Refusing to remove symlinked managed path: {path}")
            continue
        if not path.is_file():
            continue
        try:
            if file_sha256(path) == digest:
                path.unlink()
                _fsync_directory(path.parent)
                removed.append(str(path))
            else:
                info(f"  kept modified file (hash changed): {path}")
        except OSError as exc:
            warn(f"Could not inspect {path}: {exc}")

    # Remove empty managed dirs
    for name in MANAGED_DIRS:
        path = config_dir / name
        if _is_link_or_reparse(path):
            warn(f"Refusing to prune symlinked managed directory: {path}")
            continue
        if path.is_dir() and not any(path.rglob("*")):
            shutil.rmtree(path)
            _fsync_directory(path.parent)
            removed.append(str(path) + "/")
        elif path.is_dir():
            # Remove files we already deleted; prune empty subdirs
            for sub in sorted(path.rglob("*"), reverse=True):
                if sub.is_dir() and not any(sub.iterdir()):
                    sub.rmdir()
                    _fsync_directory(sub.parent)
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
                _fsync_directory(path.parent)
                removed.append(str(path) + "/")
    return removed


def restore_managed_from_backup(
    backup: Path,
    config_dir: Path,
    installed_hashes: dict[str, str],
) -> tuple[list[str], dict[str, str]]:
    """Restore only installer-owned paths, preserving post-install user additions."""
    problems = verify_backup_integrity(backup)
    if problems:
        raise OSError("Uninstall baseline failed integrity check: " + "; ".join(problems))
    if not _backup_matches_config(backup, config_dir):
        raise OSError("Uninstall baseline belongs to a different profile")
    baseline_root = backup_profile_root(backup)
    restored: list[str] = []
    remaining: dict[str, str] = {}
    for rel, installed_digest in installed_hashes.items():
        if not safe_managed_relative_path(rel):
            raise OSError(f"Unsafe installed path in state: {rel}")
        current = config_dir / rel
        baseline = baseline_root / rel
        if _is_link_or_reparse(current) or _is_link_or_reparse(baseline):
            raise OSError(f"Refusing managed restore through symlink: {rel}")
        baseline_digest = file_sha256(baseline) if baseline.is_file() else None
        if not current.is_file():
            if baseline_digest is not None:
                copy_file(baseline, current)
                restored.append(rel)
            continue
        current_digest = file_sha256(current)
        if baseline_digest is not None and current_digest == baseline_digest:
            restored.append(rel)
            continue
        if current_digest != installed_digest:
            remaining[rel] = installed_digest
            continue
        if baseline_digest is not None:
            copy_file(baseline, current)
            if file_sha256(current) != baseline_digest:
                raise OSError(f"Managed baseline verification failed: {rel}")
            restored.append(rel)
        elif baseline.exists():
            raise OSError(f"Baseline managed entry has incompatible type: {rel}")
        else:
            current.unlink()
            _fsync_directory(current.parent)
            restored.append(rel)
    for directory in MANAGED_DIRS:
        root = config_dir / directory
        if root.is_dir():
            for child in sorted(root.rglob("*"), reverse=True):
                if child.is_dir() and not any(child.iterdir()):
                    child.rmdir()
            if root.is_dir() and not any(root.iterdir()):
                root.rmdir()
    return restored, remaining


def remove_linux_branding(desktop_backup: str = "") -> list[str]:
    problems: list[str] = []
    share_root = xdg_data_home()
    safe_desktop_backup = ""
    if desktop_backup:
        try:
            candidate = Path(desktop_backup).resolve(strict=False)
            allowed = (data_home() / "desktop-entry-backup").resolve(strict=False)
            candidate.relative_to(allowed)
            safe_desktop_backup = str(candidate)
        except (OSError, ValueError):
            problems.append(f"Unsafe recorded desktop backup path: {desktop_backup}")
    # New id
    for name in ("photogimp.desktop", "org.gimp.GIMP.desktop"):
        desktop = share_root / "applications" / name
        if not desktop.is_file():
            continue
        try:
            text = desktop.read_text(encoding="utf-8")
        except OSError:
            continue
        if "X-PhotoGIMP-Installer=true" in text:
            if name == "photogimp.desktop" and safe_desktop_backup:
                backup = Path(safe_desktop_backup)
                if backup.is_file():
                    shutil.copy2(backup, desktop)
                    info(f"Restored previous desktop entry from {backup}")
                    continue
            if name == "org.gimp.GIMP.desktop":
                # Only remove stock id if we clearly overwrote it with PhotoGIMP
                backup = Path(safe_desktop_backup) if safe_desktop_backup else (
                    data_home() / "desktop-entry-backup" / "org.gimp.GIMP.desktop"
                )
                if backup.is_file():
                    try:
                        desktop.write_text(
                            backup.read_text(encoding="utf-8"), encoding="utf-8"
                        )
                        info(f"Restored original desktop entry from {backup}")
                        continue
                    except OSError as exc:
                        warn(f"Could not restore desktop entry: {exc}")
            try:
                desktop.unlink()
                info(f"Removed {desktop}")
            except OSError as exc:
                warn(f"Could not remove desktop entry: {exc}")
                problems.append(f"Could not remove desktop entry {desktop}: {exc}")

    icons_src = linux_branding_root() / "share" / "icons"
    if icons_src.is_dir():
        for source in icons_src.rglob("*"):
            if not source.is_file():
                continue
            dest = share_root / "icons" / source.relative_to(icons_src)
            try:
                if dest.is_file() and file_sha256(dest) == file_sha256(source):
                    dest.unlink()
                    info(f"Removed {dest}")
            except OSError as exc:
                problems.append(f"Could not inspect/remove icon {dest}: {exc}")
    return problems


# ---------------------------------------------------------------------------
# High-level commands
# ---------------------------------------------------------------------------


def preflight_gimp_closed() -> int:
    state = gimp_process_state()
    if state == PROCESS_RUNNING:
        error("GIMP appears to be running. Quit GIMP completely, then try again.")
        return EXIT_PREFLIGHT
    if state == PROCESS_UNKNOWN:
        error(
            "Cannot determine whether GIMP is running. Process inspection is "
            "unavailable or failed; refusing to mutate the profile."
        )
        return EXIT_PREFLIGHT
    return EXIT_OK


def _require_gimp_closed(action: str) -> None:
    state = gimp_process_state()
    if state != PROCESS_NOT_RUNNING:
        raise OSError(
            f"GIMP process state is {state!r} while {action}; refusing profile mutation"
        )


def recheck_gimp_closed_after_write() -> None:
    """Warn if GIMP appears to have started during/after a write."""
    state = gimp_process_state()
    if state == PROCESS_RUNNING:
        warn(
            "GIMP appears to be running after config changes. "
            "Quit GIMP without saving session preferences if prompted, "
            "or re-run install — an open GIMP may overwrite these settings on exit."
        )
    elif state == PROCESS_UNKNOWN:
        warn("Could not re-check GIMP process state after the write.")


def wait_for_config_dir(gimp: GimpInfo, config_dir: Path) -> Optional[Path]:
    """Ensure the bound GIMP 3.0 config dir exists (no silent redirect to other versions)."""
    problem = validate_gimp3_config_target(gimp, config_dir)
    if problem:
        error(problem)
        return None

    if config_dir.is_dir():
        return config_dir

    root = gimp_config_root(gimp)
    legacy = list_legacy_version_dirs(root)
    modern = list_version_dirs(root)
    if legacy and not modern:
        error(
            "Only GIMP 2.x config folders are present. "
            "Install GIMP 3.0.x, open it once, then re-run."
        )
        return None

    # Do not redirect to a different version folder (e.g. 3.2 when bound to 3.0)
    other = [p for p in modern if p.name != config_dir.name]
    if other:
        warn(
            f"Other GIMP config folders exist {[p.name for p in other]} but this "
            f"PhotoGIMP payload targets {config_dir.name} only."
        )

    info("")
    info(f"GIMP config folder not found yet: {config_dir}")
    info(
        f"Open GIMP {gimp.version or '3.0.x'} once so it creates {config_dir.name}/, "
        "then fully quit GIMP."
    )
    pause("When GIMP is closed, press Enter to continue...")

    if config_dir.is_dir() and (config_dir / "gimprc").is_file():
        return config_dir

    error(
        f"Config folder still missing or uninitialized at {config_dir}. "
        "Open the selected GIMP once so it creates gimprc, fully quit, then re-run. "
        "Refusing to create an empty profile (GIMP would overwrite it on first launch)."
    )
    return None


def cmd_status() -> int:
    environment_problem = validate_environment_paths()
    if environment_problem:
        error(environment_problem)
        return EXIT_PREFLIGHT
    installs = detect_all_gimp_installs()
    backups = list_backups()
    payload_problem = ""
    try:
        ensure_payload()
    except FileNotFoundError as exc:
        payload_problem = str(exc)

    info(f"PhotoGIMP installer {SCRIPT_VERSION}")
    info(f"Platform:        {platform.system()} ({platform.machine()})")
    info(f"Python:          {sys.version.split()[0]}")
    info(f"Repo root:       {repo_root()}")
    info(f"Payload:         {payload_dir()} ({'verified' if not payload_problem else 'INVALID'})")
    if payload_problem:
        info(f"  - {payload_problem}")
    info(f"Supported folders: {sorted(SUPPORTED_CONFIG_FOLDERS)}")
    info(f"GIMP installs:   {len(installs)}")
    for i, g in enumerate(installs, 1):
        tag = " [UNSUPPORTED]" if g.kind in UNSUPPORTED_KINDS else ""
        info(f"  {i}) {g.label()}{tag}")
        info("      version/config: not probed by read-only status")
    if not installs:
        info("  (none detected)")
    process_state = gimp_process_state()
    info(f"GIMP running:    {process_state}")
    info(f"Data home:       {data_home()}")
    if os.environ.get("XDG_DATA_HOME") and not is_windows():
        info(f"  (from XDG_DATA_HOME={os.environ.get('XDG_DATA_HOME')})")
    info(f"Backups:         {len(backups)} under {backups_dir()}")
    failed = (
        process_state == PROCESS_UNKNOWN
        or bool(payload_problem)
        or _is_link_or_reparse(backups_dir())
    )
    for index, backup in enumerate(backups):
        meta = read_backup_meta(backup)
        backup_problems = verify_backup_integrity(backup)
        state_label = "INVALID" if backup_problems else "sealed"
        if index < 5:
            info(f"  - {backup.name} ({meta.get('reason', '?')}, {state_label})")
        if backup_problems:
            failed = True
            if index < 5:
                for problem in backup_problems[:3]:
                    info(f"      - {problem}")
    reg = InstallRegistry.load()
    if reg.errors:
        failed = True
        info("Install state:   INVALID")
        for message in reg.errors:
            info(f"  - {message}")
    states = reg.all_states()
    if states:
        info(f"Install state:   {len(states)} recorded profile(s)")
        for state in states:
            info(f"  - {state.config_path}")
            info(
                f"      kind={state.gimp_kind} version={state.gimp_version or '?'} "
                f"at={state.installed_at}"
            )
            if state.config_path:
                cfg = Path(state.config_path)
                expected = state.installed_hashes or {}
                fake = GimpInfo(
                    found=True,
                    kind=state.gimp_kind or "native",
                    binary=state.gimp_binary or None,
                    app_path=state.gimp_app_path or None,
                    version=state.gimp_version or None,
                )
                if expected:
                    problems = verify_install(cfg, expected, fake)
                    if problems:
                        failed = True
                        info("      Verify: FAILED")
                        for p in problems[:5]:
                            info(f"        - {p}")
                    else:
                        info("      Verify: OK (SHA-256)")
                else:
                    info("      Verify: no hashes recorded")
                    failed = True
                if journal_path(cfg).is_file() or _replace_journal_path(cfg).is_file():
                    failed = True
                    info("      Transaction: INCOMPLETE")
    else:
        info("Install state:   none (installer has not recorded an install)")
    return EXIT_ERROR if failed else EXIT_OK


def cmd_backup() -> int:
    blocked = require_interactive("create a backup")
    if blocked is not None:
        return blocked
    code = preflight_execution_context()
    if code != EXIT_OK:
        return code
    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code
    installs = detect_all_gimp_installs()
    if not installs:
        error("GIMP not detected; nothing to back up from a known config path.")
        return EXIT_ERROR
    gimp = choose_gimp_install(installs, for_install=True)
    if gimp is None:
        return EXIT_CANCELLED
    gimp = enrich_gimp_version(gimp)
    config_dir = resolve_config_dir(gimp)
    problem = validate_gimp3_config_target(gimp, config_dir)
    if problem:
        error(problem)
        return EXIT_PREFLIGHT
    if config_dir.exists() and not config_dir.is_dir():
        error(f"Config path is not a directory: {config_dir}")
        return EXIT_ERROR
    if not config_dir.is_dir():
        error(f"Config directory does not exist: {config_dir}")
        return EXIT_ERROR
    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code
    try:
        with operation_lock("profile", config_dir):
            tree_recovery = recover_replace_transaction(config_dir)
            if tree_recovery:
                info(tree_recovery)
            install_recovery = recover_incomplete_install(config_dir)
            if install_recovery:
                info(install_recovery.message)
            backup = create_backup(config_dir, reason="manual", gimp=gimp)
            return EXIT_OK if backup else EXIT_ERROR
    except OSError as exc:
        error(f"Backup failed safely: {exc}")
        return EXIT_ERROR


def cmd_restore(backup_id: Optional[str] = None) -> int:
    blocked = require_interactive("restore a backup")
    if blocked is not None:
        return blocked
    code = preflight_execution_context()
    if code != EXIT_OK:
        return code
    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code

    backups = list_backups()
    if not backups:
        error(f"No backups found in {backups_dir()}")
        return EXIT_ERROR

    chosen: Optional[Path] = None
    if backup_id:
        exact = [b for b in backups if b.name == backup_id]
        if len(exact) == 1:
            chosen = exact[0]
        elif len(exact) > 1:
            error(f"Multiple backups named {backup_id!r}; refuse to guess.")
            return EXIT_ERROR
        else:
            error(
                f"Backup not found: {backup_id!r}. "
                "Use the exact folder name from `status` (no partial matches)."
            )
            return EXIT_ERROR
    else:
        info("Available GIMP profile backups (reason and source shown):")
        for i, backup in enumerate(backups, 1):
            meta = read_backup_meta(backup)
            info(
                f"  {i}) {backup.name}  "
                f"reason={meta.get('reason', '?')}  "
                f"source={meta.get('source', '')}"
            )
        answer = prompt("Select backup number to restore (or empty to cancel)", "")
        if not answer:
            info("Cancelled.")
            return EXIT_CANCELLED
        chosen = select_number(answer, backups)
        if chosen is None:
            error("Invalid selection.")
            return EXIT_ERROR

    meta = read_backup_meta(chosen)
    gimp = detect_gimp()
    if not gimp.found:
        warn("GIMP not detected; using path from backup metadata when possible.")

    seal = verify_backup_integrity(chosen)
    if seal:
        error("Backup integrity check failed:")
        for p in seal:
            error(f"  - {p}")
        return EXIT_ERROR

    source = meta.get("source") or ""
    backup_gimp = gimp_info_from_backup_meta(meta)
    if not source:
        error("Backup metadata missing source path; refuse to guess restore target.")
        return EXIT_ERROR
    config_dir = Path(source)

    # Derive trust from the recorded package kind's canonical root, never from
    # editable config_root metadata.
    expected_root = gimp_config_root(backup_gimp)
    try:
        safe_target = (
            config_dir.name in SUPPORTED_CONFIG_FOLDERS
            and config_dir.parent.resolve() == expected_root.resolve()
        )
    except OSError:
        safe_target = False
    if not safe_target:
        error(
            f"Backup source {config_dir} is not an approved version folder "
            f"directly under {expected_root}. Refusing restore."
        )
        return EXIT_ERROR

    # Block cross-kind restore unless user explicitly confirms
    if meta.get("gimp_kind") and gimp.found and meta.get("gimp_kind") != gimp.kind:
        warn(
            f"Backup was taken for GIMP kind {meta.get('gimp_kind')!r}, "
            f"current default detect is {gimp.kind!r}."
        )
        if not confirm(
            "Restore this backup into its original path anyway (cross-kind)?",
            False,
        ):
            info("Cancelled.")
            return EXIT_CANCELLED

    info("")
    info("Restore a GIMP profile backup")
    info(f"  Backup: {chosen}")
    info(f"  Target: {config_dir}")
    info(f"  Kind:   {backup_gimp.kind}")
    if not confirm("Overwrite current GIMP config with this backup?", False):
        info("Cancelled.")
        return EXIT_CANCELLED

    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code

    try:
        with operation_lock("profile", config_dir):
            return _execute_restore(chosen, config_dir, backup_gimp)
    except OSError as exc:
        error(str(exc))
        return EXIT_ERROR


def _execute_restore(backup: Path, config_dir: Path, backup_gimp: GimpInfo) -> int:
    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code
    recovery = recover_replace_transaction(config_dir)
    if recovery:
        info(recovery)
    install_recovery = recover_incomplete_install(config_dir)
    if install_recovery:
        info(install_recovery.message)
    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code
    restore_backup(backup, config_dir, gimp=backup_gimp)
    recheck_gimp_closed_after_write()
    reg = InstallRegistry.load()
    if reg.errors:
        error("Restore completed, but install registry is invalid; refusing false success.")
        return EXIT_ERROR
    recorded = reg.get(str(config_dir))
    if recorded:
        recorded_gimp = GimpInfo(
            found=True,
            kind=recorded.gimp_kind or "native",
            binary=recorded.gimp_binary or None,
            app_path=recorded.gimp_app_path or None,
            version=recorded.gimp_version or None,
        )
        still_installed = bool(recorded.installed_hashes) and not verify_install(
            config_dir, recorded.installed_hashes, recorded_gimp
        )
        if still_installed:
            info("Restored profile still matches PhotoGIMP; kept install marker.")
        else:
            reg.remove(str(config_dir))
            info("Cleared PhotoGIMP install marker for this profile.")
    return EXIT_OK


def _rollback_install(
    backup: Optional[Path],
    config_dir: Path,
    gimp: GimpInfo,
    *,
    was_empty: bool,
) -> bool:
    """Restore and verify the transaction baseline; retain journals on failure."""
    if backup is not None:
        warn(f"Rolling back from backup {backup.name}...")
        try:
            _replace_from_verified_backup(backup, config_dir)
            problems = _verify_tree_against_backup(config_dir, backup)
            if problems:
                raise OSError("rollback verification failed: " + "; ".join(problems))
            info("Rollback complete.")
            return True
        except OSError as exc:
            error(f"Rollback failed: {exc}")
            error(f"Recovery journal retained. Backup: {backup}; target: {config_dir}")
            return False
    elif was_empty:
        warn("Removing partially written managed files from new profile...")
        remove_photogimp_managed_files(config_dir)
        return not any((config_dir / name).exists() for name in MANAGED_TOPS)
    return False


def uninstall_baseline_id(
    registry: InstallRegistry,
    config_dir: Path,
    transaction_backup: Path,
) -> str:
    """Preserve the original clean backup across upgrades/reinstalls."""
    previous = registry.get(str(config_dir))
    if not previous or not previous.backup_id:
        return transaction_backup.name
    baseline = _backup_from_id(previous.backup_id)
    problems = verify_backup_integrity(baseline)
    if problems or not _backup_matches_config(baseline, config_dir):
        raise OSError(
            "Existing PhotoGIMP uninstall baseline is invalid or belongs to another profile: "
            + "; ".join(problems)
        )
    return previous.backup_id


def cmd_install() -> int:
    blocked = require_interactive("install PhotoGIMP")
    if blocked is not None:
        return blocked

    code = preflight_execution_context()
    if code != EXIT_OK:
        return code

    try:
        ensure_payload()
    except FileNotFoundError as exc:
        error(str(exc))
        return EXIT_ERROR

    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code

    gimp = ensure_gimp_installed()
    if gimp is None:
        return EXIT_CANCELLED
    if not gimp.found:
        return EXIT_PREFLIGHT
    if gimp.kind in UNSUPPORTED_KINDS:
        error(
            f"{gimp.kind.capitalize()} GIMP is not supported for install. "
            "Use Flatpak (Linux) or a normal installed GIMP 3.0.x, then re-run."
        )
        return EXIT_PREFLIGHT

    gimp = enrich_gimp_version(gimp)
    if not gimp.version:
        error(
            "Cannot probe GIMP version for the selected install. "
            "Refusing to install without a proven binary↔profile binding."
        )
        return EXIT_PREFLIGHT

    config_dir = resolve_config_dir(gimp)
    problem = validate_gimp3_config_target(gimp, config_dir)
    if problem:
        error(problem)
        return EXIT_PREFLIGHT

    info("")
    explain_target(gimp, config_dir)
    info(f"  GIMP version:  {gimp.version}")
    info(f"  Payload:       {payload_dir()} (folder {PAYLOAD_CONFIG_VERSION})")
    info("")

    # Multi-packaging acknowledgment
    others = [
        g
        for g in detect_all_gimp_installs()
        if g.kind not in UNSUPPORTED_KINDS and g.kind != gimp.kind
    ]
    if others:
        info("Other GIMP packaging models are also present:")
        for g in others:
            info(f"  - {g.label()}")
        if not confirm(
            f"Continue installing ONLY for {gimp.kind}? "
            "Other installs will NOT receive PhotoGIMP.",
            False,
        ):
            info("Cancelled.")
            return EXIT_CANCELLED

    multi = len([g for g in detect_all_gimp_installs() if g.kind not in UNSUPPORTED_KINDS]) > 1
    try:
        with operation_lock("profile", config_dir):
            return _install_selected_profile(gimp, config_dir, multi)
    except OSError as exc:
        error(f"Cannot acquire or complete the profile transaction: {exc}")
        return EXIT_ERROR


def _install_selected_profile(gimp: GimpInfo, config_dir: Path, multi: bool) -> int:
    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code
    try:
        tree_recovery = recover_replace_transaction(config_dir)
        if tree_recovery:
            info(tree_recovery)
        recovery = recover_incomplete_install(config_dir)
    except OSError as exc:
        error(f"Cannot safely recover an interrupted install: {exc}")
        error("No new writes were made. Resolve the journal/backup issue first.")
        return EXIT_ERROR
    if recovery:
        info(recovery.message)
        if recovery.finalized_install:
            return EXIT_OK

    resolved = wait_for_config_dir(gimp, config_dir)
    if resolved is None:
        error("Config directory not ready.")
        return EXIT_PREFLIGHT
    config_dir = resolved
    problem = validate_gimp3_config_target(gimp, config_dir)
    if problem:
        error(problem)
        return EXIT_PREFLIGHT
    if not config_dir.is_dir() or not (config_dir / "gimprc").is_file():
        error(f"Initialized GIMP profile required at {config_dir} (missing gimprc).")
        return EXIT_PREFLIGHT
    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code
    if not confirm(
        "Create a sealed backup and install into this exact profile?", not multi
    ):
        return EXIT_CANCELLED

    registry = InstallRegistry.load()
    if registry.errors:
        error("Install registry is invalid; refusing to overwrite it:")
        for message in registry.errors:
            error(f"  - {message}")
        return EXIT_ERROR
    backup = create_backup(config_dir, reason="pre-install", gimp=gimp)
    if backup is None:
        error("Backup failed; aborting install.")
        return EXIT_ERROR
    try:
        baseline_backup_id = uninstall_baseline_id(registry, config_dir, backup)
    except OSError as exc:
        error(str(exc))
        return EXIT_ERROR

    info("Installing PhotoGIMP settings (sealed backup → stage → verify → atomic commit)...")
    try:
        installed_hashes = install_payload(
            config_dir,
            gimp,
            backup_id=backup.name,
            baseline_backup_id=baseline_backup_id,
        )
        problems = verify_install(config_dir, installed_hashes, gimp)
        if problems:
            error("Post-install verification failed:")
            for p in problems:
                error(f"  - {p}")
            _recover_failed_install_attempt(config_dir)
            return EXIT_ERROR
    except KeyboardInterrupt:
        error("Interrupted during install; running transaction recovery...")
        _recover_failed_install_attempt(config_dir)
        return EXIT_CANCELLED
    except (OSError, NotADirectoryError, FileNotFoundError) as exc:
        error(f"Install failed: {exc}")
        _recover_failed_install_attempt(config_dir)
        return EXIT_ERROR

    state = InstallState(
        backup_id=baseline_backup_id,
        config_path=str(config_dir),
        installed_at=iso_now(),
        config_version=config_dir.name,
        platform=platform.system(),
        gimp_kind=gimp.kind,
        gimp_binary=gimp.binary or "",
        gimp_app_path=gimp.app_path or "",
        gimp_version=gimp.version or "",
        branding_installed=False,
        desktop_backup="",
        installed_hashes=installed_hashes,
        script_version=SCRIPT_VERSION,
    )
    try:
        registry.upsert(state)
    except OSError as exc:
        error(f"Could not persist install state: {exc}")
        error(f"Committed journal retained at {journal_path(config_dir)} for recovery.")
        return EXIT_ERROR
    clear_install_journal(config_dir)

    info(
        "Structural verification OK: SHA-256 matches the authoritative payload "
        "manifest under the bound profile. Runtime activation is not proven."
    )
    recheck_gimp_closed_after_write()

    info("")
    info("PhotoGIMP configuration files installed and verified on disk (SHA-256).")
    info(f"Target:    {config_dir} (GIMP kind: {gimp.kind}, version: {gimp.version})")
    info(f"Backup id: {backup.name}")
    info(f"Backups:   {backups_dir()}")
    info("Launch the SAME GIMP you selected to confirm the layout.")
    if gimp.kind == "flatpak":
        info("Note: Flatpak only — native GIMP uses a different config path.")
    info("Filesystem verification only — runtime activation is not tested by this tool.")
    info("To undo later: run this installer and choose restore or uninstall.")
    return EXIT_OK


def _recover_failed_install_attempt(config_dir: Path) -> bool:
    """Recover only states whose journal proves rollback/finalization is unambiguous."""
    try:
        tree_recovery = recover_replace_transaction(config_dir)
        if tree_recovery:
            info(tree_recovery)
        recovery = recover_incomplete_install(config_dir)
        if recovery:
            info(recovery.message)
        return True
    except OSError as exc:
        error(f"Automatic recovery stopped safely: {exc}")
        error(f"Transaction journal retained at {journal_path(config_dir)}")
        return False


def _backup_matches_config(backup: Path, config_dir: Path) -> bool:
    meta = read_backup_meta(backup)
    source = meta.get("source") or ""
    if not source:
        return False
    try:
        return Path(source).resolve() == config_dir.resolve()
    except OSError:
        return Path(source) == config_dir


def cmd_uninstall() -> int:
    blocked = require_interactive("uninstall PhotoGIMP")
    if blocked is not None:
        return blocked
    code = preflight_execution_context()
    if code != EXIT_OK:
        return code
    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code

    reg = InstallRegistry.load()
    if reg.errors:
        error("Install registry is invalid; refusing uninstall:")
        for message in reg.errors:
            error(f"  - {message}")
        return EXIT_ERROR
    states = reg.all_states()

    # Always let the user pick which profile to uninstall when multiple exist
    if len(states) > 1:
        info("PhotoGIMP is recorded on multiple profiles:")
        for i, st in enumerate(states, 1):
            info(f"  {i}) {st.config_path} ({st.gimp_kind}, {st.gimp_version or '?'})")
        answer = prompt("Choose profile number to uninstall (empty cancels)", "")
        if not answer:
            return EXIT_CANCELLED
        state = select_number(answer, states)
        if state is None:
            error("Invalid selection.")
            return EXIT_ERROR
        config_dir = Path(state.config_path)
        gimp = GimpInfo(
            found=True,
            kind=state.gimp_kind or "native",
            binary=state.gimp_binary or None,
            app_path=state.gimp_app_path or None,
            version=state.gimp_version or None,
        )
    elif len(states) == 1:
        state = states[0]
        config_dir = Path(state.config_path)
        gimp = GimpInfo(
            found=True,
            kind=state.gimp_kind or "native",
            binary=state.gimp_binary or None,
            app_path=state.gimp_app_path or None,
            version=state.gimp_version or None,
        )
    else:
        error(
            "No trusted PhotoGIMP install state found. Refusing guessed-profile uninstall; "
            "use Restore a backup with an exact sealed backup id instead."
        )
        return EXIT_PREFLIGHT

    info("Uninstall PhotoGIMP")
    info(f"  Config dir: {config_dir}")
    if gimp.found:
        explain_target(gimp, config_dir)

    try:
        approved_profile = (
            config_dir.name in SUPPORTED_CONFIG_FOLDERS
            and config_dir.parent.resolve() == gimp_config_root(gimp).resolve()
        )
    except OSError:
        approved_profile = False
    if not approved_profile:
        error(
            f"Recorded config path {config_dir} is not an approved profile under "
            f"{gimp_config_root(gimp)}. Refusing uninstall."
        )
        return EXIT_ERROR

    if config_dir.exists() and _is_link_or_reparse(config_dir):
        error("Config path is linked; refusing uninstall through links.")
        return EXIT_ERROR
    if config_dir.exists() and not config_dir.is_dir():
        error(f"Config path is not a directory: {config_dir}")
        return EXIT_ERROR

    try:
        with operation_lock("profile", config_dir):
            return _uninstall_selected_profile(reg, state, config_dir, gimp)
    except OSError as exc:
        error(f"Uninstall failed safely: {exc}")
        return EXIT_ERROR


def _uninstall_selected_profile(
    reg: InstallRegistry,
    state: Optional[InstallState],
    config_dir: Path,
    gimp: GimpInfo,
) -> int:
    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code
    recovery = recover_replace_transaction(config_dir)
    if recovery:
        info(recovery)
    install_recovery = recover_incomplete_install(config_dir)
    if install_recovery:
        info(install_recovery.message)
        reg = InstallRegistry.load()
        if reg.errors:
            raise OSError("Install recovery left an invalid registry")
        state = reg.get(str(config_dir))
    code = preflight_gimp_closed()
    if code != EXIT_OK:
        return code
    if state is None or not state.installed_hashes:
        error(
            "No trusted install provenance exists for this profile. Refusing filename-only "
            "removal or full-profile deletion. Use Restore a backup and select an exact "
            "sealed backup instead."
        )
        return EXIT_PREFLIGHT

    backup: Optional[Path] = None
    if state.backup_id:
        backup = _backup_from_id(state.backup_id)
        if not backup.is_dir() or not _backup_matches_config(backup, config_dir):
            raise OSError("Recorded uninstall baseline is missing or belongs to another profile")
        problems = verify_backup_integrity(backup)
        if problems:
            raise OSError("Recorded uninstall baseline is invalid: " + "; ".join(problems))

    if not confirm(
        "Restore only PhotoGIMP-managed paths and preserve unrelated current files?",
        True,
    ):
        return EXIT_CANCELLED
    live_entries = _tree_entries(config_dir) if config_dir.is_dir() else None
    if config_dir.is_dir() and any(config_dir.iterdir()):
        safety = create_backup(config_dir, reason="pre-uninstall-managed", gimp=gimp)
        if safety is None:
            raise OSError("Required pre-uninstall safety backup failed")

    if gimp_process_state() != PROCESS_NOT_RUNNING:
        raise OSError("GIMP process state changed before uninstall; refusing mutation")
    if live_entries is not None:
        live_problems = _verify_tree_entries(config_dir, live_entries)
        if live_problems:
            raise OSError(
                "Profile changed after the uninstall safety snapshot; refusing mutation: "
                + "; ".join(live_problems[:5])
            )

    if backup is not None:
        changed, remaining_hashes = restore_managed_from_backup(
            backup, config_dir, state.installed_hashes
        )
    else:
        changed = remove_photogimp_managed_files(
            config_dir, expected_hashes=state.installed_hashes
        )
        remaining_hashes = {
            rel: digest
            for rel, digest in state.installed_hashes.items()
            if (config_dir / rel).is_file()
        }
    for rel in changed:
        info(f"  restored/removed: {rel}")
    if config_dir.is_dir():
        _fsync_tree(config_dir)
        _fsync_directory(config_dir.parent)

    branding_remaining = state.branding_installed
    if branding_remaining and confirm("Remove legacy PhotoGIMP Linux branding?", True):
        branding_problems = remove_linux_branding(state.desktop_backup)
        if branding_problems:
            for problem in branding_problems:
                error(problem)
        else:
            branding_remaining = False

    if remaining_hashes or branding_remaining:
        state.installed_hashes = remaining_hashes
        state.branding_installed = branding_remaining
        reg.upsert(state)
        warn("Uninstall was partial because user-modified managed files or branding remain.")
        return EXIT_ERROR
    reg.remove(str(config_dir))
    recheck_gimp_closed_after_write()
    info("Uninstall finished; unrelated current profile files were preserved.")
    return EXIT_OK


# ---------------------------------------------------------------------------
# CLI / menu
# ---------------------------------------------------------------------------


def print_menu() -> None:
    info("")
    info("PhotoGIMP Setup")
    info("---------------")
    info("1) Install PhotoGIMP")
    info("2) Restore a GIMP profile backup")
    info("3) Uninstall PhotoGIMP")
    info("4) Status")
    info("5) Exit")
    info("")


def interactive_menu() -> int:
    """Interactive loop: cancel/success return to menu; only Exit leaves."""
    blocked = require_interactive("run the interactive menu")
    if blocked is not None:
        return blocked

    actions = {
        "1": cmd_install,
        "2": lambda: cmd_restore(None),
        "3": cmd_uninstall,
        "4": cmd_status,
    }
    last_code = EXIT_OK
    while True:
        print_menu()
        # No default action — empty/EOF cancels to re-prompt, not auto-install
        choice = prompt("Choose an option (empty re-prompts)", "")
        if _prompt_eof:
            return EXIT_CANCELLED
        if not choice:
            continue
        if choice in ("5", "q", "quit", "exit"):
            return last_code
        action = actions.get(choice)
        if not action:
            warn("Invalid option.")
            continue
        code = action()
        if code == EXIT_CANCELLED:
            continue
        last_code = code
        if code == EXIT_OK:
            info("Done. Returning to menu.")
        elif code == EXIT_PREFLIGHT:
            warn("Preflight check failed. Returning to menu.")
        elif code == EXIT_ERROR:
            warn("Command failed. Returning to menu.")
        continue


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="photogimp_install.py",
        description="PhotoGIMP interactive installer (backup, install, restore, uninstall).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"PhotoGIMP installer {SCRIPT_VERSION}",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("install", help="Install PhotoGIMP (with automatic backup)")
    sub.add_parser("backup", help="Backup current GIMP configuration only")
    restore_p = sub.add_parser(
        "restore",
        help="Restore an exact sealed GIMP profile backup",
    )
    restore_p.add_argument(
        "backup_id",
        nargs="?",
        default=None,
        help="Backup id (folder name); omit to choose interactively",
    )
    sub.add_parser("uninstall", help="Remove/restore installer-owned PhotoGIMP paths")
    sub.add_parser("status", help="Show detection, paths, backups, and install state")
    sub.add_parser("menu", help="Show interactive menu (default)")
    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    command = args.command
    if command is None or command == "menu":
        code = interactive_menu()
    elif command == "install":
        code = cmd_install()
    elif command == "backup":
        code = cmd_backup()
    elif command == "restore":
        code = cmd_restore(args.backup_id)
    elif command == "uninstall":
        code = cmd_uninstall()
    elif command == "status":
        code = cmd_status()
    else:
        parser.error(f"Unknown command: {command}")
        return EXIT_ERROR

    return code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(EXIT_CANCELLED)
