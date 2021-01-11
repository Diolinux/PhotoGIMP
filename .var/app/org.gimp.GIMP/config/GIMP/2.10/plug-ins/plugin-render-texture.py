#!/usr/bin/env python

'''
Gimp plugin.

Create new image having texture synthesized from the selection.
Works best if selection is natural (fractal).
Can work with man-made regular texture.
Works worst with man-made, structured but not regular, symbols.
Sometimes called rendering a texture.

Requires resynthesizer plug-in.

Authors:
lloyd konneker, lkk, bootch at nc.rr.com
Gabriel Almir, avlye, avlye.me

Version:
1.0 lkk 7/15/2010 Initial version
1.1 lkk 4/10/2011 Fixed a bug with layer types impacting greyscale images.
1.3 avlye 01/10/2020 Minor changes for improving developer experience

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


The effect for users:
Similar to "Fill resynthesized pattern" except:
  - here the arguments are reversed: you select a texture and create a new image
    instead of selecting an area and choosing a pattern.
  - here the result is less random (since Fill resynthesized adds noise.)
Different from tiling since:
  - seamless and irregular pattern

The continuum of randomness versus speed:
  - Filters.Map.Tile is fast but has seams and regular pattern (even if you use "Make Seamless" first.)
  - Filter.Render.Texture a tile followed by tiling is seamless but still has regularity.
  - Filte.Render.Texture an entire image is slower but seamless and moderately irregular.
  - Edit.Fill with resynthesized pattern is slowest but seamless and highly irregular, unpatterned.

This filter is not tiling (instead resynthesizing) but makes
an image that you can then use to tile with especially if
you choose the option to make the edges suitable for tiling.

IN: The selection (or the entire active drawable) is the source of texture and is not changed.
OUT New image, possibly resized canvas, same scale and resolution.

TODO a quality setting
'''

from gimpfu import *

gettext.install("resynthesizer", gimp.locale_directory, unicode=True)

debug = False


def new_resized_image(image, resize_ratio):
  # Create new image resized by a ratio from *selection* in the old image

  (is_selection, ulx, uly, lrx, lry) = pdb.gimp_selection_bounds(image)

  if not is_selection :
    # Resynthesizer will use the entire source image as corpus.
    # Resize new image in proportion to entire source image.
    new_width = int(pdb.gimp_image_width(image) * resize_ratio)
    new_height = int(pdb.gimp_image_height(image) * resize_ratio)
    new_type = pdb.gimp_image_base_type(image)  # same as source
  else :
    # Resize new image in proportion to selection in source
    new_width = int((lrx - ulx) * resize_ratio)
    new_height = int((lry - uly) * resize_ratio)

  new_basetype = pdb.gimp_image_base_type(image)  # same as source
  new_layertype = pdb.gimp_drawable_type(pdb.gimp_image_get_active_layer(image))
  new_image = pdb.gimp_image_new(new_width, new_height, new_basetype)

  # !!! Note that gimp_layer_new wants a layer type, not an image basetype
  new_drawable = pdb.gimp_layer_new(new_image, new_width, new_height,
    new_layertype, "Texture", 100, NORMAL_MODE)
  pdb.gimp_image_add_layer(new_image, new_drawable, 0)

  return new_image, new_drawable


def display_image(image):
  try:
    gimp.Display(image)
  except gimp.error:
    pass  # If runmode is NONINTERACTIVE, expect gimp_display_new() to fail

  gimp.displays_flush()


def render_texture(image, drawable, resize_ratio=2, make_tile=0):
  '''
  Create a randomized texture image from the selection.
  The image can be suited for further, seamless tiling.
  The image is same scale and resolution but resized from the selection.
  Not undoable, no changes to the source (you can just delete the new image.)

  A selection in the source image is optional.
  If there is no selection, the resynthesizer will use the entire source image.
  '''

  # Its all or nothing, user must delete new image if not happy.
  pdb.gimp_image_undo_disable(image)

  '''
  Create new image, optionally resized, and display for it.
  '''
  new_image, new_drawable = new_resized_image(image, resize_ratio)
  pdb.gimp_image_undo_disable(new_image)

  if not new_drawable:
    raise RuntimeError, "Failed create layer."

  # If using new resynthesizer with animation for debugging
  if debug:
    display_image(new_image)

  '''
  copy original into temp and crop it to the selection to save memory in resynthesizer
  '''
  temp_image = pdb.gimp_image_duplicate(image)

  if not temp_image:
      raise RuntimeError, "Failed duplicate image"

  # Get bounds, offset of selection
  (is_selection, ulx, uly, lrx, lry) = pdb.gimp_selection_bounds(image)

  if is_selection:
    pdb.gimp_image_crop(temp_image, lrx - ulx, lry - uly, ulx, uly)

  # Don't flatten because it turns transparency to background (white usually)
  work_layer = pdb.gimp_image_get_active_layer(temp_image)

  if not work_layer:
    raise RuntimeError, "Failed get active layer"

  # Insure the selection is all (not necessary, resynthesizer will use all if no selection.)
  pdb.gimp_selection_all(temp_image)

  # Settings for making edges suitable for seamless tiling afterwards.
  # That is what these settings mean in the resynthesizer:
  # wrap context probes in the target so that edges of target will be suitable for seamless tiling.
  # I.E. treat the target as a sphere when matching.
  tile = (1, 1) if make_tile else (0, 0)

  # Call resynthesizer
  # use_border is moot since there is no context (outside the target) in the newImage.
  # The target is the entire new image, the source is the cropped copy of the selection.
  #
  # 9 neighbors (a 3x3 patch) and 200 tries for speed, since new image is probably large
  # and source is probably natural (fractal), where quality is not important.

  # For version of resynthesizer with uninverted selection
  # !!! Pass -1 for ID of no layer, not None
  pdb.plug_in_resynthesizer(new_image, new_drawable, tile[0], tile[1], 0, work_layer.ID, -1, -1, 0.0, 0.117, 9, 200)

  display_image(new_image)

  # Clean up.
  pdb.gimp_image_delete(temp_image)
  pdb.gimp_image_undo_enable(image)
  pdb.gimp_image_undo_enable(new_image)

  return new_image

register(
  "python_fu_render_texture",
  N_("Create a new image with texture from the current image or selection. Optionally, create image edges suited for further, seamless tiling. "),
  "New image is the same scale but seamless and irregular.  Use 'Map>Tile' for less randomness. Use 'Edit>Fill resynthesized pattern' for more randomness. Requires separate resynthesizer plugin.",
  "Lloyd Konneker",
  "Copyright 2010 Lloyd Konneker",
  "2010",
  N_("_Texture..."),
  "RGB*, GRAY*",
  [
    (PF_IMAGE, "image",       "Input image", None),
    (PF_DRAWABLE, "drawable", "Input drawable", None),
    # Spinner is digital and linear, slider is analog but exponential
    (PF_SPINNER, "resize_ratio", _("Ratio of size of new image to source selection"), 2, (0.5, 10, 0.5)),
    (PF_TOGGLE, "make_tile", _("Make new image edges suitable for seamless tiling"), 0 )
  ],
  [(PF_IMAGE, "new_image", "New, synthesized texture.")],
  render_texture,
  menu="<Image>/Filters/Render",
  domain=("resynthesizer", gimp.locale_directory)
  )

main()
