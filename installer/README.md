# PhotoGIMP installer

Interactive, filesystem-level PhotoGIMP setup for Python 3.9+ using only the
standard library. Current installer version: **1.2.0**.

## Verification boundary

The installer proves that an explicitly selected GIMP 3.0.x executable reports
the expected version, that the selected profile is initialized, and that files
written to that profile match the checked-in `payload-manifest.json`.

It does **not** launch GIMP or claim that GIMP accepted the configuration. After
installation, launch the same selected GIMP and confirm the layout. Repository
CI uses isolated filesystem profiles; it does not currently certify live GIMP
runtime behavior on every platform/package combination.

## Implemented routing matrix

| OS | Package model | Filesystem routing | Runtime-certified by CI? |
| -- | ------------- | ------------------ | ------------------------ |
| Linux | Native package | `${XDG_CONFIG_HOME:-~/.config}/GIMP/3.0/` | No |
| Linux | Flatpak `org.gimp.GIMP` | `~/.var/app/org.gimp.GIMP/config/GIMP/3.0/` | No |
| Linux | Snap | Refused | No |
| macOS | Runnable `/Applications/GIMP*.app` | `~/Library/Application Support/GIMP/3.0/` | No |
| Windows | Installed GIMP executable | `%APPDATA%\GIMP\3.0\` | No |
| Windows | Portable/USB | Refused | No |

Only config folder **`3.0`** is accepted. GIMP 2.x, 3.2+, unknown versions,
relative environment roots, elevated execution, symlinked paths, uninitialized
profiles, and unknown process state are rejected before mutation.

## Prerequisites

1. Install GIMP yourself from an official source.
2. Open that exact GIMP once, then fully quit it.
3. Run the installer as the desktop user, not with `sudo` or Administrator.
4. Use a local profile without symlinks or unsupported special files.

The installer does not execute package managers or launch a browser.

## Run

```bash
# macOS / Linux
python3 installer/photogimp_install.py

# Windows
py -3 installer\photogimp_install.py
```

Subcommands:

```bash
python3 installer/photogimp_install.py status
python3 installer/photogimp_install.py backup
python3 installer/photogimp_install.py install
python3 installer/photogimp_install.py restore
python3 installer/photogimp_install.py restore BACKUP_ID
python3 installer/photogimp_install.py uninstall
```

All mutating commands require a real TTY. `status` does not execute discovered
GIMP candidates or probe their versions.

## Safety model

- Candidate execution occurs only after explicit selection.
- GIMP version probing must establish a `3.0.x` executable/profile binding.
- Per-profile locks serialize backup, install, restore, and uninstall.
- A sealed backup completes before installation mutates the profile.
- Backup format 3 separates `control/` from the exact copied `profile/` tree.
- Files, directories, modes, timestamps, ownership, and available extended
  attributes are inventoried; links and special files are rejected.
- Source, staged, and final trees are verified against explicit manifests.
- Full-profile activation uses a durable parent-level replacement journal.
- A committed replacement atomically retires, rather than recursively deletes,
  the displaced live tree as a sibling named `.photogimp-retired-<id>`. This
  preserves writes through already-open file handles and avoids destructive
  cleanup recovery. These trees are not sealed backups; inspect them before
  manually removing them after a successful verified operation.
- Interrupted or aborted replacements may similarly retain a verified staged
  tree as `.photogimp-new-<id>` rather than risk deleting concurrent writes.
- Install journals live outside the profile and remain until registry state is
  durable.
- Interrupted committed installs finalize the original uninstall baseline.
- Failed rollback retains its journal and backup reference.
- Uninstall restores/removes only files still owned by the recorded install;
  unrelated files added later are preserved.
- Automatic Linux desktop branding is disabled in the transactional installer.
- Runtime activation remains an explicit user verification step.

Legacy version-2 sealed backups are validated strictly and may be restored.
Unsealed backups are listed as invalid and cannot be restored by this tool.

## Backup layout

| Platform | Data directory |
| -------- | -------------- |
| macOS/Linux | `${XDG_DATA_HOME:-~/.local/share}/photogimp/` |
| Windows | `%LOCALAPPDATA%\PhotoGIMP\` |

Each version-3 backup contains:

```text
BACKUP_ID/
  control/
    manifest.json
    metadata.json
  profile/
    ...exact GIMP profile tree...
```

Restore always displays the backup reason, source path, package kind, and exact
target. It creates another sealed safety backup before replacing a nonempty
current profile.

## Exit codes

| Code | Meaning |
| ---- | ------- |
| `0` | Requested operation and required structural verification completed |
| `1` | Operation, verification, recovery, state persistence, or status failed |
| `2` | Preconditions were not proven; no requested mutation was attempted |
| `3` | User cancelled or input ended before completion |

## Tests and release package

```bash
python3 -m unittest discover -s installer/tests -p "test_*.py" -v
python3 installer/package_release.py --check
python3 installer/package_release.py --output PhotoGIMP-installer.zip
```

`payload-manifest.json` is the independent runtime payload contract.
`release-manifest.json` is the exact release inventory. The package builder
checks every source hash, writes a deterministic archive, then reopens and
verifies every archived entry.

## License

Same as PhotoGIMP: [GNU GPL v3](../LICENSE).
