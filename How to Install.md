# How to install PhotoGIMP

## On Linux with flatpak version of GIMP

Extract all hidden folders

- `.icons`
- `.var`
- `.local`

to your Home directory and you are done.

## On Linux with GIMP installed through package manager —or— On&nbsp;*BSD

Extract all hidden folders

- `.icons`
- `.var`
- `.local`

to your Home directory and then move the subfolder 

- `.var/app/org.gimp.GIMP/config/GIMP/2.10`  

to `~/.config/gimp/2.10`.

Afterwards you can delete `.var/app/org.gimp.GIMP` respectively `.var` (if not used otherwise!).

## On macOS

Unpack the whole archive and copy/move only the subfolder  
—or—  
Extract only the subfolder

- `.var/app/org.gimp.GIMP/config/GIMP/2.10`  
(inside the hidden folder `.var`)

into the folder `~/Library/Application Support/GIMP`.

Afterwards you can delete `.var`.
