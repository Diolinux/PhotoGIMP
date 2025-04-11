# 🎨 PhotoGIMP

<img src="./.local/share/icons/hicolor/256x256/256x256.png" align="right" alt="PhotoGimp application icon">
PhotoGIMP improves GIMP 3.0+ to make it behave, look and feel more like Adobe Photoshop by patching [GIMP's configuration and supporting data](https://www.gimp.org/tutorials/GIMPProfile/).

## 🎁 Features

* Tool organization to mimic the layout of Adobe Photoshop.
* Keyboard shortcuts similar to the ones in Photoshop for Windows, following Adobe's documentation.
* New default settings to maximize space on the canvas.
* New splash screen.
* New app icon and name from custom `.desktop` file.

## 📷 Screenshots

![PhotoGIMP Diolinux splash screen artwork](./.config/GIMP/3.0/splashes/splash-screen-2025-v2.png)  
 *PhotoGIMP Diolinux splash screen artwork*

![GIMP 3.0 with the PhotoGIMP patch applied](./screenshots/photogimp_3_-_diolinux.png)  
 *GIMP 3.0 with the PhotoGIMP patch applied*

## 🗳 How to Install

This patch is originally intended to work with the Flatpak version of GIMP for Linux, but it can be used in almost any package format with no restriction by extracting the files on the correct folders.

### Flatpak (Linux)

<img src="https://skillicons.dev/icons?i=linux" align="right" width="40" />
In order to install the newest version of PhotoGIMP on your Linux operating system using Flatpak, just follow this simple steps:

1. Make sure you already have GIMP installed [from Flathub](https://flathub.org/apps/org.gimp.GIMP);
2. **Start and quit GIMP after you installed before you continue!**
3. Download the files from this repository [or just click here](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP-linux.zip);
4. Extract the content of the zip file on your home folder (`.config` and `.local` - they are the important ones) and overwrite the files if needed;
5. You're done, enjoy it! :smile:

### Windows

<img src="https://skillicons.dev/icons?i=windows" align="right" />
In order to install the newest version of PhotoGIMP on your Windows:

1. Make sure you already have [GIMP installed from official website](https://www.gimp.org/downloads/);
2. **Start and quit GIMP after you installed before you continue!**
3. Download thes files from this repository or [just click here](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip);
4. Extract the content from `PhotoGIMP.zip` to a folder of your preference;
5. Copy the `3.0` folder;
6. Hold <kbd>Windows</kbd> key and press <kbd>R</kbd> to open the *Execute* dialog;
7. Type `%APPDATA%\GIMP` into the dialog and press <kbd>Return</kbd>;
8. Paste the `3.0` folder inside the GIMP's folder that you just opened;
9. When prompted about existing files, select "Replace the files in the destination";
10. You're done, enjoy it! :smile:

Or install via [Chocolatey](https://chocolatey.org/):

```powershell
choco install photogimp
```

Maintained by: [André Augusto](https://github.com/AndreAugustoDev)

:bulb: Tips:

* Optionally, you can also download the [photogimp.ico](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/photogimp.ico) and update the icon from the shortcut in `%appdata%\Microsoft\Windows\Start Menu\Programs\GIMP 3.0.0`;
* If you want to backup your current GIMP settings before installing PhotoGIMP, copy the entire `3.0` folder from `%APPDATA%\GIMP` to a safe location before proceeding with the installation.

### macOS

<img src="https://skillicons.dev/icons?i=apple" align="right" />
In order to install the newest version of PhotoGIMP on your macOS:

1. Make sure you already have [GIMP installed from official website](https://www.gimp.org/downloads/);
2. **Start and quit GIMP after you installed before you continue!**
3. Download the files from this repository or [just click here](https://github.com/Diolinux/PhotoGIMP/releases/download/3.0/PhotoGIMP.zip).
4. Extract the contents from `PhotoGIMP.zip` per doubleclick, it should extract a `3.0` folder.
5. Select and copy the extracted `3.0` folder by pressing <kbd>Cmd</kbd> + <kbd>C</kbd>.
6. Press <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> to open the *Go to Folder…* dialog.<br>Type and/or select `~/Library/Application Support/GIMP` and press <kbd>Return</kbd>.
7. If you already have a `2.10` or `3.0` folder (or alike), rename or delete it to avoid conflicts;
8. Paste the `3.0` folder inside the GIMP folder by pressing <kbd>Cmd</kbd> + <kbd>V</kbd>.
9. You're done, enjoy it! :smile:

:bulb: Tips:

* If you want to backup your current GIMP settings before installing PhotoGIMP, copy the entire GIMP folder from `~/Library/Application Support/GIMP` to a safe location before proceeding with the installation.

## Credits

* This project would not be possible without the amazing GIMP team.
* A BIG thanks to all Diolinux's supporters on [YouTube](https://youtube.com/Diolinux).
* Splash screen & icons from [Adriel Filipe Design](https://bento.me/adrielfilipedesign)

## Contributors

<a align="center" href="https://github.com/Diolinux/PhotoGIMP/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Diolinux/PhotoGIMP" />
</a>
