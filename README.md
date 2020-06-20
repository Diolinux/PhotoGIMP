![](https://github.com/Diolinux/PhotoGIMP/blob/master/.var/app/org.gimp.GIMP/config/GIMP/2.10/splashes/photogimp-diolinux-splash.png)

# PhotoGIMP
A simple Patch for GIMP 2.10+ to help all Photoshop Users.

* Tool organization to mimic the position of Adobe's Photoshop;
* Hundreds of new fonts by default;
* New Python filters installed by default, such as "heal selection";
* New Splash Screen
* New default settings to maximize space on the canvas;
* Shortcuts setted for the similars on Photoshop, following Adobe's Documentation;
* New icon and Name from custom .desktop file.
* The new default language is English (you can still change in the Settings if you want)


<img src="https://github.com/Diolinux/PhotoGIMP/blob/master/.icons/photogimp.png" data-canonical-src="https://github.com/Diolinux/PhotoGIMP/blob/master/.icons/photogimp.png" width="200" height="200" />

## Included Fonts

https://github.com/Diolinux/PhotoGIMP/blob/master/fonts.txt

# How to Install

This build is all about flatpak, but also "just files" that you can use on any version of GIMP (.deb,.rpm, Snap, AppImage, Windows, macOS), just check the localization of the GIMP files on every system/package.

## Preparing the Flatpak enviroment

* First of all, you need to have the latest GIMP installed on your system [using Flatpak](https://flatpak.org/setup/)
* Install GIMP Flatpak through your AppCenter/Package Manager or terminal:
```flatpak install flathub org.gimp.GIMP```

## Installing this Patch (PhotoGIMP)

Inside of the .zip file from the [releases page](https://github.com/Diolinux/PhotoGIMP/releases) you'll find three hidden folders (on Linux, using the dot before its name). All of this folders has to be extracted on your ```/home/$USER``` folder, overriting everything if you already has the same files from an older installation.

The file has this directories:

* .icons (wich have a new PhotoGIMP icon)
* .local (wich contain the personalized .desktop file)
* .var (wich contain the flatpak patch customization for GIMP 2.10+)

If you just want the PhotoGIMP custom without change the original GIMP icon and its name, just extract only the .var folder to your home directory.

## Credits

* This project would't be possible without the amazing GIMP Team.
* The Photo from the new Splash is from [Isabella Mariana](https://www.pexels.com/pt-br/@isabella-mariana-1022505)
* A BIG thanks to all Diolinux's supporters on Twitch and YouTube.
