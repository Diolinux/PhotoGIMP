#!/usr/bin/env python

'''
Gimp plugin "Heal selection"

Copyright 2009 lloyd konneker (bootch at nc.rr.com)
Based on smart_remove.scm Copyright 2000 by Paul Harrison.

Version:
  1.0 lloyd konneker lkk 9/21/2009 Initial version in python.
  (See release notes for differences over P. Harrison's prior version in scheme language.)

License:

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  The GNU Public License is available at
  http://www.gnu.org/copyleft/gpl.html

'''

from gimpfu import *

gettext.install("resynthesizer", gimp.locale_directory, unicode=True)

debug = False

def heal_selection(timg, tdrawable, samplingRadiusParam=50, directionParam=0, orderParam=0):
  '''
  Create stencil selection in a temp image to pass as source (corpus) to plugin resynthesizer,
  which does the substantive work.
  '''
  if pdb.gimp_selection_is_empty(timg):
    pdb.gimp_message(_("You must first select a region to heal."))
    return

  pdb.gimp_image_undo_group_start(timg)

  targetBounds = tdrawable.mask_bounds

  # In duplicate image, create the sample (corpus).
  # (I tried to use a temporary layer but found it easier to use duplicate image.)
  tempImage = pdb.gimp_image_duplicate(timg)

  if not tempImage:
      raise RuntimeError, "Failed duplicate image"

  # !!! The drawable can be a mask (grayscale channel), don't restrict to layer.
  work_drawable = pdb.gimp_image_get_active_drawable(tempImage)

  if not work_drawable:
      raise RuntimeError, "Failed get active drawable"

  '''
  grow and punch hole, making a frisket iow stencil iow donut

  '''
  orgSelection = pdb.gimp_selection_save(tempImage) # save for later use
  pdb.gimp_selection_grow(tempImage, samplingRadiusParam)
  # ??? returns None , docs say it returns SUCCESS

  # !!! Note that if selection is a bordering ring already, growing expanded it inwards.
  # Which is what we want, to make a corpus inwards.

  grownSelection = pdb.gimp_selection_save(tempImage)

  # Cut hole where the original selection was, so we don't sample from it.
  # !!! Note that gimp enums/constants are not prefixed with GIMP_
  pdb.gimp_selection_combine(orgSelection, CHANNEL_OP_SUBTRACT)

  '''
  Selection (to be the corpus) is donut or frisket around the original target T
    xxx
    xTx
    xxx
  '''

  # crop the temp image to size of selection to save memory and for directional healing!!
  frisketBounds = grownSelection.mask_bounds

  frisketLowerLeftX = frisketBounds[0]
  frisketLowerLeftY = frisketBounds[1]
  frisketUpperRightX = frisketBounds[2]
  frisketUpperRightY = frisketBounds[3]

  targetLowerLeftX = targetBounds[0]
  targetLowerLeftY = targetBounds[1]
  targetUpperRightX = targetBounds[2]
  targetUpperRightY = targetBounds[3]

  frisketWidth = frisketUpperRightX - frisketLowerLeftX
  frisketHeight = frisketUpperRightY - frisketLowerLeftY

  # User's choice of direction affects the corpus shape, and is also passed to resynthesizer plugin
  if directionParam == 0: # all around
      # Crop to the entire frisket
      newWidth, newHeight, newLLX, newLLY = ( frisketWidth, frisketHeight,
        frisketLowerLeftX, frisketLowerLeftY )
  elif directionParam == 1: # sides
      # Crop to target height and frisket width:  XTX
      newWidth, newHeight, newLLX, newLLY =  ( frisketWidth, targetUpperRightY-targetLowerLeftY,
        frisketLowerLeftX, targetLowerLeftY )
  elif directionParam == 2: # above and below
      # X Crop to target width and frisket height
      # T
      # X
      newWidth, newHeight, newLLX, newLLY = ( targetUpperRightX-targetLowerLeftX, frisketHeight,
        targetLowerLeftX, frisketLowerLeftY )

  # Restrict crop to image size (condition of gimp_image_crop) eg when off edge of image
  newWidth = min(pdb.gimp_image_width(tempImage) - newLLX, newWidth)
  newHeight = min(pdb.gimp_image_height(tempImage) - newLLY, newHeight)
  pdb.gimp_image_crop(tempImage, newWidth, newHeight, newLLX, newLLY)

  # Encode two script params into one resynthesizer param.
  # use border 1 means fill target in random order
  # use border 0 is for texture mapping operations, not used by this script
  if not orderParam :
      useBorder = 1   # User wants NO order, ie random filling
  elif orderParam == 1 :  # Inward to corpus.  2,3,4
      useBorder = directionParam + 2   # !!! Offset by 2 to get past the original two boolean values
  else:
      # Outward from image center.
      # 5+0=5 outward concentric
      # 5+1=6 outward from sides
      # 5+2=7 outward above and below
      useBorder = directionParam + 5

  # Note that the old resynthesizer required an inverted selection !!

  if debug:
    try:
      gimp.Display(tempImage)
      gimp.displays_flush()
    except RuntimeError:  # thrown if non-interactive
      pass

    from time import sleep
    sleep(2)

  # Not necessary to restore image to initial condition of selection, activity,
  # the original image should not have been changed,
  # and the resynthesizer should only heal, not change selection.

  # Note that the API hasn't changed but use_border param now has more values.
  pdb.plug_in_resynthesizer(timg, tdrawable, 0,0, useBorder, work_drawable.ID, -1, -1, 0.0, 0.117, 16, 500)

  # Clean up (comment out to debug)
  gimp.delete(tempImage)
  pdb.gimp_image_undo_group_end(timg)


register(
  "python_fu_heal_selection",
  N_("Heal the selection from surroundings as if using the heal tool."),
  "Requires separate resynthesizer plugin.",
  "Lloyd Konneker",
  "2009 Lloyd Konneker",  # Copyright
  "2009",
  N_("_Heal selection..."),
  "RGB*, GRAY*",
  [
    (PF_IMAGE, "image",       "Input image", None),
    (PF_DRAWABLE, "drawable", "Input drawable", None),
    (PF_INT, "samplingRadiusParam", _("Context sampling width (pixels):"), 50),
    (PF_OPTION,"directionParam",   _("Sample from:"),0,[_("All around"),_("Sides"),_("Above and below")]),
    (PF_OPTION, "orderParam",   _("Filling order:"), 0, [_("Random"),
      _("Inwards towards center"), _("Outwards from center") ])
  ],
  [],
  heal_selection,
  menu="<Image>/Filters/Enhance",
  domain=("resynthesizer", gimp.locale_directory)
  )

main()
