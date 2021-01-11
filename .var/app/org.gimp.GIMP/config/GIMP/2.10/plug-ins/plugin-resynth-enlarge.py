#!/usr/bin/env python

'''
Gimp plugin "Enlarge and resynthesize"

Author:
lloyd konneker
Based on smart_enlarge.scm 2000 by Paul Harrison.

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

  Scale image up.
  Resynthesize with:
    corpus = original size image
    in map = original size image but scaled up and down to blur
    out map = scaled up image

  This restores the detail that scaling up looses.
  It maintains the aspect ratio of all image features.

  Unlike the original smart-enlarge.scm, this alters the original image.

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

  # scale input map down and back, to blur
  width = pdb.gimp_drawable_width(drawable)
  height = pdb.gimp_drawable_height(drawable)
  pdb.gimp_image_scale(temp_image1, width/scale_factor, height/scale_factor)
  pdb.gimp_image_scale(temp_image1, width, height)

  # scale up the image
  pdb.gimp_image_scale(image, width * scale_factor, height*scale_factor)

  # Resynthesize to restore details.
  # Note there should not be a selection. TODO
  pdb.plug_in_resynthesizer(
      image,
      drawable,
      0, 0, 0,
      temp_layer2.ID,  # corpus
      temp_layer1.ID,  # input map
      drawable.ID,     # output map is scaled up original itself
      1.0, 0.117, 8, 500)

  pdb.gimp_image_delete(temp_image1)
  pdb.gimp_image_delete(temp_image2)


if __name__ == "__main__" :
  register(
    "python_fu_enlarge_resynthesized",
    N_("Enlarge image and synthesize to sharpen."),
    "Requires separate resynthesizer plugin",
    "Lloyd Konneker",
    "Copyright 2000 Paul Harrison, 2010 Lloyd Konneker",
    "2010",
    N_("Enlarge & sharpen..."),
    "RGB*, GRAY*",
    [
      (PF_IMAGE, "image",       "Input image", None),
      (PF_DRAWABLE, "drawable", "Input drawable", None),
      (PF_ADJUSTMENT, "scale_factor", _("Scale by:"), 2, (1, 32, 0.1))
    ],
    [],
    plugin_main,
    menu="<Image>/Filters/Enhance",
    domain=("resynthesizer", gimp.locale_directory)
    )

  main()


