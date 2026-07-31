#!/usr/bin/env python3
"""Release inventory and deterministic archive tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from installer import package_release


class PackageReleaseTests(unittest.TestCase):
    def test_manifest_is_complete_and_sources_match(self) -> None:
        files = package_release.load_manifest()
        package_release.validate_sources(files)
        self.assertEqual(set(files), package_release.required_release_files())

    def test_archives_are_byte_for_byte_deterministic(self) -> None:
        files = package_release.load_manifest()
        with tempfile.TemporaryDirectory(prefix="pgrelease-") as directory:
            first = Path(directory) / "first.zip"
            second = Path(directory) / "second.zip"
            package_release.build_archive(first, files)
            package_release.build_archive(second, files)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_output_cannot_overwrite_a_release_source(self) -> None:
        files = package_release.load_manifest()
        with self.assertRaisesRegex(ValueError, "overwrite a source file"):
            package_release.validate_output_path(package_release.ROOT / "README.md", files)


if __name__ == "__main__":
    unittest.main()
