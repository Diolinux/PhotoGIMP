#!/usr/bin/env python

"""
Gimp plugin "Heal transparency"

Copyright 2010 lloyd konneker (bootch at nc.rr.com)

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

"""

from gimpfu import *

gettext.install("resynthesizer", gimp.locale_directory, unicode=True)


def heal_transparency(timg, tdrawable, samplingRadiusParam=50, orderParam=2):
    # precondition should be enforced by Gimp according to image modes allowed.
    if not pdb.gimp_drawable_has_alpha(tdrawable):
        pdb.gimp_message("The active layer has no alpha channel to heal.")
        return

    pdb.gimp_image_undo_group_start(timg)

    # save selection for later restoration.
    # Saving selection channel makes it active, so we must save and restore the active layer
    org_selection = pdb.gimp_selection_save(timg)
    pdb.gimp_image_set_active_layer(timg, tdrawable)

    # alpha to selection
    pdb.gimp_selection_layer_alpha(tdrawable)
    # Want the transparent, not the opaque.
    pdb.gimp_selection_invert(timg)
    # Since transparency was probably anti-aliased (dithered with partial transpancy),
    # grow the selection to get past the dithering.
    pdb.gimp_selection_grow(timg, 1)
    # Remove the alpha from this layer. IE compose with current background color (often white.)
    # Resynthesizer won't heal transparent.
    pdb.gimp_layer_flatten(tdrawable)

    # Call heal selection (not the resynthesizer), which will create a proper corpus.
    # 0 = sample from all around
    pdb.python_fu_heal_selection(
        timg, tdrawable, samplingRadiusParam, 0, orderParam, run_mode=RUN_NONINTERACTIVE
    )

    # Restore image to initial conditions of user, except for later cleanup.

    # restore selection
    pdb.gimp_selection_load(org_selection)

    # Clean up (comment out to debug)
    pdb.gimp_image_undo_group_end(timg)


register(
    "python_fu_heal_transparency",
    N_(
        "Removes alpha channel by synthesis.  Fill outward for edges, inward for holes."
    ),
    "Requires separate resynthesizer plugin.",
    "Lloyd Konneker",
    "Copyright 2010 Lloyd Konneker",
    "2010",
    N_("Heal transparency..."),
    "RGBA, GRAYA",  # !!! Requires an alpha channel to heal
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_INT, "samplingRadiusParam", _("Context sampling width (pixels):"), 50),
        (
            PF_OPTION,
            "orderParam",
            _("Filling order:"),
            2,
            [_("Random"), _("Inwards towards center"), _("Outwards from center")],
        ),
    ],
    [],
    heal_transparency,
    menu="<Image>/Filters/Enhance",
    domain=("resynthesizer", gimp.locale_directory),
)

main()
