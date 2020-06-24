<h1 align="center">
  <img src="https://github.com/Diolinux/PhotoGIMP/blob/master/.icons/photogimp.png" alt="GIMP" width="256" height="256">
  <br />
  PhotoGIMP <br/>
  <h3 align="center">Download: <a href="https://github.com/Diolinux/PhotoGIMP/releases/download/1.0/PhotoGIMP.by.Diolinux.v2020.for.Flatpak.zip">Patch</a> | <a href="https://github.com/sudo-give-me-coffee/PhotoGIMP/releases/download/continuous/PhotoGIMP-x86_64.AppImage">AppImage</a></h3>
</h1>

<p align="center"><i>"The GIMP for those who come from Adobe Photoshop for Windows"</i>.<br> Original work</p>

<hr>

### What is?

A simple Patch for GIMP 2.10+ to help all Photoshop Users.

* Tool organization to mimic the position of Adobe's Photoshop;
* Hundreds of new fonts by default;
* New Python filters installed by default, such as "heal selection";
* New Splash Screen
* New default settings to maximize space on the canvas;
* Shortcuts setted for the similars on Photoshop, following Adobe's Documentation;
* New icon and Name from custom .desktop file.
* The new default language is English (you can still change in the Settings if you want)

It should looks like this:

![](https://github.com/Diolinux/PhotoGIMP/blob/master/2020-06-22_12-06.png
)

### Included Fonts

https://github.com/Diolinux/PhotoGIMP/blob/master/fonts.txt

### How to Install

Is very easy to do:

##### Linux

Run inside the extracted folder:

```
bash install_linux.sh
```

##### Windows

Double click inside the extracted folder on file:

```
install_windows.bat
```

##### Installing manual

Inside of the .zip file from the [releases page](https://github.com/Diolinux/PhotoGIMP/releases) you'll find three hidden folders (on Linux, using the dot before its name). All of this folders has to be extracted on your ```/home/$USER``` folder, overriting everything if you already has the same files from an older installation.

The file has this directories:

* .icons (wich have a new PhotoGIMP icon)
* .local (wich contain the personalized .desktop file)
* .var (wich contain the flatpak patch customization for GIMP 2.10+ as flatpak)

If you just want the PhotoGIMP custom without change the original GIMP icon and its name, just extract only the `.var` folder to your home directory. For installation with other gimp installations, copy the contents of `.var/app/org.gimp.GIMP/config/GIMP/2.10` to the specified gimp profile directory.

### Credits

* This project would't be possible without the amazing GIMP Team.
* The Photo in the new Splash is from [Isabella Mariana](https://www.pexels.com/pt-br/@isabella-mariana-1022505)
* The AppImage version is maintaied by [sudo-give-me-coffee](https://github.com/sudo-give-me-coffee/)
* A BIG thanks to all Diolinux's supporters on [Twitch](https://twitch.tv/Diolinux) and [YouTube](https://youtube.com/Diolinux).

