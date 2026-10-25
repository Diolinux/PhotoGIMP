from __future__ import annotations

import hashlib
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import Union
import unittest
from unittest.mock import patch
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import package_release  # noqa: E402


def write_file(path: Path, content: Union[bytes, str] = b"content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        path.write_text(content, encoding="utf-8")
    else:
        path.write_bytes(content)


class PackageReleaseTests(unittest.TestCase):
    def create_repository(self, root: Path) -> Path:
        config = root / ".config" / "GIMP" / "3.0"
        write_file(config / "gimprc", "(single-window-mode yes)\n")
        write_file(config / "tool-options" / "gimp-paintbrush-tool")
        write_file(
            root / ".local" / "share" / "applications" / "org.gimp.GIMP.desktop",
            "[Desktop Entry]\nName=PhotoGIMP\n",
        )
        write_file(
            root / ".local" / "share" / "icons" / "hicolor" / "64x64" / "apps" / "photogimp.png",
            b"png-data",
        )
        write_file(root / "install.sh", "#!/usr/bin/env bash\n")
        return config

    def repository_patches(self, root: Path):
        return patch.multiple(
            package_release,
            ROOT=root,
            CONFIG_ROOT=root / ".config" / "GIMP",
            LINUX_DESKTOP=root / ".local" / "share" / "applications" / "org.gimp.GIMP.desktop",
            LINUX_ICONS=root / ".local" / "share" / "icons",
        )

    def test_discover_config_returns_the_only_version(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = self.create_repository(root)

            with self.repository_patches(root):
                version, discovered = package_release.discover_config()

            self.assertEqual(version, "3.0")
            self.assertEqual(discovered, config)

    def test_discover_config_rejects_zero_or_multiple_versions(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            config_root = root / ".config" / "GIMP"
            config_root.mkdir(parents=True)

            with self.repository_patches(root):
                with self.assertRaisesRegex(SystemExit, "found: none"):
                    package_release.discover_config()

                (config_root / "2.10").mkdir()
                (config_root / "3.0").mkdir()
                with self.assertRaisesRegex(SystemExit, "found: 2.10, 3.0"):
                    package_release.discover_config()

    def test_platform_archives_have_the_expected_layout_and_metadata(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = self.create_repository(root)
            linux_archive = root / "linux.zip"
            windows_archive = root / "windows.zip"

            with self.repository_patches(root):
                package_release.build_archive(linux_archive, "linux", "3.0", config)
                package_release.build_archive(windows_archive, "windows", "3.0", config)

            with ZipFile(linux_archive) as archive:
                self.assertEqual(
                    archive.namelist(),
                    [
                        "PhotoGIMP-linux/.config/GIMP/3.0/gimprc",
                        "PhotoGIMP-linux/.config/GIMP/3.0/tool-options/gimp-paintbrush-tool",
                        "PhotoGIMP-linux/.local/share/applications/org.gimp.GIMP.desktop",
                        "PhotoGIMP-linux/.local/share/icons/hicolor/64x64/apps/photogimp.png",
                        "PhotoGIMP-linux/install.sh",
                    ],
                )
                self.assertTrue(all(item.date_time == package_release.FIXED_TIME for item in archive.infolist()))
                self.assertIsNone(archive.testzip())

            with ZipFile(windows_archive) as archive:
                self.assertEqual(
                    archive.namelist(),
                    ["3.0/gimprc", "3.0/tool-options/gimp-paintbrush-tool"],
                )
                self.assertIsNone(archive.testzip())

    def test_archives_are_reproducible(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = self.create_repository(root)
            first = root / "first.zip"
            second = root / "second.zip"

            with self.repository_patches(root):
                package_release.build_archive(first, "linux", "3.0", config)
                package_release.build_archive(second, "linux", "3.0", config)

            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_gimp_plugin_entrypoint_is_executable_in_archives(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = self.create_repository(root)
            plugin = config / "plug-ins" / "sample" / "sample.py"
            helper = config / "plug-ins" / "sample" / "helper.py"
            bytecode = (
                config
                / "plug-ins"
                / "sample"
                / "__pycache__"
                / "helper.cpython-312.pyc"
            )
            write_file(plugin, "#!/usr/bin/env python3\n")
            write_file(helper, "VALUE = 1\n")
            write_file(bytecode, b"generated-bytecode")
            archive_path = root / "linux.zip"

            with self.repository_patches(root):
                package_release.build_archive(
                    archive_path, "linux", "3.0", config
                )

            with ZipFile(archive_path) as archive:
                prefix = "PhotoGIMP-linux/.config/GIMP/3.0/plug-ins/sample/"
                plugin_mode = archive.getinfo(prefix + "sample.py").external_attr >> 16
                helper_mode = archive.getinfo(prefix + "helper.py").external_attr >> 16
                self.assertFalse(
                    any("__pycache__" in name for name in archive.namelist())
                )

            self.assertEqual(plugin_mode & 0o111, 0o111)
            self.assertEqual(helper_mode & 0o111, 0)

    def test_main_builds_all_archives_and_matching_checksums(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.create_repository(root)
            output = root / "release"

            with self.repository_patches(root), patch.object(
                sys, "argv", ["package_release.py", "--output", str(output)]
            ):
                package_release.main()

            expected_names = {
                "PhotoGIMP-linux.zip",
                "PhotoGIMP-windows.zip",
                "PhotoGIMP-macos.zip",
            }
            self.assertEqual(
                {path.name for path in output.glob("*.zip")},
                expected_names,
            )

            checksum_lines = (output / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
            checksums = dict(line.split("  ", 1)[::-1] for line in checksum_lines)
            self.assertEqual(set(checksums), expected_names)
            for name, expected_digest in checksums.items():
                actual_digest = hashlib.sha256((output / name).read_bytes()).hexdigest()
                self.assertEqual(actual_digest, expected_digest)

    def test_repository_payload_can_be_packaged(self) -> None:
        with TemporaryDirectory() as temporary, patch.object(
            sys,
            "argv",
            ["package_release.py", "--output", temporary],
        ):
            package_release.main()

            for name in (
                "PhotoGIMP-linux.zip",
                "PhotoGIMP-windows.zip",
                "PhotoGIMP-macos.zip",
            ):
                with ZipFile(Path(temporary) / name) as archive:
                    members = archive.namelist()
                    self.assertTrue(members)
                    self.assertTrue(
                        all(
                            not member.startswith("/") and ".." not in Path(member).parts
                            for member in members
                        )
                    )
                    self.assertIsNone(archive.testzip())


if __name__ == "__main__":
    unittest.main()
