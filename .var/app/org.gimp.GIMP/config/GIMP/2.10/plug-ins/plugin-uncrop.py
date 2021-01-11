#!/usr/bin/env python

"""
Gimp plugin "Uncrop"

Increase image/canvas size and synthesize outer band from edge of original.

Author:
lloyd konneker, lkk
Gabriel Almir, avlye

Version:
1.0 lkk 5/15/2009 Initial version in scheme, released to Gimp Registry.
1.1 lkk 9/21/2009 Translate to python.
1.3 avlye 01/11/2020

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
widens the field of view, maintaining perspective of original
Should be undoable, except for loss of selection.
Should work on any image type, any count of layers and channels (although only active layer is affected.)

Programming notes:
Scheme uses - in names, python uses _
Programming devt. cycle:
Initial creation: cp foo.py ~/.gimp-2.6/scripts, chmod +x, start gimp
Refresh:  just copy, no need to restart gimp if the pdb registration is unchanged

IN: Nothing special.  The selection is immaterial but is not preserved.
OUT larger layer and image.  All other layers not enlarged.
"""

from gimpfu import *

gettext.install("resynthesizer", gimp.locale_directory, unicode=True)


def resizeImageCentered(image, percentEnlarge):
    # resize and center image by percent (converted to pixel units)
    priorWidth = pdb.gimp_image_width(image)
    priorHeight = pdb.gimp_image_height(image)

    deltaFraction = (percentEnlarge / 100) + 1.0
    deltaWidth = priorWidth * deltaFraction
    deltaHeight = priorHeight * deltaFraction

    centeredOffX = (deltaWidth - priorWidth) / 2
    centeredOffY = (deltaHeight - priorHeight) / 2

    pdb.gimp_image_resize(image, deltaWidth, deltaHeight, centeredOffX, centeredOffY)


def shrinkSelectionByPercent(image, percent):
    # convert to pixel dimensions
    priorWidth = pdb.gimp_image_width(image)
    priorHeight = pdb.gimp_image_height(image)

    deltaWidth = priorWidth * deltaFraction
    deltaHeight = priorHeight * deltaFraction
    # shrink selection by percent (converted to pixel units)
    deltaFraction = percent / 100

    # !!! Note total shrink percentage is halved (width of band is percentage/2)
    maxDelta = max(deltaWidth, deltaHeight) / 2

    pdb.gimp_selection_shrink(image, maxDelta)


def uncrop(orgImage, drawable, percentEnlargeParam=10):
    """
    Create frisket stencil selection in a temp image to pass as source (corpus) to plugin resynthesizer,
    which does the substantive work.
    """

    if not pdb.gimp_drawable_is_layer(drawable):
        pdb.gimp_message(_("A layer must be active, not a channel."))
        return

    pdb.gimp_image_undo_group_start(orgImage)

    # copy original into temp for later use
    tempImage = pdb.gimp_image_duplicate(orgImage)

    if not tempImage:
        raise RuntimeError, "Failed duplicate image"

    """
    Prepare target: enlarge canvas and select the new, blank outer ring
    """

    # Save original bounds to later select outer band
    pdb.gimp_selection_all(orgImage)
    selectAllPrior = pdb.gimp_selection_save(orgImage)

    # Resize image alone doesn't resize layer, so resize layer also
    resizeImageCentered(orgImage, percentEnlargeParam)
    pdb.gimp_layer_resize_to_image_size(drawable)
    pdb.gimp_selection_load(selectAllPrior)

    # select outer band, the new blank canvas.
    pdb.gimp_selection_invert(orgImage)

    # Assert target image is ready.

    """
    Prepare source (corpus) layer, a band at edge of original, in a dupe.
    Note the width of corpus band is same as width of enlargement band.
    """
    # Working with the original size.
    # Could be alpha channel transparency
    workLayer = pdb.gimp_image_get_active_layer(tempImage)

    if not workLayer:
        raise RuntimeError, "Failed get active layer"

    # Select outer band:  select all, shrink
    pdb.gimp_selection_all(tempImage)
    shrinkSelectionByPercent(tempImage, percentEnlargeParam)
    pdb.gimp_selection_invert(tempImage)  # invert interior selection into a frisket

    # Note that v1 resynthesizer required an inverted selection !!
    # No need to crop corpus to save memory.

    # Note that the API hasn't changed but use_border param now has more values.
    # !!! The crux: use_border param=5 means inside out direction
    pdb.plug_in_resynthesizer(
        orgImage, drawable, 0, 0, 5, workLayer.ID, -1, -1, 0.0, 0.117, 16, 500
    )

    # Clean up.
    # Any errors now are moot.
    pdb.gimp_selection_none(orgImage)
    pdb.gimp_image_remove_channel(orgImage, selectAllPrior)
    pdb.gimp_image_undo_group_end(orgImage)
    pdb.gimp_displays_flush()

    gimp.delete(tempImage)  # Comment out to debug corpus creation.


register(
    "python_fu_uncrop",
    N_(
        "Enlarge image by synthesizing a border that matches the edge, maintaining perspective.  Works best for small enlargement of natural edges. Undo a Crop instead, if possible! "
    ),
    "Requires separate resynthesizer plugin.",
    "Lloyd Konneker",
    "Copyright 2009 Lloyd Konneker",
    "2009",
    N_("Uncrop..."),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_SLIDER, "percentEnlargeParam", _("Percent enlargement"), 10, (0, 100, 1)),
    ],
    [],
    uncrop,
    menu="<Image>/Filters/Enhance",
    domain=("resynthesizer", gimp.locale_directory),
)

main()
