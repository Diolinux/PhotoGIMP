#!/usr/bin/env python3
"""Validate and optionally build the exact PhotoGIMP installer release archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "installer" / "release-manifest.json"
PAYLOAD_MANIFEST = ROOT / "installer" / "payload-manifest.json"
STATIC_RELEASE_FILES = {
    "LICENSE",
    "README.md",
    "installer/README.md",
    "installer/__init__.py",
    "installer/package_release.py",
    "installer/payload-manifest.json",
    "installer/photogimp_install.py",
}
EXECUTABLE_RELEASE_FILES = {
    "installer/package_release.py",
    "installer/photogimp_install.py",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_link_or_reparse(path: Path) -> bool:
    try:
        item_stat = path.lstat()
    except FileNotFoundError:
        return False
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(item_stat.st_mode) or bool(
        getattr(item_stat, "st_file_attributes", 0) & reparse_flag
    )


def _valid_relpath(rel: object) -> bool:
    if not isinstance(rel, str) or not rel or "\\" in rel or ":" in rel:
        return False
    path = PurePosixPath(rel)
    return not path.is_absolute() and all(part not in ("", ".", "..") for part in path.parts)


def _source_path(rel: str) -> Path:
    return ROOT.joinpath(*PurePosixPath(rel).parts)


def required_release_files() -> set[str]:
    contract = json.loads(PAYLOAD_MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(contract, dict) or contract.get("version") != 1:
        raise ValueError("payload manifest has an unsupported schema")
    payload = contract.get("payload")
    branding = contract.get("branding")
    if not isinstance(payload, dict) or not isinstance(branding, dict):
        raise ValueError("payload manifest inventory is invalid")

    required = set(STATIC_RELEASE_FILES)
    for rel in payload:
        if not _valid_relpath(rel):
            raise ValueError(f"invalid payload manifest path: {rel!r}")
        required.add(f".config/GIMP/3.0/{rel}")
    for rel in branding:
        if not _valid_relpath(rel):
            raise ValueError(f"invalid branding manifest path: {rel!r}")
        required.add(f".local/{rel}")
    return required


def load_manifest() -> dict[str, str]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("release manifest has an unsupported schema")
    files = data.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("release manifest has no files map")
    result: dict[str, str] = {}
    for rel, digest in files.items():
        if (
            not _valid_relpath(rel)
            or not isinstance(digest, str)
            or len(digest) != 64
            or any(char not in "0123456789abcdef" for char in digest)
        ):
            raise ValueError(f"invalid release manifest entry: {rel!r}")
        result[rel] = digest
    required = required_release_files()
    if set(result) != required:
        missing = sorted(required - set(result))
        extra = sorted(set(result) - required)
        raise ValueError(f"release manifest inventory mismatch; missing={missing}; extra={extra}")
    return result


def validate_sources(files: dict[str, str]) -> None:
    problems: list[str] = []
    for rel, expected in files.items():
        path = _source_path(rel)
        if _is_link_or_reparse(path) or not path.is_file():
            problems.append(f"missing or unsafe release file: {rel}")
        elif sha256(path) != expected:
            problems.append(f"release file hash mismatch: {rel}")
    if problems:
        raise ValueError("; ".join(problems))


def validate_output_path(output: Path, files: dict[str, str]) -> Path:
    resolved = output.expanduser().resolve()
    protected = {MANIFEST.resolve()}
    protected.update(_source_path(rel).resolve() for rel in files)
    if resolved in protected:
        raise ValueError(f"release output would overwrite a source file: {resolved}")
    return resolved


def build_archive(output: Path, files: dict[str, str]) -> None:
    output = validate_output_path(output, files)
    output.parent.mkdir(parents=True, exist_ok=True)
    archive_files = dict(files)
    archive_files["installer/release-manifest.json"] = sha256(MANIFEST)
    fd, temp_name = tempfile.mkstemp(prefix=f".{output.name}.", suffix=".tmp", dir=output.parent)
    os.close(fd)
    temp_output = Path(temp_name)
    try:
        with zipfile.ZipFile(
            temp_output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for rel in sorted(archive_files):
                source = MANIFEST if rel == "installer/release-manifest.json" else _source_path(rel)
                data = source.read_bytes()
                entry = zipfile.ZipInfo(
                    f"PhotoGIMP/{rel}", date_time=(1980, 1, 1, 0, 0, 0)
                )
                mode = 0o755 if rel in EXECUTABLE_RELEASE_FILES else 0o644
                entry.create_system = 3
                entry.external_attr = (stat.S_IFREG | mode) << 16
                entry.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(entry, data, compresslevel=9)
        with zipfile.ZipFile(temp_output) as archive:
            names = set(archive.namelist())
            expected_names = {f"PhotoGIMP/{rel}" for rel in archive_files}
            if names != expected_names:
                raise ValueError("release archive inventory mismatch")
            for rel, expected in archive_files.items():
                actual = hashlib.sha256(archive.read(f"PhotoGIMP/{rel}")).hexdigest()
                if actual != expected:
                    raise ValueError(f"release archive hash mismatch: {rel}")
        os.replace(temp_output, output)
    finally:
        temp_output.unlink(missing_ok=True)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate source inventory")
    parser.add_argument("--output", type=Path, help="write a deterministic release zip")
    args = parser.parse_args(argv)
    files = load_manifest()
    validate_sources(files)
    if args.output:
        build_archive(args.output.resolve(), files)
        print(f"Built and verified {args.output.resolve()}")
    else:
        print(f"Verified {len(files)} release files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
