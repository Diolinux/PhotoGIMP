# 🎨 PhotoGIMP

<img src="./.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="PhotoGimp application icon" title="PhotoGimp application icon">

A patch for optimizing GIMP 3.0+ for Adobe Photoshop users, including features like:

* Tool organization to mimic the position of Adobe Photoshop;
* New Splash Screen;
* New default settings to maximize space on the canvas;
* Shortcuts similar to the ones in Photoshop for Windows, following Adobe's Documentation;
* New icon and Name from custom .desktop file.

## 📷 Screenshots

<p>
  <img src="./.config/GIMP/3.0/splashes/splash-screen-2025-v2.png" alt="PhotoGIMP Diolinux Splash Art">
  <em>PhotoGIMP Diolinux Splash Art</em>
</p>

<p>
  <img src="./screenshots/photogimp_3_-_diolinux.png" alt="PhotoGIMP 3">
  <em>GIMP 3.0 with the PhotoGIMP patch applied</em>
</p>

## ⚙ How to Install

This patch is originally intended to work with the Flatpak version of GIMP for Linux, but it can be used in almost any package format with no restriction by extracting the files on the correct folders.


### Flatpak (Linux)

In order to install the newest version of PhotoGIMP on your Linux operating system using Flatpak, just follow this simple steps:

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />

1. Make sure you already have GIMP installed [from Flathub](https://flathub.org/apps/org.gimp.GIMP);
2. **Start and quit GIMP after you installed before you continue!**
3. Download the files from this repository [or just click here](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip);
4. Extract the content of the zip file on your home folder (`.config` and `.local` - they are the important ones) and overwrite the files if needed;
5. You're done, enjoy it! :smile:

<hr>

### Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />

In order to install the newest version of PhotoGIMP on your Windows:

1. Make sure you already have [GIMP installed from official website](https://www.gimp.org/downloads/);
2. **Start and quit GIMP after you installed before you continue!**
3. Download thes files from this repository or [just click here](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip);
4. Extract the content from `PhotoGIMP.zip` to a folder of your preference;
5. Copy the `3.0` folder;
6. Hold <kbd>Windows</kbd> key and press <kbd>R</kbd> to open the *Execute* dialog;
7. Type `%APPDATA%\GIMP` into the dialog and press <kbd>Enter</kbd>;
8. Paste the `3.0` folder inside the GIMP's folder that you just opened;
9. When prompted about existing files, select "Replace the files in the destination";
10. You're done, enjoy it! :smile:

Or install via [Chocolatey](https://chocolatey.org/):
```powershell
choco install photogimp
```
Maintained by: [André Augusto](https://github.com/AndreAugustoDev)


:bulb: Tips:
- Optionally, you can also download the [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) and update the icon from the shortcut in `%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0`;
- If you want to backup your current GIMP settings before installing PhotoGIMP, copy the entire `3.0` folder from `%APPDATA%\GIMP` to a safe location before proceeding with the installation.

### macOS

<img src="https://skillicons.dev/icons?i=macos" align="right" />

In order to install the newest version of PhotoGIMP on your macOS:

1. Make sure you already have [GIMP installed from official website](https://www.gimp.org/downloads/);
2. **Start and quit GIMP after you installed before you continue!**
3. Download the files from this repository or [just click here](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip);
4. Extract the content from `PhotoGIMP.zip` to a folder of your preference;
5. Copy the `3.0` folder;
6. Open Finder, press <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> to open "Go to Folder";
7. Type `~/Library/Application Support/GIMP` and press <kbd>Enter</kbd>;
8. If you have a `2.10` folder from a previous installation, delete it to avoid conflicts;
9. Paste the `3.0` folder inside the GIMP folder;
10. When prompted about existing files, select "Replace" or "Merge";
11. You're done, enjoy it! :smile:

:bulb: Tips:
- If you want to backup your current GIMP settings before installing PhotoGIMP, copy the entire GIMP folder from `~/Library/Application Support/GIMP` to a safe location before proceeding with the installation.

## Credits

* This project would not be possible without the amazing GIMP team.
* A BIG thanks to all Diolinux's supporters on [YouTube](https://youtube.com/Diolinux).
* Splash screen & icons from [Adriel Filipe Design](https://bento.me/adrielfilipedesign)

## Contributors
<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>
