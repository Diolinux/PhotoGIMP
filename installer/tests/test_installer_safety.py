#!/usr/bin/env python3
"""P0 safety tests for photogimp_install.py (stdlib unittest)."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "installer" / "photogimp_install.py"


def load_installer():
    spec = importlib.util.spec_from_file_location("photogimp_install", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    mod.__file__ = str(MODULE_PATH)
    sys.modules["photogimp_install"] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


pg = load_installer()
real_gimp_config_root = pg.gimp_config_root


class InstallerSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="pgtest-")).resolve()
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))
        self.config_root = self.tmp / "GIMP"
        self.config_root.mkdir()
        self.backups = self.tmp / "backups"
        self.backups.mkdir()
        # Point installer data roots at temp
        pg.backups_dir = lambda: self.backups  # type: ignore
        pg.data_home = lambda: self.tmp / "data"  # type: ignore
        pg.state_path = lambda: self.tmp / "data" / "state.json"  # type: ignore
        pg.gimp_config_root = lambda gimp: self.config_root  # type: ignore
        pg.gimp_process_state = lambda: pg.PROCESS_NOT_RUNNING  # type: ignore
        pg.is_elevated = lambda: False  # type: ignore

    def _native(self, version: Optional[str] = "3.0.4") -> object:
        return pg.GimpInfo(
            found=True,
            kind="native",
            binary="/usr/bin/gimp",
            version=version,
        )

    def _install_over_profile(self, cfg: Path, g: object) -> tuple[dict, Path]:
        backup = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert backup is not None
        hashes = pg.install_payload(
            cfg,
            g,
            backup_id=backup.name,
            baseline_backup_id=backup.name,
        )
        return hashes, backup

    def test_resolve_binds_probed_version_not_newest_on_disk(self) -> None:
        (self.config_root / "3.0").mkdir()
        (self.config_root / "3.2").mkdir()
        g = self._native("3.0.4")
        cfg = pg.resolve_config_dir(g)
        self.assertEqual(cfg.name, "3.0")
        self.assertEqual(cfg, self.config_root / "3.0")

    def test_refuse_unsupported_config_folder(self) -> None:
        g = self._native("3.2.0")
        cfg = pg.resolve_config_dir(g)
        self.assertEqual(cfg.name, "3.2")
        err = pg.validate_gimp3_config_target(g, cfg)
        self.assertIsNotNone(err)
        self.assertIn("supports config folder", err or "")

    def test_symlink_profile_refused(self) -> None:
        outside = self.tmp / "outside"
        outside.mkdir()
        link = self.config_root / "3.0"
        link.symlink_to(outside, target_is_directory=True)
        g = self._native("3.0.0")
        err = pg.validate_gimp3_config_target(g, link)
        self.assertIsNotNone(err)
        self.assertIn("symlink", (err or "").lower())

    def test_payload_hash_verify_detects_bitflip(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        # Use real payload from repo
        hashes = pg.build_payload_manifest(g)
        # Install one file then corrupt
        src = pg.payload_dir() / "gimprc"
        dest = cfg / "gimprc"
        shutil.copy2(src, dest)
        data = bytearray(dest.read_bytes())
        data[0] = (data[0] + 1) % 256
        dest.write_bytes(bytes(data))
        problems = pg.verify_install(cfg, {"gimprc": hashes["gimprc"]}, g)
        self.assertTrue(any("hash mismatch" in p for p in problems))

    def test_install_payload_hashes_match(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        installed, backup = self._install_over_profile(cfg, g)
        problems = pg.verify_install(cfg, installed, g)
        self.assertEqual(problems, [])
        self.assertIn("shortcutsrc", installed)
        self.assertTrue((cfg / "shortcutsrc").is_file())

    def test_remove_without_hashes_is_noop(self) -> None:
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "shortcutsrc").write_text("user", encoding="utf-8")
        removed = pg.remove_photogimp_managed_files(cfg, expected_hashes=None)
        self.assertEqual(removed, [])
        self.assertTrue((cfg / "shortcutsrc").is_file())

    def test_remove_only_matching_hashes(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        installed = pg.install_payload(cfg, g)
        # User modifies one file
        p = cfg / "gimprc"
        p.write_text(p.read_text(encoding="utf-8") + "\n# user\n", encoding="utf-8")
        removed = pg.remove_photogimp_managed_files(cfg, expected_hashes=installed)
        self.assertNotIn("gimprc", removed)
        self.assertTrue(p.is_file())  # modified kept
        self.assertFalse((cfg / "shortcutsrc").exists())

    def test_backup_source_match(self) -> None:
        g = self._native()
        cfg_a = self.config_root / "3.0"
        cfg_a.mkdir()
        (cfg_a / "x").write_text("a", encoding="utf-8")
        b = pg.create_backup(cfg_a, reason="pre-install", gimp=g)
        self.assertIsNotNone(b)
        self.assertTrue(pg._backup_matches_config(b, cfg_a))
        cfg_b = self.config_root / "other"
        cfg_b.mkdir()
        self.assertFalse(pg._backup_matches_config(b, cfg_b))

    def test_eof_confirm_is_false(self) -> None:
        # confirm uses input; simulate EOF via monkeypatch
        def boom(_prompt=""):
            raise EOFError

        old = __builtins__["input"] if isinstance(__builtins__, dict) else input
        import builtins

        builtins.input = boom  # type: ignore
        try:
            self.assertFalse(pg.confirm("Destroy everything?", True))
        finally:
            builtins.input = old  # type: ignore

    def test_snap_refused(self) -> None:
        g = pg.GimpInfo(found=True, kind="snap", binary="snap", version="3.0.0")
        err = pg.validate_gimp3_config_target(g, self.config_root / "3.0")
        self.assertIsNotNone(err)
        self.assertIn("Snap", err or "")

    def test_preferred_unsupported_raises(self) -> None:
        g = self._native()
        with self.assertRaises(ValueError):
            pg.resolve_config_dir(g, preferred="3.2")

    def test_unprobed_always_refused(self) -> None:
        only = self.config_root / "3.0"
        only.mkdir()
        (only / "gimprc").write_text("(gimprc)", encoding="utf-8")
        g = self._native(None)
        g.version = None
        cfg = pg.resolve_config_dir(g)
        err = pg.validate_gimp3_config_target(g, cfg)
        self.assertIsNotNone(err)
        self.assertIn("Cannot determine GIMP version", err or "")

    def test_missing_gimprc_refused(self) -> None:
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        g = self._native("3.0.2")
        err = pg.validate_gimp3_config_target(g, cfg)
        self.assertIsNotNone(err)
        self.assertIn("gimprc", err or "")

    def test_status_with_registry_no_crash(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "gimprc").write_text("(gimprc)", encoding="utf-8")
        installed, backup = self._install_over_profile(cfg, g)
        st = pg.InstallState(
            backup_id=backup.name,
            config_path=str(cfg),
            installed_at="t",
            config_version="3.0",
            gimp_kind="native",
            gimp_version="3.0.2",
            installed_hashes=installed,
        )
        reg = pg.InstallRegistry()
        reg.installs = {}
        # Point state path into temp
        pg.state_path = lambda: self.tmp / "data" / "state.json"  # type: ignore
        (self.tmp / "data").mkdir(exist_ok=True)
        reg.upsert(st)
        # verify_install path used by status
        problems = pg.verify_install(cfg, st.installed_hashes, g)
        self.assertEqual(problems, [])

    def test_registry_multi_install_keys(self) -> None:
        pg.state_path = lambda: self.tmp / "data" / "state.json"  # type: ignore
        (self.tmp / "data").mkdir(exist_ok=True)
        reg = pg.InstallRegistry()
        a = pg.InstallState(config_path=str(self.tmp / "a" / "3.0"), gimp_kind="native")
        b = pg.InstallState(config_path=str(self.tmp / "b" / "3.0"), gimp_kind="flatpak")
        (self.tmp / "a" / "3.0").mkdir(parents=True)
        (self.tmp / "b" / "3.0").mkdir(parents=True)
        reg.upsert(a)
        reg.upsert(b)
        self.assertEqual(len(reg.all_states()), 2)
        reg.remove(str(self.tmp / "a" / "3.0"))
        self.assertEqual(len(reg.all_states()), 1)
        # Remaining profile untouched
        remaining = reg.all_states()[0]
        self.assertIn("b", remaining.config_path)

    def test_pgi001_status_with_state_uses_hash_dict(self) -> None:
        """Regression: status must not pass a list into verify_install.items()."""
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "gimprc").write_text("(gimprc)", encoding="utf-8")
        hashes, backup = self._install_over_profile(cfg, g)
        pg.clear_install_journal(cfg)
        pg.state_path = lambda: self.tmp / "data" / "state.json"  # type: ignore
        (self.tmp / "data").mkdir(exist_ok=True)
        st = pg.InstallState(
            backup_id=backup.name,
            config_path=str(cfg),
            gimp_kind="native",
            gimp_version="3.0.2",
            installed_hashes=hashes,
        )
        pg.InstallRegistry.load().upsert(st)
        # This is what status does — must not raise
        expected = st.installed_hashes or {}
        self.assertIsInstance(expected, dict)
        problems = pg.verify_install(cfg, expected, g)
        self.assertEqual(problems, [])
        code = pg.cmd_status()
        self.assertEqual(code, 0)

    def test_choose_install_filters_unsupported(self) -> None:
        installs = [
            pg.GimpInfo(found=True, kind="portable", binary="p"),
            pg.GimpInfo(found=True, kind="snap", binary="s"),
            pg.GimpInfo(found=True, kind="native", binary="/usr/bin/gimp", version="3.0.2"),
        ]
        old_confirm = pg.confirm
        pg.confirm = lambda *_args, **_kwargs: True  # type: ignore
        try:
            chosen = pg.choose_gimp_install(installs, for_install=True)
        finally:
            pg.confirm = old_confirm  # type: ignore
        self.assertIsNotNone(chosen)
        assert chosen is not None
        self.assertEqual(chosen.kind, "native")

    def test_vanilla_regression_stale_folder_wrong_version(self) -> None:
        """Probed 3.2 must not install into leftover 3.0 (false vanilla)."""
        (self.config_root / "3.0").mkdir()
        (self.config_root / "3.0" / "gimprc").write_text("(gimprc)", encoding="utf-8")
        g = self._native("3.2.1")
        cfg = pg.resolve_config_dir(g)
        self.assertEqual(cfg.name, "3.2")
        err = pg.validate_gimp3_config_target(g, cfg)
        self.assertIsNotNone(err)
        # Even if someone forces 3.0 target with 3.2 binary:
        err2 = pg.validate_gimp3_config_target(g, self.config_root / "3.0")
        self.assertIsNotNone(err2)

    def test_backup_is_sealed(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "a.txt").write_text("hello", encoding="utf-8")
        b = pg.create_backup(cfg, reason="manual", gimp=g)
        self.assertIsNotNone(b)
        assert b is not None
        self.assertTrue((b / "control" / "manifest.json").is_file())
        self.assertEqual(pg.verify_backup_integrity(b), [])
        # Corrupt sealed file
        (b / "profile" / "a.txt").write_text("evil", encoding="utf-8")
        problems = pg.verify_backup_integrity(b)
        self.assertTrue(any("hash mismatch" in p for p in problems))

    def test_journal_recovery_restores_backup(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "original.txt").write_text("orig", encoding="utf-8")
        b = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert b is not None
        # Simulate partial install
        (cfg / "shortcutsrc").write_text("partial", encoding="utf-8")
        pg.write_install_journal(
            cfg, backup_id=b.name, tops=["shortcutsrc"], phase="committing"
        )
        msg = pg.recover_incomplete_install(cfg)
        self.assertIsNotNone(msg)
        self.assertTrue((cfg / "original.txt").is_file())
        self.assertFalse((cfg / "shortcutsrc").exists())
        self.assertFalse(pg.journal_path(cfg).exists())

    def test_portable_refused(self) -> None:
        g = pg.GimpInfo(
            found=True,
            kind="portable",
            binary=r"C:\Users\x\Portable\gimp.exe",
            version="3.0.0",
        )
        err = pg.validate_gimp3_config_target(g, self.config_root / "3.0")
        self.assertIsNotNone(err)
        self.assertIn("Portable", err or "")

    def test_install_clears_journal_on_success(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "gimprc").write_text("stock", encoding="utf-8")
        backup = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert backup is not None
        installed = pg.install_payload(
            cfg, g, backup_id=backup.name, baseline_backup_id=backup.name
        )
        # journal left in verifying phase until caller clears — simulate clear
        if pg.journal_path(cfg).exists():
            pg.clear_install_journal(cfg)
        self.assertEqual(pg.verify_install(cfg, installed, g), [])
        self.assertFalse(pg.journal_path(cfg).exists())

    def test_backup_metadata_is_sealed(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "a.txt").write_text("hello", encoding="utf-8")
        b = pg.create_backup(cfg, reason="manual", gimp=g)
        assert b is not None
        meta_path = b / "control" / "metadata.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["source"] = str(self.tmp / "outside")
        meta_path.write_text(json.dumps(meta), encoding="utf-8")
        self.assertIn("backup metadata hash mismatch", pg.verify_backup_integrity(b))

    def test_backup_refuses_symlink(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        outside = self.tmp / "outside.txt"
        outside.write_text("secret", encoding="utf-8")
        try:
            (cfg / "linked.txt").symlink_to(outside)
        except OSError:
            self.skipTest("symlinks unavailable")
        self.assertIsNone(pg.create_backup(cfg, reason="manual", gimp=g))

    def test_malicious_journal_is_rejected_before_delete(self) -> None:
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        victim = self.tmp / "victim.txt"
        victim.write_text("safe", encoding="utf-8")
        pg.journal_path(cfg).parent.mkdir(parents=True)
        pg.journal_path(cfg).write_text(
            json.dumps(
                {
                    "phase": "committing",
                    "backup_id": "../../victim",
                    "tops": ["../../victim.txt"],
                    "installed_hashes": {},
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(OSError):
            pg.recover_incomplete_install(cfg)
        self.assertEqual(victim.read_text(encoding="utf-8"), "safe")
        self.assertTrue(pg.journal_path(cfg).exists())

    def test_corrupt_backup_blocks_journal_recovery(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "original.txt").write_text("orig", encoding="utf-8")
        b = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert b is not None
        (b / "profile" / "original.txt").write_text("corrupt", encoding="utf-8")
        pg.write_install_journal(
            cfg, backup_id=b.name, tops=["shortcutsrc"], phase="committing"
        )
        with self.assertRaises(OSError):
            pg.recover_incomplete_install(cfg)
        self.assertTrue(pg.journal_path(cfg).exists())

    def test_committed_journal_uses_own_hashes(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "gimprc").write_text("stock", encoding="utf-8")
        backup = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert backup is not None
        pg.install_payload(
            cfg, g, backup_id=backup.name, baseline_backup_id=backup.name
        )
        outcome = pg.recover_incomplete_install(cfg)
        self.assertIsNotNone(outcome)
        assert outcome is not None
        self.assertTrue(outcome.finalized_install)
        recorded = pg.InstallRegistry.load().get(str(cfg))
        self.assertIsNotNone(recorded)
        assert recorded is not None
        self.assertEqual(recorded.backup_id, backup.name)
        self.assertFalse(pg.journal_path(cfg).exists())

    def test_zero_selection_is_invalid(self) -> None:
        self.assertIsNone(pg.select_number("0", ["first", "last"]))
        self.assertIsNone(pg.select_number("-1", ["first", "last"]))
        self.assertEqual(pg.select_number("2", ["first", "last"]), "last")

    def test_payload_contract_classifies_every_file(self) -> None:
        pg.validate_payload_contract(pg.payload_dir())

    def test_xdg_config_home_is_used(self) -> None:
        old = os.environ.get("XDG_CONFIG_HOME")
        os.environ["XDG_CONFIG_HOME"] = str(self.tmp / "xdg-config")
        original_system = pg.platform.system
        try:
            fresh = load_installer()
            fresh.platform.system = lambda: "Linux"  # type: ignore
            g = fresh.GimpInfo(found=True, kind="native", version="3.0.2")
            self.assertEqual(
                fresh.gimp_config_root(g), (self.tmp / "xdg-config").resolve() / "GIMP"
            )
        finally:
            if old is None:
                os.environ.pop("XDG_CONFIG_HOME", None)
            else:
                os.environ["XDG_CONFIG_HOME"] = old
            pg.platform.system = original_system  # type: ignore

    def test_reinstall_preserves_original_uninstall_baseline(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "gimprc").write_text("stock", encoding="utf-8")
        baseline = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert baseline is not None

        pg.state_path = lambda: self.tmp / "data" / "state.json"  # type: ignore
        (self.tmp / "data").mkdir(exist_ok=True)
        reg = pg.InstallRegistry()
        reg.upsert(
            pg.InstallState(
                backup_id=baseline.name,
                config_path=str(cfg),
                gimp_kind="native",
                gimp_version="3.0.2",
            )
        )

        (cfg / "gimprc").write_text("photogimp", encoding="utf-8")
        upgrade = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert upgrade is not None
        selected = pg.uninstall_baseline_id(
            pg.InstallRegistry.load(), cfg, upgrade
        )
        self.assertEqual(selected, baseline.name)
        self.assertNotEqual(selected, upgrade.name)

    def test_process_search_command_is_not_gimp(self) -> None:
        fresh = load_installer()
        fresh.is_windows = lambda: False  # type: ignore
        fresh._trusted_system_tool = lambda name: "/usr/bin/ps" if name == "ps" else None  # type: ignore
        fresh.run = lambda _args, **_kwargs: fresh.subprocess.CompletedProcess(  # type: ignore
            args=_args,
            returncode=0,
            stdout="123 /bin/zsh -c ps ax | grep -i gimp\n124 grep -i gimp\n",
            stderr="",
        )
        self.assertEqual(fresh.gimp_process_state(), fresh.PROCESS_NOT_RUNNING)

    def test_planned_path_escape_is_refused(self) -> None:
        outside = self.tmp / "outside" / "3.0"
        problem = pg.validate_path_containment(outside, self.config_root)
        self.assertIsNotNone(problem)
        self.assertIn("outside GIMP root", problem or "")

    def test_relative_xdg_root_is_refused(self) -> None:
        old = os.environ.get("XDG_CONFIG_HOME")
        os.environ["XDG_CONFIG_HOME"] = ".config"
        fresh = load_installer()
        original_system = fresh.platform.system
        fresh.platform.system = lambda: "Linux"  # type: ignore
        try:
            problem = fresh.validate_environment_paths()
            self.assertIsNotNone(problem)
            self.assertIn("absolute path", problem or "")
        finally:
            if old is None:
                os.environ.pop("XDG_CONFIG_HOME", None)
            else:
                os.environ["XDG_CONFIG_HOME"] = old
            fresh.platform.system = original_system  # type: ignore

    def test_payload_source_cannot_be_live_target(self) -> None:
        g = self._native()
        problem = pg.validate_gimp3_config_target(g, pg.payload_dir())
        self.assertIsNotNone(problem)
        self.assertIn("repository payload", problem or "")

    def test_snap_wrapper_is_not_native(self) -> None:
        self.assertTrue(pg._is_snap_executable("/snap/bin/gimp"))
        self.assertTrue(pg._is_snap_executable("/var/lib/snapd/snap/bin/gimp"))

    def test_windows_portable_scanner_does_not_crash(self) -> None:
        root = self.tmp / "Downloads"
        exe = root / "GIMPPortable" / "App" / "bin" / "gimp.exe"
        exe.parent.mkdir(parents=True)
        exe.write_bytes(b"MZ")
        (root / "GIMPPortable" / "Data").mkdir()
        old_windows = pg.is_windows
        pg.is_windows = lambda: True  # type: ignore
        try:
            hits = pg._detect_windows_portable_candidates(set(), [root])
        finally:
            pg.is_windows = old_windows  # type: ignore
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].kind, "portable")
        self.assertEqual(hits[0].app_path, str(exe.parent))

    def test_backup_control_names_are_preserved(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        nested = cfg / "plugin"
        nested.mkdir(parents=True)
        (cfg / "backup-meta.json").write_text("root-user-data", encoding="utf-8")
        (nested / "backup-manifest.json").write_text("nested-user-data", encoding="utf-8")
        backup = pg.create_backup(cfg, reason="manual", gimp=g)
        assert backup is not None
        (cfg / "backup-meta.json").write_text("changed", encoding="utf-8")
        (nested / "backup-manifest.json").unlink()
        pg.restore_backup(backup, cfg, gimp=g)
        self.assertEqual((cfg / "backup-meta.json").read_text(), "root-user-data")
        self.assertEqual(
            (nested / "backup-manifest.json").read_text(), "nested-user-data"
        )

    def test_malformed_backup_manifest_is_rejected(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "x").write_text("x", encoding="utf-8")
        backup = pg.create_backup(cfg, reason="manual", gimp=g)
        assert backup is not None
        manifest_path = backup / "control" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["entries"] = {}
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(pg.verify_backup_integrity(backup))
        with self.assertRaises(OSError):
            pg.restore_backup(backup, cfg, gimp=g)

    def test_symlink_added_to_sealed_backup_is_rejected(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "x").write_text("x", encoding="utf-8")
        backup = pg.create_backup(cfg, reason="manual", gimp=g)
        assert backup is not None
        outside = self.tmp / "outside"
        outside.write_text("outside", encoding="utf-8")
        try:
            (backup / "profile" / "link").symlink_to(outside)
        except OSError:
            self.skipTest("symlinks unavailable")
        problems = pg.verify_backup_integrity(backup)
        self.assertTrue(any("link" in problem.lower() for problem in problems))

    @unittest.skipUnless(os.name == "posix", "POSIX mode semantics")
    def test_backup_restore_preserves_directory_mode(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        private = cfg / "private"
        private.mkdir(parents=True)
        private.chmod(0o711)
        backup = pg.create_backup(cfg, reason="manual", gimp=g)
        assert backup is not None
        private.chmod(0o755)
        pg.restore_backup(backup, cfg, gimp=g)
        self.assertEqual(stat.S_IMODE(private.stat().st_mode), 0o711)

    def test_keyboard_interrupt_during_swap_restores_original(self) -> None:
        src = self.tmp / "new"
        dest = self.tmp / "target"
        src.mkdir()
        dest.mkdir()
        (src / "value").write_text("new", encoding="utf-8")
        (dest / "value").write_text("old", encoding="utf-8")
        original_rename = Path.rename

        def interrupted(path_self, target):
            if path_self.name.startswith(".photogimp-new-") and Path(target) == dest:
                raise KeyboardInterrupt
            return original_rename(path_self, target)

        with mock.patch.object(Path, "rename", interrupted):
            with self.assertRaises(KeyboardInterrupt):
                pg.replace_tree_atomic(src, dest)
        self.assertEqual((dest / "value").read_text(), "old")
        self.assertFalse(pg._replace_journal_path(dest).exists())

    def test_cross_target_journal_backup_is_rejected(self) -> None:
        g = self._native()
        cfg_a = self.config_root / "3.0"
        cfg_a.mkdir()
        (cfg_a / "a").write_text("a", encoding="utf-8")
        backup = pg.create_backup(cfg_a, reason="pre-install", gimp=g)
        assert backup is not None
        cfg_b = self.tmp / "OtherGIMP" / "3.0"
        cfg_b.mkdir(parents=True)
        (cfg_b / "b").write_text("b", encoding="utf-8")
        pg.write_install_journal(
            cfg_b, backup_id=backup.name, tops=["gimprc"], phase="committing"
        )
        with self.assertRaises(OSError):
            pg.recover_incomplete_install(cfg_b)
        self.assertEqual((cfg_b / "b").read_text(), "b")

    def test_registry_stale_writers_merge(self) -> None:
        first = pg.InstallRegistry.load()
        second = pg.InstallRegistry.load()
        a_path = self.tmp / "a" / "3.0"
        b_path = self.tmp / "b" / "3.0"
        a_path.mkdir(parents=True)
        b_path.mkdir(parents=True)
        first.upsert(pg.InstallState(config_path=str(a_path), gimp_kind="native"))
        second.upsert(pg.InstallState(config_path=str(b_path), gimp_kind="flatpak"))
        self.assertEqual(len(pg.InstallRegistry.load().all_states()), 2)

    def test_process_inspection_unknown_fails_closed(self) -> None:
        pg.gimp_process_state = lambda: pg.PROCESS_UNKNOWN  # type: ignore
        self.assertEqual(pg.preflight_gimp_closed(), pg.EXIT_PREFLIGHT)

    def test_profile_change_after_backup_aborts_install(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "gimprc").write_text("stock", encoding="utf-8")
        backup = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert backup is not None
        (cfg / "concurrent").write_text("change", encoding="utf-8")
        with self.assertRaises(OSError):
            pg.install_payload(
                cfg,
                g,
                backup_id=backup.name,
                baseline_backup_id=backup.name,
            )
        self.assertEqual((cfg / "gimprc").read_text(), "stock")

    def test_uninstall_managed_restore_preserves_new_brush(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "gimprc").write_text("stock", encoding="utf-8")
        hashes, backup = self._install_over_profile(cfg, g)
        brushes = cfg / "brushes"
        brushes.mkdir()
        (brushes / "user.gbr").write_text("brush", encoding="utf-8")
        restored, remaining = pg.restore_managed_from_backup(backup, cfg, hashes)
        self.assertTrue(restored)
        self.assertEqual(remaining, {})
        self.assertEqual((cfg / "gimprc").read_text(), "stock")
        self.assertEqual((brushes / "user.gbr").read_text(), "brush")

    def test_payload_manifest_detects_missing_required_file(self) -> None:
        copied = self.tmp / "payload"
        shutil.copytree(pg.payload_dir(), copied)
        (copied / "splashes" / "splash-screen-2025-v2.png").unlink()
        with self.assertRaises(FileNotFoundError):
            pg.validate_payload_contract(copied)

    def test_symlinked_backup_root_is_refused_without_chmod(self) -> None:
        data = self.tmp / "data"
        data.mkdir()
        outside = self.tmp / "outside-backups"
        outside.mkdir()
        outside.chmod(0o755)
        original_mode = stat.S_IMODE(outside.stat().st_mode)
        link = data / "backups"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("symlinks unavailable")
        pg.data_home = lambda: data  # type: ignore
        pg.backups_dir = lambda: link  # type: ignore
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        self.assertIsNone(pg.create_backup(cfg, reason="manual", gimp=self._native()))
        self.assertEqual(stat.S_IMODE(outside.stat().st_mode), original_mode)

    def test_tampered_state_backup_id_is_invalid_registry(self) -> None:
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        path = pg.state_path()
        path.parent.mkdir(parents=True)
        state = pg.InstallState(
            backup_id="../outside",
            config_path=str(cfg),
            gimp_kind="native",
        )
        path.write_text(
            json.dumps({"version": 2, "installs": {str(cfg.resolve()): state.__dict__}}),
            encoding="utf-8",
        )
        self.assertTrue(pg.InstallRegistry.load().errors)

    def test_status_does_not_probe_discovered_executable(self) -> None:
        old_detect = pg.detect_all_gimp_installs
        old_probe = pg.probe_gimp_version
        pg.detect_all_gimp_installs = lambda: [  # type: ignore
            pg.GimpInfo(found=True, kind="native", binary="/tmp/untrusted-gimp")
        ]
        pg.probe_gimp_version = lambda _gimp: (_ for _ in ()).throw(AssertionError("executed"))  # type: ignore
        try:
            self.assertEqual(pg.cmd_status(), pg.EXIT_OK)
        finally:
            pg.detect_all_gimp_installs = old_detect  # type: ignore
            pg.probe_gimp_version = old_probe  # type: ignore

    def test_failed_rollback_retains_install_journal(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "gimprc").write_text("stock", encoding="utf-8")
        backup = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert backup is not None
        pg.write_install_journal(
            cfg,
            backup_id=backup.name,
            baseline_backup_id=backup.name,
            tops=["gimprc"],
            phase="committing",
            gimp=g,
        )
        old_replace = pg._replace_from_verified_backup
        pg._replace_from_verified_backup = lambda *_args: (_ for _ in ()).throw(  # type: ignore
            OSError("disk full")
        )
        try:
            self.assertFalse(pg._rollback_install(backup, cfg, g, was_empty=False))
        finally:
            pg._replace_from_verified_backup = old_replace  # type: ignore
        self.assertTrue(pg.journal_path(cfg).is_file())

    def test_status_hash_failure_is_nonzero(self) -> None:
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "gimprc").write_text("changed", encoding="utf-8")
        pg.InstallRegistry().upsert(
            pg.InstallState(
                config_path=str(cfg),
                gimp_kind="native",
                gimp_version="3.0.2",
                installed_hashes={"gimprc": "0" * 64},
            )
        )
        self.assertEqual(pg.cmd_status(), pg.EXIT_ERROR)

    def test_existing_live_operation_lock_is_rejected(self) -> None:
        target = self.config_root / "3.0"
        with pg.operation_lock("profile", target):
            held = set(pg._held_locks)
            pg._held_locks.clear()
            try:
                with self.assertRaises(OSError):
                    with pg.operation_lock("profile", target):
                        pass
            finally:
                pg._held_locks.update(held)

    def test_elevated_execution_is_refused(self) -> None:
        pg.is_elevated = lambda: True  # type: ignore
        self.assertEqual(pg.preflight_execution_context(), pg.EXIT_PREFLIGHT)

    def test_detect_gimp_without_candidates_does_not_crash(self) -> None:
        old_detect = pg.detect_all_gimp_installs
        pg.detect_all_gimp_installs = lambda: []  # type: ignore
        try:
            detected = pg.detect_gimp()
        finally:
            pg.detect_all_gimp_installs = old_detect  # type: ignore
        self.assertFalse(detected.found)

    def test_platform_config_roots(self) -> None:
        old_windows = pg.is_windows
        old_macos = pg.is_macos
        old_appdata = os.environ.get("APPDATA")
        try:
            pg.is_windows = lambda: True  # type: ignore
            pg.is_macos = lambda: False  # type: ignore
            os.environ["APPDATA"] = str(self.tmp / "Roaming")
            self.assertEqual(
                real_gimp_config_root(self._native()),
                (self.tmp / "Roaming").resolve() / "GIMP",
            )

            pg.is_windows = lambda: False  # type: ignore
            pg.is_macos = lambda: True  # type: ignore
            self.assertEqual(
                real_gimp_config_root(self._native()),
                pg.user_home() / "Library" / "Application Support" / "GIMP",
            )

            pg.is_macos = lambda: False  # type: ignore
            flatpak = pg.GimpInfo(found=True, kind="flatpak", version="3.0.2")
            self.assertEqual(
                real_gimp_config_root(flatpak),
                pg.user_home()
                / ".var"
                / "app"
                / pg.FLATHUB_GIMP_ID
                / "config"
                / "GIMP",
            )
        finally:
            pg.is_windows = old_windows  # type: ignore
            pg.is_macos = old_macos  # type: ignore
            if old_appdata is None:
                os.environ.pop("APPDATA", None)
            else:
                os.environ["APPDATA"] = old_appdata

    def test_all_written_install_journal_phases_are_loadable(self) -> None:
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        for phase in ("prepared", "activating", "committing", "committed"):
            pg.write_install_journal(
                cfg,
                backup_id="",
                tops=["gimprc"],
                phase=phase,
            )
            self.assertEqual(pg._load_install_journal(cfg)["phase"], phase)

    def test_prepared_journal_recovery_preserves_profile(self) -> None:
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        current = cfg / "current.txt"
        current.write_text("user data", encoding="utf-8")
        pg.write_install_journal(
            cfg,
            backup_id="",
            tops=["gimprc"],
            phase="prepared",
        )
        outcome = pg.recover_incomplete_install(cfg)
        self.assertIsNotNone(outcome)
        self.assertEqual(current.read_text(encoding="utf-8"), "user data")
        self.assertFalse(pg.journal_path(cfg).exists())

    def test_activating_journal_can_finalize_verified_install(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "gimprc").write_text("stock", encoding="utf-8")
        backup = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert backup is not None
        installed = pg.install_payload(
            cfg,
            g,
            backup_id=backup.name,
            baseline_backup_id=backup.name,
        )
        pg.write_install_journal(
            cfg,
            backup_id=backup.name,
            baseline_backup_id=backup.name,
            tops=sorted({rel.split("/", 1)[0] for rel in installed}),
            phase="activating",
            installed_hashes=installed,
            gimp=g,
        )
        outcome = pg.recover_incomplete_install(cfg)
        self.assertIsNotNone(outcome)
        assert outcome is not None
        self.assertTrue(outcome.finalized_install)

    def test_concurrent_change_after_original_rename_is_restored(self) -> None:
        dest = self.config_root / "3.0"
        dest.mkdir()
        original = dest / "original.txt"
        original.write_text("original", encoding="utf-8")
        approved = pg._tree_entries(dest)
        src = self.tmp / "new-profile"
        src.mkdir()
        (src / "new.txt").write_text("new", encoding="utf-8")
        real_write = pg._atomic_write_json
        changed = False

        def write_and_change(path, payload):
            nonlocal changed
            real_write(path, payload)
            if payload.get("phase") == "old-moved" and not changed:
                changed = True
                (Path(payload["old_path"]) / "late.txt").write_text(
                    "concurrent", encoding="utf-8"
                )

        with mock.patch.object(pg, "_atomic_write_json", side_effect=write_and_change):
            with self.assertRaises(OSError):
                pg.replace_tree_atomic(
                    src,
                    dest,
                    expected_dest_entries=approved,
                    expected_dest_exists=True,
                )

        self.assertEqual(original.read_text(encoding="utf-8"), "original")
        self.assertEqual((dest / "late.txt").read_text(encoding="utf-8"), "concurrent")
        self.assertFalse((dest / "new.txt").exists())
        self.assertFalse(pg._replace_journal_path(dest).exists())

    def test_replacement_recovery_rejects_untrusted_old_identity(self) -> None:
        dest = self.config_root / "3.0"
        dest.mkdir()
        (dest / "current.txt").write_text("current", encoding="utf-8")
        expected = pg._tree_entries(dest)
        token = "a" * 32
        old = dest.parent / f".photogimp-old-{token}"
        old.mkdir()
        (old / "victim.txt").write_text("preserve", encoding="utf-8")
        pg._replace_journal_path(dest).write_text(
            json.dumps(
                {
                    "version": 1,
                    "transaction_id": token,
                    "target": str(dest.resolve()),
                    "new_path": str(dest.parent / f".photogimp-new-{token}"),
                    "old_path": str(old),
                    "retired_path": str(dest.parent / f".photogimp-retired-{token}"),
                    "had_dest": True,
                    "phase": "activated",
                    "expected_entries": expected,
                    "new_identity": pg._directory_identity(dest),
                    "original_entries": expected,
                    "original_identity": {"device": -1, "inode": -1},
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(OSError, "identity is not trusted"):
            pg.recover_replace_transaction(dest)
        self.assertEqual((dest / "current.txt").read_text(encoding="utf-8"), "current")
        self.assertEqual((old / "victim.txt").read_text(encoding="utf-8"), "preserve")

    def test_malformed_replacement_path_type_is_a_safe_error(self) -> None:
        dest = self.config_root / "3.0"
        dest.mkdir()
        current = dest / "current.txt"
        current.write_text("preserve", encoding="utf-8")
        token = "b" * 32
        pg._replace_journal_path(dest).write_text(
            json.dumps(
                {
                    "version": 1,
                    "transaction_id": token,
                    "target": str(dest.resolve()),
                    "new_path": [],
                    "old_path": str(dest.parent / f".photogimp-old-{token}"),
                    "retired_path": str(dest.parent / f".photogimp-retired-{token}"),
                    "had_dest": True,
                    "phase": "prepared",
                    "expected_entries": pg._tree_entries(dest),
                    "new_identity": pg._directory_identity(dest),
                    "original_entries": pg._tree_entries(dest),
                    "original_identity": pg._directory_identity(dest),
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(OSError, "paths must be strings"):
            pg.recover_replace_transaction(dest)
        self.assertEqual(current.read_text(encoding="utf-8"), "preserve")

    def test_partial_old_tree_is_retired_not_restored_over_committed_tree(self) -> None:
        dest = self.config_root / "3.0"
        dest.mkdir()
        (dest / "new.txt").write_text("committed", encoding="utf-8")
        expected = pg._tree_entries(dest)
        token = "c" * 32
        old = dest.parent / f".photogimp-old-{token}"
        retired = dest.parent / f".photogimp-retired-{token}"
        old.mkdir()
        (old / "one.txt").write_text("one", encoding="utf-8")
        (old / "two.txt").write_text("two", encoding="utf-8")
        original = pg._tree_entries(old)
        identity = pg._directory_identity(old)
        (old / "two.txt").unlink()
        pg._replace_journal_path(dest).write_text(
            json.dumps(
                {
                    "version": 1,
                    "transaction_id": token,
                    "target": str(dest.resolve()),
                    "new_path": str(dest.parent / f".photogimp-new-{token}"),
                    "old_path": str(old),
                    "retired_path": str(retired),
                    "had_dest": True,
                    "phase": "new-committed",
                    "expected_entries": expected,
                    "new_identity": pg._directory_identity(dest),
                    "original_entries": original,
                    "original_identity": identity,
                }
            ),
            encoding="utf-8",
        )
        outcome = pg.recover_replace_transaction(dest)
        self.assertIsNotNone(outcome)
        self.assertEqual((dest / "new.txt").read_text(encoding="utf-8"), "committed")
        self.assertEqual((retired / "one.txt").read_text(encoding="utf-8"), "one")
        self.assertFalse((retired / "two.txt").exists())

    def test_late_write_to_displaced_tree_is_retained(self) -> None:
        dest = self.config_root / "3.0"
        dest.mkdir()
        (dest / "original.txt").write_text("original", encoding="utf-8")
        approved = pg._tree_entries(dest)
        src = self.tmp / "replacement"
        src.mkdir()
        (src / "new.txt").write_text("new", encoding="utf-8")
        real_write = pg._atomic_write_json
        changed = False

        def write_and_change(path, payload):
            nonlocal changed
            real_write(path, payload)
            if payload.get("phase") == "new-committed" and not changed:
                changed = True
                (Path(payload["old_path"]) / "late.txt").write_text(
                    "late user write", encoding="utf-8"
                )

        with mock.patch.object(pg, "_atomic_write_json", side_effect=write_and_change):
            pg.replace_tree_atomic(
                src,
                dest,
                expected_dest_entries=approved,
                expected_dest_exists=True,
            )
        retired = list(dest.parent.glob(".photogimp-retired-*"))
        self.assertEqual(len(retired), 1)
        self.assertEqual((dest / "new.txt").read_text(encoding="utf-8"), "new")
        self.assertEqual(
            (retired[0] / "late.txt").read_text(encoding="utf-8"),
            "late user write",
        )

    def test_prepared_replacement_preserves_concurrently_changed_live_tree(self) -> None:
        dest = self.config_root / "3.0"
        dest.mkdir()
        current = dest / "current.txt"
        current.write_text("original", encoding="utf-8")
        approved = pg._tree_entries(dest)
        src = self.tmp / "prepared-new"
        src.mkdir()
        (src / "new.txt").write_text("new", encoding="utf-8")
        real_write = pg._atomic_write_json
        changed = False

        def write_and_change(path, payload):
            nonlocal changed
            real_write(path, payload)
            if payload.get("phase") == "prepared" and not changed:
                changed = True
                current.write_text("concurrent", encoding="utf-8")

        with mock.patch.object(pg, "_atomic_write_json", side_effect=write_and_change):
            with self.assertRaises(OSError):
                pg.replace_tree_atomic(
                    src,
                    dest,
                    expected_dest_entries=approved,
                    expected_dest_exists=True,
                )
        self.assertEqual(current.read_text(encoding="utf-8"), "concurrent")
        self.assertFalse(pg._replace_journal_path(dest).exists())
        self.assertEqual(len(list(dest.parent.glob(".photogimp-new-*"))), 1)

    def test_rollback_retains_changed_activated_tree(self) -> None:
        dest = self.config_root / "3.0"
        dest.mkdir()
        original = dest / "original.txt"
        original.write_text("original", encoding="utf-8")
        approved = pg._tree_entries(dest)
        src = self.tmp / "activated-new"
        src.mkdir()
        (src / "new.txt").write_text("new", encoding="utf-8")
        real_write = pg._atomic_write_json
        changed = False

        def write_and_change(path, payload):
            nonlocal changed
            real_write(path, payload)
            if payload.get("phase") == "activated" and not changed:
                changed = True
                (dest / "late.txt").write_text("concurrent", encoding="utf-8")

        with mock.patch.object(pg, "_atomic_write_json", side_effect=write_and_change):
            with self.assertRaises(OSError):
                pg.replace_tree_atomic(
                    src,
                    dest,
                    expected_dest_entries=approved,
                    expected_dest_exists=True,
                )
        self.assertEqual(original.read_text(encoding="utf-8"), "original")
        retained = list(dest.parent.glob(".photogimp-new-*"))
        self.assertEqual(len(retained), 1)
        self.assertEqual(
            (retained[0] / "late.txt").read_text(encoding="utf-8"),
            "concurrent",
        )

    def test_post_commit_write_does_not_block_recovery(self) -> None:
        dest = self.config_root / "3.0"
        dest.mkdir()
        current = dest / "new.txt"
        current.write_text("committed", encoding="utf-8")
        expected = pg._tree_entries(dest)
        new_identity = pg._directory_identity(dest)
        current.write_text("post-commit", encoding="utf-8")
        token = "d" * 32
        pg._replace_journal_path(dest).write_text(
            json.dumps(
                {
                    "version": 1,
                    "transaction_id": token,
                    "target": str(dest.resolve()),
                    "new_path": str(dest.parent / f".photogimp-new-{token}"),
                    "old_path": str(dest.parent / f".photogimp-old-{token}"),
                    "retired_path": str(dest.parent / f".photogimp-retired-{token}"),
                    "had_dest": False,
                    "phase": "new-committed",
                    "expected_entries": expected,
                    "new_identity": new_identity,
                    "original_entries": None,
                    "original_identity": None,
                }
            ),
            encoding="utf-8",
        )
        outcome = pg.recover_replace_transaction(dest)
        self.assertIsNotNone(outcome)
        self.assertEqual(current.read_text(encoding="utf-8"), "post-commit")
        self.assertFalse(pg._replace_journal_path(dest).exists())

    def test_unhashable_replacement_phase_is_a_safe_error(self) -> None:
        dest = self.config_root / "3.0"
        dest.mkdir()
        current = dest / "current.txt"
        current.write_text("preserve", encoding="utf-8")
        token = "e" * 32
        pg._replace_journal_path(dest).write_text(
            json.dumps(
                {
                    "version": 1,
                    "transaction_id": token,
                    "target": str(dest.resolve()),
                    "phase": [],
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(OSError):
            pg.recover_replace_transaction(dest)
        self.assertEqual(current.read_text(encoding="utf-8"), "preserve")

    def test_rollback_crash_state_restores_old_and_keeps_modified_new(self) -> None:
        dest = self.config_root / "3.0"
        token = "f" * 32
        old = dest.parent / f".photogimp-old-{token}"
        new = dest.parent / f".photogimp-new-{token}"
        retired = dest.parent / f".photogimp-retired-{token}"
        old.mkdir()
        (old / "original.txt").write_text("original", encoding="utf-8")
        original = pg._tree_entries(old)
        original_identity = pg._directory_identity(old)
        new.mkdir()
        changed = new / "new.txt"
        changed.write_text("activated", encoding="utf-8")
        expected = pg._tree_entries(new)
        new_identity = pg._directory_identity(new)
        changed.write_text("concurrent", encoding="utf-8")
        pg._replace_journal_path(dest).write_text(
            json.dumps(
                {
                    "version": 1,
                    "transaction_id": token,
                    "target": str(dest.resolve()),
                    "new_path": str(new),
                    "old_path": str(old),
                    "retired_path": str(retired),
                    "had_dest": True,
                    "phase": "activated",
                    "expected_entries": expected,
                    "new_identity": new_identity,
                    "original_entries": original,
                    "original_identity": original_identity,
                }
            ),
            encoding="utf-8",
        )
        outcome = pg.recover_replace_transaction(dest)
        self.assertIsNotNone(outcome)
        self.assertEqual(
            (dest / "original.txt").read_text(encoding="utf-8"), "original"
        )
        self.assertEqual(changed.read_text(encoding="utf-8"), "concurrent")
        self.assertFalse(pg._replace_journal_path(dest).exists())

    def test_replacement_rejects_linked_parent(self) -> None:
        real_parent = self.tmp / "real-parent"
        real_parent.mkdir()
        linked_parent = self.tmp / "linked-parent"
        try:
            linked_parent.symlink_to(real_parent, target_is_directory=True)
        except OSError:
            self.skipTest("directory symlinks unavailable")
        src = self.tmp / "source-profile"
        src.mkdir()
        (src / "new.txt").write_text("new", encoding="utf-8")
        with self.assertRaisesRegex(OSError, "linked parent path"):
            pg.replace_tree_atomic(src, linked_parent / "3.0")
        self.assertFalse((real_parent / "3.0").exists())

    def test_symlink_loop_in_replacement_record_is_a_safe_error(self) -> None:
        dest = self.config_root / "3.0"
        dest.mkdir()
        current = dest / "current.txt"
        current.write_text("preserve", encoding="utf-8")
        loop = self.tmp / "loop"
        try:
            loop.symlink_to(loop, target_is_directory=True)
        except OSError:
            self.skipTest("symlinks unavailable")
        token = "1" * 32
        pg._replace_journal_path(dest).write_text(
            json.dumps(
                {
                    "version": 1,
                    "transaction_id": token,
                    "target": str(dest.resolve()),
                    "phase": "prepared",
                    "new_path": str(loop / f".photogimp-new-{token}"),
                    "old_path": str(dest.parent / f".photogimp-old-{token}"),
                    "retired_path": str(dest.parent / f".photogimp-retired-{token}"),
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(OSError):
            pg.recover_replace_transaction(dest)
        self.assertEqual(current.read_text(encoding="utf-8"), "preserve")

    def test_recovery_refuses_profile_mutation_while_gimp_runs(self) -> None:
        g = self._native()
        cfg = self.config_root / "3.0"
        cfg.mkdir()
        (cfg / "original.txt").write_text("original", encoding="utf-8")
        backup = pg.create_backup(cfg, reason="pre-install", gimp=g)
        assert backup is not None
        (cfg / "partial.txt").write_text("partial", encoding="utf-8")
        pg.write_install_journal(
            cfg,
            backup_id=backup.name,
            tops=["gimprc"],
            phase="committing",
            gimp=g,
        )
        pg.gimp_process_state = lambda: pg.PROCESS_RUNNING  # type: ignore
        with self.assertRaisesRegex(OSError, "refusing profile mutation"):
            pg.recover_incomplete_install(cfg)
        self.assertEqual((cfg / "partial.txt").read_text(encoding="utf-8"), "partial")
        self.assertTrue(pg.journal_path(cfg).exists())

    def test_windows_directory_flush_requests_write_access(self) -> None:
        import ctypes

        create_file = mock.Mock(return_value=123)
        kernel32 = mock.Mock()
        kernel32.CreateFileW = create_file
        kernel32.FlushFileBuffers.return_value = 1
        fake_windll = mock.Mock(kernel32=kernel32)
        with mock.patch.object(pg.os, "name", "nt"), mock.patch.object(
            pg, "is_windows", return_value=True
        ), mock.patch.object(ctypes, "windll", fake_windll, create=True):
            pg._fsync_directory(self.tmp)
        self.assertEqual(create_file.call_args.args[1], 0x40000000)

    def test_windows_file_flush_opens_a_writable_descriptor(self) -> None:
        path = self.tmp / "flush.txt"
        path.write_text("flush", encoding="utf-8")
        with mock.patch.object(pg, "is_windows", return_value=True), mock.patch.object(
            pg.os, "open", return_value=42
        ) as open_file, mock.patch.object(pg.os, "fsync") as fsync_file, mock.patch.object(
            pg.os, "close"
        ):
            pg._fsync_file(path)
        self.assertEqual(open_file.call_args.args[1], os.O_RDWR)
        fsync_file.assert_called_once_with(42)


if __name__ == "__main__":
    unittest.main()
