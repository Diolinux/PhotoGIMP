# 🎨 PhotoGIMP

<img src="./.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="PhotoGIMP application icon" title="PhotoGIMP application icon">

[![GitHub stars](https://img.shields.io/github/stars/Diolinux/PhotoGIMP?style=social)](https://github.com/Diolinux/PhotoGIMP)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Latest Release](https://img.shields.io/github/v/release/Diolinux/PhotoGIMP)](https://github.com/Diolinux/PhotoGIMP/releases/latest)

**PhotoGIMP** is a free, community-driven patch that transforms [GIMP](https://www.gimp.org/) (GNU Image Manipulation Program) into a layout that feels familiar to **Adobe Photoshop** users. If you're switching from Photoshop to GIMP and want to feel at home right away, PhotoGIMP is for you.

> **New to GIMP?** GIMP is a free and open-source image editor available for Linux, macOS, and Windows. It can do most things Photoshop can — photo retouching, image composition, graphic design, and more — all for free. PhotoGIMP just makes it _look and feel_ more like Photoshop.

---

## ✨ Features

- **Photoshop-like tool layout** — Tools are reorganized to mimic the positions you're used to in Adobe Photoshop.
- **Custom Splash Screen** — A unique PhotoGIMP splash screen greets you on startup.
- **Maximized canvas space** — Default settings are optimized to give you the largest possible working area.
- **Photoshop keyboard shortcuts** — Keyboard shortcuts follow [Adobe's official documentation](https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html) for the Windows version.
- **Custom icon & name** — On Linux, a dedicated `.desktop` file can give PhotoGIMP its own icon and app name in your system menu.
- **Guided installer** — Optional Python installer detects GIMP, backs up your settings, and applies PhotoGIMP automatically.

---

## 📷 Screenshots

| Splash Screen | Application Window |
|-|-|
| ![[PhotoGIMP Diolinux splash screen]](./.config/GIMP/3.0/splashes/splash-screen-2025-v2.png)<br>PhotoGIMP Diolinux splash screen | ![[PhotoGIMP 3]](./screenshots/photogimp_3_-_diolinux.png)<br>PhotoGIMP 3

---

## 📋 Requirements

| Requirement | Details |
| ----------- | ------- |
| **GIMP 3.0.x** | Required by the guided installer and current payload. [gimp.org/downloads](https://www.gimp.org/downloads/) or [Flathub](https://flathub.org/apps/org.gimp.GIMP) (Linux). GIMP 3.2+ is refused until a matching payload is available. |
| **Python 3.9+** | Only required for the guided installer (`python3` / Windows `py -3`). Not needed for manual zip install. |
| **Run GIMP at least once** | GIMP creates its config folders on first launch. The installer will prompt you if they are missing. |

---

## 🚀 Quick install (recommended)

The installer is an interactive wizard that:

1. Detects an existing GIMP installation without executing candidates during `status`
2. Creates a sealed, timestamped backup of the selected profile
3. Installs the exact files listed in `installer/payload-manifest.json`
4. Supports verified **restore a backup** and managed-path **uninstall**

### Get the files

Clone this repository. Existing release archives may predate the guided installer;
future installer releases must bundle `installer/`, `.config/GIMP/3.0/`, and
`.local/` together.

```bash
git clone https://github.com/Diolinux/PhotoGIMP.git
cd PhotoGIMP
```

### Run the wizard

```bash
# macOS / Linux
python3 installer/photogimp_install.py

# Windows
py -3 installer\photogimp_install.py
```

Menu options:

1. **Install PhotoGIMP**
2. **Restore a GIMP profile backup**
3. **Uninstall PhotoGIMP**
4. **Status**
5. **Exit**

You can also run subcommands directly:

```bash
python3 installer/photogimp_install.py status
python3 installer/photogimp_install.py install
python3 installer/photogimp_install.py restore
python3 installer/photogimp_install.py uninstall
```

More detail and the **support matrix**: [installer/README.md](./installer/README.md).

> [!IMPORTANT]
> Quit GIMP completely before install, restore, or uninstall. GIMP may overwrite settings on exit if it is still running.
>
> The installer targets **GIMP 3.0.x** config folders only, verifies files with **SHA-256** (not a live GIMP session), and refuses Snap and Windows Portable installs. Mutating commands require a real terminal, absolute profile roots, a non-elevated desktop user, a proven closed-GIMP state, and symlink-free user data. Durable journals recover interrupted profile replacement and install finalization. Replaced live trees are retained beside the profile as `.photogimp-retired-<id>` directories instead of being automatically deleted; inspect them before manual cleanup.
>
> Cross-platform routing is implemented and tested with isolated profiles, but repository CI does not currently certify live GIMP runtime activation for every OS/package combination. Launch the same selected GIMP and confirm the layout after installation.

---

## 💾 Backups, restore & uninstall

The installer completes and verifies a sealed backup before applying PhotoGIMP. If it cannot prove an equivalent backup, it does not mutate the profile.

| Platform | Backup location |
| -------- | --------------- |
| **macOS / Linux** | `${XDG_DATA_HOME:-~/.local/share}/photogimp/backups/` |
| **Windows** | `%LOCALAPPDATA%\PhotoGIMP\backups\` |

Each version-3 backup separates installer controls from profile data: `control/manifest.json`, `control/metadata.json`, and `profile/`. Files, directories, supported metadata, and hashes are verified before restore.

| Action | How |
| ------ | --- |
| **Restore a GIMP profile backup** | Installer menu option 2, or `… restore`; the reason, source, and exact target are displayed first |
| **Uninstall PhotoGIMP** | Menu option 3; restores/removes only files still owned by the recorded install and preserves unrelated current files |
| **See paths & state** | Menu option 4, or `… status` |

---

## 📁 Where GIMP stores settings

| GIMP install type | Config directory |
| ----------------- | ---------------- |
| **Linux (native package)** | `~/.config/GIMP/<version>/` |
| **Linux (Flatpak)** | `~/.var/app/org.gimp.GIMP/config/GIMP/<version>/` |
| **Windows** | `%APPDATA%\GIMP\<version>\` (usually `C:\Users\<you>\AppData\Roaming\GIMP\3.0`) |
| **macOS** | `~/Library/Application Support/GIMP/<version>/` |

The guided installer probes the selected GIMP executable, requires version **3.0.x**, and binds it to the matching `3.0` profile. It never guesses the newest folder.

---

## ⚙ Manual install (advanced)

Manual installation is not equivalent to the transactional installer. Copying
the whole repository or legacy release archive also copies author-generated
`filters/`, `plug-in-settings/`, and Flatpak-specific `theme.css`; that can
overwrite filter history, export metadata defaults, and native-package theme
state. Use it only after making and independently verifying your own backup.

### 🐧 Linux

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

#### Backup (manual)

**Native package:**

```bash
cp -r ~/.config/GIMP/3.0 ~/GIMP-3.0-backup
```

**Flatpak:**

```bash
cp -r ~/.var/app/org.gimp.GIMP/config/GIMP/3.0 ~/GIMP-3.0-backup
```

#### Install from zip

1. Install GIMP ([Flathub](https://flathub.org/apps/org.gimp.GIMP) recommended, or your distro packages).
2. **Open GIMP once, then close it.**
3. Legacy external asset, not generated by the current manifest pipeline: **[PhotoGIMP for Linux (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip)**
4. Extract the `.zip` **into your home folder** (`~`) so files land under `~/.config` and `~/.local`.
   - Hidden folders: press <kbd>Ctrl</kbd> + <kbd>H</kbd> in your file manager.
   - On conflicts, choose **Replace** / **Overwrite**.
5. **Flatpak note:** the release zip targets `~/.config/GIMP/3.0`. Flatpak GIMP normally uses `~/.var/app/org.gimp.GIMP/config/GIMP/3.0`. Prefer the [guided installer](#-quick-install-recommended), which uses the correct Flatpak path, or copy the `3.0` payload into that Flatpak config directory yourself.
6. Open GIMP — you should see the PhotoGIMP layout.

<details>
<summary><strong>💡 Using a non-Flatpak GIMP?</strong></summary>

Config lives at `${XDG_CONFIG_HOME:-~/.config}/GIMP/3.0` for most distro packages. The current guided installer requires GIMP 3.0.x.

</details>

---

### 🪟 Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

#### Backup (manual)

1. Press <kbd>Windows</kbd> + <kbd>R</kbd>.
2. Type `%APPDATA%\GIMP` and press <kbd>Enter</kbd>.
3. Copy the entire `3.0` folder somewhere safe (e.g. Desktop).

#### Install from zip

1. Install [GIMP from the official website](https://www.gimp.org/downloads/).
2. **Open GIMP once, then close it.**
3. Legacy external asset, not generated by the current manifest pipeline: **[PhotoGIMP for Windows (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Extract the zip, copy the `3.0` folder.
5. Open `%APPDATA%\GIMP` and paste `3.0` there.
6. Choose **Replace the files in the destination** when prompted.
7. Open GIMP — you should see the PhotoGIMP layout.

<details>
<summary><strong>💡 Optional: Change the GIMP shortcut icon</strong></summary>

The linked [legacy external `photogimp.ico`](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) is not present in or verified by this repository's release manifest. If you still use it, set it on the Start Menu shortcut under:

```
%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0
```

Right-click → **Properties** → **Change Icon**.

</details>

<details>
<summary><strong>🍫 Install via Chocolatey (alternative)</strong></summary>

The following Chocolatey package is third-party maintained and is not built or
verified by this repository's release manifest:

```powershell
choco install photogimp
```

Maintained by: [André Augusto](https://github.com/AndreAugustoDev)

</details>

---

### 🍎 macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

#### Backup (manual)

1. Open Finder.
2. <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> → `~/Library/Application Support/GIMP`
3. Copy the `GIMP` folder (or the `3.0` folder) somewhere safe.

#### Install from zip

1. Install [GIMP from the official website](https://www.gimp.org/downloads/).
2. **Open GIMP once, then close it.**
3. Legacy external asset, not generated by the current manifest pipeline: **[PhotoGIMP for macOS (.zip)](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip)**
4. Extract the zip and copy the `3.0` folder.
5. Go to `~/Library/Application Support/GIMP`.
6. Keep any existing `2.10` folder; it belongs to the older GIMP version and may contain settings you still need.
7. Paste `3.0` into the GIMP folder; choose **Replace** / **Merge** on conflicts.
8. Open GIMP — you should see the PhotoGIMP layout.

<details>
<summary><strong>Alternative: install with Terminal</strong></summary>

If Finder **Merge** skips files, use `rsync` (both paths should end with `/`):

```bash
rsync -av --ignore-times /path/to/extracted/3.0/ ~/Library/Application\ Support/GIMP/3.0/
```

The current payload is authored for GIMP 3.0. Copying it into another version folder (for example `3.2`) is unsupported and unverified.

</details>

---

## 📦 What's inside the patch

The guided installer replaces or adds these manifest-controlled files in the selected GIMP configuration directory:

| File / folder | What it does |
| ------------- | ------------ |
| `shortcutsrc` | Keyboard shortcuts mapped closer to Photoshop |
| `toolrc` | Tool configuration and ordering |
| `sessionrc` | Window layout and panel positions |
| `gimprc` | General preferences (canvas, UI options, etc.) |
| `contextrc` | Active tool/color context defaults |
| `splashes/` | Custom PhotoGIMP splash screen |
| `tool-options/` | Default options for individual tools |
| `theme.css` | Minor theme tweaks (Flatpak-oriented; installer applies it on Flatpak only) |

On Linux, the patch can also install:

- A custom `.desktop` launcher (PhotoGIMP name and icon)
- Icons under `~/.local/share/icons/`

The checked-in desktop launcher is Flatpak-specific. Installer 1.2.0 does not
install Linux branding automatically because branding is outside the profile
transaction; apply it manually only if its `Exec=` command matches your setup.

The guided installer intentionally excludes `filters/` and `plug-in-settings/`; these contain author-specific state, including export metadata choices. `theme.css` is Flatpak-only because its `/app` imports do not exist in native packages. The exact paths and SHA-256 values are enforced by `installer/payload-manifest.json`. Whole-folder manual copying does not apply these exclusions.

---

## 🗑 How to uninstall (manual)

Prefer the installer **Uninstall** or **Restore a GIMP profile backup** when possible.

To reset GIMP without the installer, delete the versioned config folder and reopen GIMP (it recreates defaults), or restore your own backup.

### Linux

Native:

```bash
rm -rf ~/.config/GIMP/3.0
```

Flatpak:

```bash
rm -rf ~/.var/app/org.gimp.GIMP/config/GIMP/3.0
```

Restore a manual backup example:

```bash
cp -r ~/GIMP-3.0-backup ~/.config/GIMP/3.0
```

### Windows

1. <kbd>Windows</kbd> + <kbd>R</kbd> → `%APPDATA%\GIMP`
2. Delete the `3.0` folder (or paste your backup back)
3. Open GIMP

### macOS

1. <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> → `~/Library/Application Support/GIMP`
2. Delete the `3.0` folder (or paste your backup back)
3. Open GIMP

---

## ❓ Troubleshooting / FAQ

> [!CAUTION]
> **PhotoGIMP does not have an official website.** The only official source for the project is its GitHub repository: https://github.com/Diolinux/PhotoGIMP/

<details>
<summary><strong>PhotoGIMP didn't change anything — GIMP looks the same</strong></summary>

- Confirm files were written to the **config path for your GIMP install** (see [Where GIMP stores settings](#-where-gimp-stores-settings)). Flatpak is not the same as `~/.config` unless you copied there on purpose.
- Did you **fully quit GIMP** before installing? GIMP can overwrite settings on exit.
- Run `python3 installer/photogimp_install.py status` to see which paths the installer detects.
- **Windows:** the `3.0` folder must be inside `%APPDATA%\GIMP`, not next to it.
- **macOS:** the `3.0` folder must be inside `~/Library/Application Support/GIMP`.

</details>

<details>
<summary><strong>The installer says GIMP is not installed</strong></summary>

- Install GIMP yourself from [gimp.org](https://www.gimp.org/downloads/) or Flathub. The installer does not run package managers or launch a browser.
- After installing, open GIMP once, quit it, and run the installer again (`status` then `install`).

</details>

<details>
<summary><strong>Python is not found</strong></summary>

- **macOS / Linux:** install Python 3.9+ from your package manager or [python.org](https://www.python.org/downloads/), then use `python3`.
- **Windows:** install Python from [python.org](https://www.python.org/downloads/) or the Microsoft Store, then use `py -3`.
- Manual zip install does not require Python.

</details>

<details>
<summary><strong>I get an error when opening GIMP after installing PhotoGIMP</strong></summary>

- The current PhotoGIMP payload and guided installer target **GIMP 3.0.x**. GIMP 2.x and 3.2+ are not supported by this payload.
- Restore a backup via the installer, or delete the versioned config folder and reinstall — see [Uninstall](#-how-to-uninstall-manual).

</details>

<details>
<summary><strong>Can I use PhotoGIMP with GIMP 2.10?</strong></summary>

No. This release is limited to **GIMP 3.0.x**. GIMP 2.x and GIMP 3.2+ are rejected by the guided installer.

</details>

<details>
<summary><strong>Will PhotoGIMP delete my custom brushes, fonts, or plug-ins?</strong></summary>

The guided installer replaces only manifest-controlled configuration paths. Managed-path uninstall preserves unrelated brushes, fonts, gradients, plug-ins, and files added after installation. A full-profile **Restore a backup** intentionally replaces the entire selected profile after first creating another sealed safety backup. Whole-folder manual installation has broader overwrite behavior.

</details>

<details>
<summary><strong>Can I customize the shortcuts after installing PhotoGIMP?</strong></summary>

Yes. PhotoGIMP is a starting point. Change shortcuts in GIMP via **Edit → Keyboard Shortcuts**.

</details>

<details>
<summary><strong>How do I update PhotoGIMP to a new version?</strong></summary>

Re-run the installer (`install`) or repeat the manual zip steps. The installer creates a new backup each time before overwriting.

</details>

<details>
<summary><strong>How do I undo PhotoGIMP?</strong></summary>

Use **Uninstall PhotoGIMP** to restore/remove only installer-owned paths while preserving unrelated current files. Use **Restore a GIMP profile backup** only when you intend to replace the entire selected profile with that exact backup.

</details>

---

## 🤝 Contributing

Found a bug? Have a suggestion? We'd love your help!

- **Report an issue**: [Open an issue](https://github.com/Diolinux/PhotoGIMP/issues)
- **Submit a fix**: [Create a pull request](https://github.com/Diolinux/PhotoGIMP/pulls)
- **Translate**: Help us translate the README into more languages! See the [Translations](#-translations) section.

Installer documentation is English-first for now; translations can follow the same structure when ready.

---

## 🌍 Translations

This README is available in other languages:

- 🇮🇹 [Italiano (Italian)](./docs/README_it.md)
- 🇵🇱 [Polski (Polish)](./docs/README_pl.md)
- 🇺🇦 [Українська (Ukrainian)](./docs/README_ua.md)
- 🇧🇷 [Português (Brazilian Portuguese)](./docs/README_pt.md)
- 🇷🇺 [Русский (Russian)](./docs/README_ru.md)
- 🇪🇸 [Español (Spanish)](./docs/README_es.md)
- 🇮🇱 [עברית (Hebrew)](https://github.com/Diolinux/PhotoGIMP/blob/master/docs/README_he.md)
- 🇰🇷 [Korean (한국어)](./docs/README_ko.md)
- 🇨🇳 [简体中文 (Simplified Chinese)](./docs/README_zh.md)

Want to add your language? Fork the repo, create a `docs/README_xx.md` file, and submit a pull request!

---

## 🏆 Credits

- This project would not be possible without the amazing [GIMP](https://www.gimp.org/) team.
- A BIG thanks to all Diolinux's supporters on [YouTube](https://youtube.com/Diolinux).
- Splash screen & icons from [Adriel Filipe Design](https://bento.me/adrielfilipedesign).

---

## 👥 Contributors

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>

---

## 📄 License

PhotoGIMP is licensed under the [GNU General Public License v3.0](./LICENSE).
