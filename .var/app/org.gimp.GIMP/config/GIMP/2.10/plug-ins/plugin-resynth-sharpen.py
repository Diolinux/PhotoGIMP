#!/usr/bin/env python

'''
Gimp plugin "Sharpen by resynthesis"
Requires resynthesizer plug_in (v2).

Author:
lloyd konneker (bootch at nc.rr.com)
Based on smart_enlarge.scm 2000 by Paul Harrison.
Gabriel Almir, avlye

Version:
1.0 lloyd konneker lkk 2010 Initial version in python.


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

def plugin_main(image, drawable, scale_factor):
  '''
  Algorithm:

  Resynthesize with:
    corpus = smaller image
    in map = smaller image but scaled up and down to blur
    out map = original image

  TODO undo

  original did not accept an alpha channel
  '''


  temp_image1 = pdb.gimp_image_duplicate(image)  # duplicate for in map
  if not temp_image1:
    raise RuntimeError, "Failed duplicate image"
  temp_image2 = pdb.gimp_image_duplicate(image)  # duplicate for corpus
  if not temp_image2:
    raise RuntimeError, "Failed duplicate image"
  temp_layer1 = pdb.gimp_image_get_active_layer(temp_image1)
  if not temp_layer1:
    raise RuntimeError, "Failed get active layer"
  temp_layer2 = pdb.gimp_image_get_active_layer(temp_image2)
  if not temp_layer2:
    raise RuntimeError, "Failed get active layer"


  width = pdb.gimp_drawable_width(drawable)
  height = pdb.gimp_drawable_height(drawable)


  # scale input image down, for corpus map
  pdb.gimp_image_scale(temp_image2, width/scale_factor, height/scale_factor)

  # scale input image way down, then back up to, to blur, for corpus
  # Final size is same size as corpus map.
  pdb.gimp_image_scale(temp_image1, width / (2 * scale_factor), height / (2 * scale_factor) )
  pdb.gimp_image_scale(temp_image1, width/scale_factor, height/scale_factor)

  # Resynthesize to restore details.
  # Note there should not be a selection. TODO
  pdb.plug_in_resynthesizer(
      image,
      drawable,
      0, 0, 0,
      temp_layer2.ID,  # corpus is smaller original
      temp_layer1.ID,  # input map is blurred smaller original
      drawable.ID,     # output map is original itself
      1.0, 0.117, 8, 500)

  pdb.gimp_image_delete(temp_image1)
  pdb.gimp_image_delete(temp_image2)


register(
  "python_fu_sharpen_resynthesized",
  N_("Sharpen image by synthesis."),
  "Requires separate resynthesizer plugin.",
  "Lloyd Konneker",
  "Copyright 2000 Paul Harrison, 2010 Lloyd Konneker",
  "2010",
  N_("Sharpen by synthesis..."),
  "RGB*, GRAY*",
  [ (PF_IMAGE, "image",       "Input image", None),
    (PF_DRAWABLE, "drawable", "Input drawable", None),
    (PF_ADJUSTMENT, "sharpen_factor", _("Sharpening:"), 2, (1, 32, 0.1)),
  ],
  [],
  plugin_main,
  menu="<Image>/Filters/Enhance",
  domain=("resynthesizer", gimp.locale_directory)
  )

main()


