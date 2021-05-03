![PhotoGimp Diolinux Splash Art](./.var/app/org.gimp.GIMP/config/GIMP/2.10/splashes/photogimp-diolinux-splash.png)

# 🎨 PhotoGIMP

<img
  src="https://raw.githubusercontent.com/Diolinux/PhotoGIMP/master/.icons/photogimp.png"
  alt="PhotoGimp Icon"
  title="PhotoGimp"
  width="200px">

A patch for optimizing GIMP 2.10+ for Adobe Photoshop users, including features like:

* Tool organization to mimic the position of Adobe's Photoshop;
* Hundreds of new fonts by default;
* New Python filters installed by default, such as "heal selection";
* New Splash Screen
* New default settings to maximize space on the canvas;
* Shortcuts similar to the ones on Photoshop, following Adobe's Documentation;
* New icon and Name from custom .desktop file.
* System Language is now used by default, you can still change in settings if you want.

## 📷 Screenshots

![PhotoGimp Screenshot - Editing Google Takeout](./screenshots/2020-06-22_12-06.png)

## ✍️ Have a large set of fonts available anytime

More than 1800 fonts are included by default in PhotoGimp so you can speed up your creative workflow.

<!-- TODO: Add Screenshot utilizing one of included fonts. -->

[Check out all included fonts](https://github.com/Diolinux/PhotoGIMP/blob/master/fonts.txt)

# 🖥️ How to Install

This build is all about flatpak, but it also contains "just files" that you can use on any version of GIMP (.deb,.rpm, Snap, AppImage, Windows, macOS). Just check the localization of the GIMP files on every system/package.

## Preparing the Flatpak enviroment

* First of all, you need to have the latest GIMP installed on your system [using Flatpak](https://flatpak.org/setup/)
* Install GIMP Flatpak through your AppCenter/Package Manager or terminal:
```flatpak install flathub org.gimp.GIMP```

## Installing PhotoGIMP

Inside the .zip file from the [releases page](https://github.com/Diolinux/PhotoGIMP/releases) you'll find three hidden folders (on Linux, using the dot before it's name). All of these folders have to be extracted on your ```/home/$USER``` folder, overwriting everything if you already have the same files from an older installation.

The file contains these directories:

* .icons (which has a new PhotoGIMP icon)
* .local (which contains the personalized .desktop file)
* .var (which contains the flatpak patch customization for GIMP 2.10+)

If you just want the PhotoGIMP customization without changing the original GIMP icon and it's name, just extract only the .var folder to your home directory.

## Want to use on Windows, macOS or Ubuntu(Snap)?

* [Vídeo Tutorial by Davies Media Design on macOS](https://youtu.be/5nXhtaGQs9U)
* [Vídeo Tutorial by Davies Media Design on Windows](https://youtu.be/57DNUsf4A-0)

Since it's just files, the only thing you need to do is to copy all the files that reside on a particular folder from this patch ```/.var/app/org.gimp.GIMP/config/GIMP/2.10``` to the the GIMP's folder on each particular system, overriding the existent ones:

* Windows: `%APPDATA%\GIMP\2.10`

* macOS: `~/Library/Application Support/GIMP/2.10/`

  This one-liner will do the job: download release 1.0 into `Downloads` folder, unzip and copy patch files, then remove previously downloaded zip:
  ```bash
  curl -L "https://github.com/Diolinux/PhotoGIMP/releases/download/1.0/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip" -o ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip && unzip ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip -d ~/Downloads && cp -R ~/Downloads/PhotoGIMP\ by\ Diolinux\ v2020\ for\ Flatpak/.var/app/org.gimp.GIMP/config/GIMP/2.10/ ~/Library/Application\ Support/GIMP/2.10 && rm ~/Downloads/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip
  ```
  **Notice:** GIMP on macOS are a bit late on it's release. This way, this patch still works, specially on the shorcuts matter, but somethings, such the toolbox organization, will not work properly. Until macOS's version reaches the version 2.10.20, expect this behavior.

* Ubuntu (Snap): `/home/$USER/snap/gimp/47/.config/GIMP/2.10/`

* Regular Linux Installation (.deb, .rpm): `/home/$USER/.config/GIMP/2.10/`

The new icon will only work through the patch extration process on Linux enviroments, but you can set it manually on your system.

## Credits

* This project would't be possible without the amazing GIMP Team.
* The Photo in the new Splash is from [Isabella Mariana](https://www.pexels.com/pt-br/@isabella-mariana-1022505)
* A BIG thanks to all Diolinux's supporters on [Twitch](https://twitch.tv/Diolinux) and [YouTube](https://youtube.com/Diolinux).

## Patch Notes
-  [Veja as Notas de Lançamento em Português](https://diolinux.com.br/2020/06/photogimp-2020.html)
