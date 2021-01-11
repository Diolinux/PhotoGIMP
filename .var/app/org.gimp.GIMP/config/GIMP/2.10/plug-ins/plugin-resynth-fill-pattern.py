#!/usr/bin/env python

"""
Gimp plugin "Fill with pattern seamless..."
Front end to the resynthesizer plugin to make a seamless fill.

Copyright 2011 lloyd konneker
Idea by Rob Antonishen

Version:
1.0 lloyd konneker

During development, remember to make it executable!!!
And to remove older versions, both .scm and .py that might hide it.

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

"""

from gimpfu import *

gettext.install("resynthesizer", gimp.locale_directory, unicode=True)

debug = False


def layer_from_pattern(image, pattern):
    """
    Create a new image and layer having the same size as a pattern.
    """
    new_basetype = pdb.gimp_image_base_type(image)  # same as source
    new_layertype = pdb.gimp_drawable_type(pdb.gimp_image_get_active_layer(image))
    pattern_width, pattern_height, bpp = pdb.gimp_pattern_get_info(pattern)
    new_image = pdb.gimp_image_new(pattern_width, pattern_height, new_basetype)

    # !!! Note that gimp_layer_new wants a layer type, not an image basetype
    new_drawable = pdb.gimp_layer_new(
        new_image,
        pattern_width,
        pattern_height,
        new_layertype,
        "Texture",
        100,
        NORMAL_MODE,
    )
    pdb.gimp_image_add_layer(new_image, new_drawable, 0)

    return new_image, new_drawable


def guts(image, drawable, pattern):
    """ Crux of algorithm """

    # Make drawble from pattern
    pattern_image, pattern_layer = layer_from_pattern(image, pattern)

    # Fill it with pattern
    # NOT pass pattern_layer.ID !!!
    pdb.gimp_drawable_fill(pattern_layer, PATTERN_FILL)

    if debug:
        gimp.Display(pattern_image)
        gimp.displays_flush()

    # Resynthesize the selection from the pattern without using context
    # 0,0,0: Not use_border (context), not tile horiz, not tile vert
    # -1, -1, 0: No maps and no map weight
    # DO pass pattern_layer.ID !!!
    # Resynthesizer is an engine, never interactive
    pdb.plug_in_resynthesizer(
        image, drawable, 0, 0, 0, pattern_layer.ID, -1, -1, 0, 0.05, 8, 300
    )

    # Clean up
    if not debug:
        # Delete image that is displayed throws RuntimeError
        pdb.gimp_image_delete(pattern_image)


def plugin_main(image, drawable, pattern):
    """
    Main: the usual user-friendly precondition checking, postcondition cleanup.
    pattern is a string
    """
    # User_friendly: if no selection, use entire image.
    # But the resynthesizer does that for us.

    # Save/restore the context since we change the pattern
    pdb.gimp_context_push()
    pdb.gimp_context_set_pattern(pattern)
    guts(image, drawable, pattern)
    pdb.gimp_context_pop()

    gimp.displays_flush()


register(
    "python_fu_fill_pattern_resynth",
    N_("Seamlessly fill with a pattern using synthesis."),
    "Requires separate resynthesizer plugin.",
    "Lloyd Konneker",
    "Copyright 2011 Lloyd Konneker",
    "2011",
    N_("_Fill with pattern seamless..."),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_PATTERN, "pattern", _("Pattern:"), "Maple Leaves"),
    ],
    [],
    plugin_main,
    menu="<Image>/Edit",
    domain=("resynthesizer", gimp.locale_directory),
)

main()
