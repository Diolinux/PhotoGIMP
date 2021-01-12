#!/usr/bin/env python

"""
Gimp plugin.
Transfer style (color and surface texture) from a source image to the active, target image.

Requires resynthesizer plug-in.

Authors:
lloyd konneker, lkk
Gabriel Almir, avlye

Version:
1.0 lkk 7/15/2010 Initial version.  Released to Gimp Registry.
1.1 lkk 8/1/2010 Unreleased
1.2 lkk 8/10/2010
1.3 avlye 01/10/2021

Change log:
_________________
1.1
    Bug: Fixed test of mode variable, since it is a string, needs explicit test for == 1
    Bug: Added remove Selection Mask copy channel in make_grayscale_map
1.2
    Changes for new resynthesizer: no need to synchronize, remove alphas
    Fixed improper adjustment of contrast of source: only adjust source map.
1.3
    Minor changes to improve developer experience

TODO
a quality setting that changes the parameters to resynth

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


Users Guide
___________

What this plugin does:

Transfers artistic style from one image to another.  Often the source is an artistic image and the target is a realistic, photo image.  But you can also transfer between artistic images or between realistic images.

An artist might say this plugin "renders in the media and style from another image."  A computer user might say it "renders in the theme of another image."

Transferring style means transferring small scale features (color and texture) to an image while retaining large scale features (objects.)

Map can mean "transfer and transform".  This plugin gives limited control of the transform.  That is, colors are usually mapped to similar colors (hues.)  This plugin is not intended to do "false color" (but it might have that effect.)

Style can mean "color and surface."  Texture mapping usually means just surface (pattern of brightness, e.g. a weave or grain.)  This plugin can transfer both color and surface.

This plugin has more effect than just an overlay or screen or a map.  A screen usually applies a texture uniformly across an image.  This plugin transfers style in patches.  The style in a region can come from any patch of the source, or be synthesized (mixed) from many patches of the source.

The transfer is not exactly a copy, again because of optional synthesis or mixing.

About the selection:

Usually you transfer between separate images, the target and source images.  You can make a selection in either image, or both.  If there is no selection, the plugin uses the entire layer.

The target is the active LAYER and you can choose the source LAYER.  Note that the plugin doesn't use everything visible in an image, just one layer.

SPECIAL CASE: If the target and source layers are in the same image, the source style comes from the inverse of the selection in the source layer.  Similarly, if the target and source layers are the same layer, the target is the selection and the style comes from the inverse of the selection, i.e. outside the selection.  In this case, the effect is little if there is no difference in texture between the inside and outside of the selection, or a distort, if there is a difference.

About the settings:

"Percent transfer:" how much style to transfer.  Less transfer means the effect retains the large scale objects of the original, but gives the image a grainy surface.  More transfer means the effect leaves only a ghost of the large scale objects, and almost fully copies the style image (with less synthesis or mixing.)

"Map by:" whether color affects the style transfer, when both target and source are in color.  If you choose "color and brightness", style colors are more apt to be transferred to areas with same colors.  However, it is still possible that colors are radically transformed, if the surface (brightness pattern) is a better match.  If you choose "brightness only", style colors are more apt to be radically transformed.

This setting has less effect if there are no color matches between source and target (e.g. one is all red and the other is all green) or if the target image is GRAY.  This setting has NO effect if the source image or both images are GRAY.

About image modes:

You can transfer style between any combination of RGB and GRAY images.   The plugin changes the mode of the target to the mode of the source as necessary.

Why this plugin:

This plugin is a front-end to the separate resynthesizer plugin.  This plugin simplifies using the resynthesizer plugin.  It automates many steps.  It hides several complexities of the resynthesizer plugin:  selection, modes, alpha channels, and settings.



Programming notes:
_________________

IN: The active image and layer.
    The selection in the active image.
    The selection in any layers chosen for source.
OUT: The active image, altered.  The source is unaltered.
  Target mode can be altered, but with the implied consent of the user.

The print stmts go to the console, info to advanced users and debuggers.

This plugin is mostly about UI and simplifications for user (the engine does the image processing):
making maps automatically
synchronization of alphas (note the new resynthesizer ignores alphas.)
synchronization of modes
abstracting the settings
contrast adjustment

"""

from gimpfu import *
from math import acos, pi

gettext.install("resynthesizer", gimp.locale_directory, unicode=True)

# True if you want to display and retain working, temporary images
debug = False


def display_debug_image(image):
    if debug:
        try:
            pdb.gimp_display_new(image)
            pdb.gimp_displays_flush()
        except RuntimeError:
            pass  # if run-mode not interactive, Gimp throws


def make_grayscale_map(image, drawable):
    """
    Make a grayscale copy for a map.

    Maps must be same size as their parent image.

    If image is already grayscale, return it without copying.

    Maps don't need a selection, since the resynthesizer looks at parent drawables for the selection.
    """
    if pdb.gimp_image_base_type(image) == GRAY:
        return image, drawable

    # Save selection, copy entire image, and restore
    original_selection = pdb.gimp_selection_save(image)
    pdb.gimp_selection_all(image)  # copy requires selection
    pdb.gimp_edit_copy(drawable)

    if original_selection:
        pdb.gimp_selection_load(original_selection)  # restore selection in image
        pdb.gimp_image_remove_channel(
            image, original_selection
        )  # cleanup the copied selection mask
        # !!! Note remove_channel not drawable_delete

    # Make a copy, greyscale
    temp_image = pdb.gimp_edit_paste_as_new()
    pdb.gimp_image_convert_grayscale(temp_image)
    display_debug_image(temp_image)
    temp_drawable = pdb.gimp_image_get_active_drawable(temp_image)
    return temp_image, temp_drawable


def synchronize_modes(target_image, source_image):
    """
    User-friendliness:
    If mode of target is not equal to mode of source source, change modes.
    Resynthesizer requires target and source to be same mode.
    Assert target is RGB or GRAY (since is precondition of plugin.)
    UI decision: make this quiet, presume user intends mode change.
    But don't permanently change mode of source.
    Always upgrade GRAY to RGB, not downgrade RGB to GRAY.
    """
    target_mode = pdb.gimp_image_base_type(target_image)
    source_mode = pdb.gimp_image_base_type(source_image)
    if target_mode != source_mode:
        # print("Map style: converted mode\n.")
        if target_mode == GRAY:
            pdb.gimp_image_convert_rgb(target_image)
        else:  # target is RGB and source is GRAY
            # Assert only convert a copy of source,
            # user NEVER intends original source be altered.
            pdb.gimp_image_convert_rgb(source_image)


def copy_selection_to_image(drawable):
    """
    If image has a selection, copy selection to new image, and prepare it for resynthesizer,
    else return a copy of the entire source image.
    This is called for the source image, where it helps performance to reduce size and flatten.
    """
    image = pdb.gimp_drawable_get_image(drawable)

    # copy selection or whole image
    pdb.gimp_edit_copy(drawable)
    image_copy = pdb.gimp_edit_paste_as_new()
    # Activate layer, and remove alpha channel
    pdb.gimp_image_flatten(image_copy)
    layer_copy = pdb.gimp_image_get_active_layer(image_copy)
    # In earlier version, futzed with selection to deal with transparencey
    display_debug_image(image_copy)

    return image_copy, layer_copy


def synchronize_contrast(drawable, source_drawable, percent_transfer):
    """
    Adjust contrast of source, to match target.
    Adjustment depends inversely on percent_transfer.
    Very crude histogram matching.
    """
    # histogram upper half: typical mean is 191 (3/4*255). Skew of mean towards 255 means high contrast.
    mean, deviation, median, pixels, count, percentile = pdb.gimp_histogram(
        drawable, HISTOGRAM_VALUE, 128, 255
    )
    (
        source_mean,
        source_deviation,
        source_median,
        pixels,
        count,
        percentile,
    ) = pdb.gimp_histogram(source_drawable, HISTOGRAM_VALUE, 128, 255)

    # if mean > source_mean:  # target has more contrast than source
    # Adjust contrast of source.
    # Inversely proportional to percent transfer.
    # 2.5 is from experimentation with gimp_brightness_contrast which seems linear in its effect.
    contrast_control = (mean - source_mean) * 2.5 * (1 - (percent_transfer / 100))

    # clamp to valid range
    contrast_control = max(min(contrast_control, 127), -127)

    pdb.gimp_brightness_contrast(source_drawable, 0, contrast_control)

    # For experimentation, print new values
    (
        source_mean,
        source_deviation,
        source_median,
        pixels,
        count,
        percentile,
    ) = pdb.gimp_histogram(source_drawable, HISTOGRAM_VALUE, 128, 255)

    # print "Map style: Source contrast changed by ", contrast_control
    # print "Map style: Target and source upper half histogram means", mean, source_mean


def calculate_map_weight(percent_transfer):
    """
    This is a GUI design discussion.
    Transform percent_transfer to map_weight parameter to resynthesizer.
    For resynthesizer:
    map weight 0 means copy source to target, meaning ALL style.
    map weight 0.5 means just a grainy transfer of style (as little as is possible.)
    Transform from a linear percent GUI, because user more comfortable than with a ratio [.5, 0]
    which is backwards to the usual *less on the left*.
    By experiment, a sinusoid gives good results for linearizing the non-linear map_weight control.
    """
    return acos((percent_transfer / 100) * 2 - 1) / (2 * pi)


def transfer_style(image, drawable, source_drawable, percent_transfer, map_mode):
    """
    Main body of plugin to transfer style from one image to another.

    !!! Note map_mode is type string, "if map_mode:" will not work.
    """

    pdb.gimp_image_undo_group_start(image)

    # Get image of source drawable
    source_image = pdb.gimp_drawable_get_image(source_drawable)

    """
  User-friendliness.
  Note the drawable chooser widget in Pygimp does not allow us to prefilter INDEXED mode.
  So check here and give a warning.
  """
    # These are the originals base types, and this plugin might change the base types
    original_source_base_type = pdb.gimp_image_base_type(source_image)
    original_target_base_type = pdb.gimp_image_base_type(image)

    if original_source_base_type == INDEXED:
        pdb.gimp_message(_("The style source cannot be of mode INDEXED"))
        return

    if image == source_image and drawable == source_drawable:
        is_source_copy = False
        """
    If source is same as target,
    then the old resynthesizer required a selection (engine used inverse selection for corpus).
    New resynthesizer doesn't need a selection.
    If source same as target, effect is similar to a blur.
    """
        # assert modes and alphas are same (since they are same layer!)
    else:  # target layer is not the source layer (source could be a copy of target, but effect is none)
        # Copy source always, for performance, and for possible mode change.
        is_source_copy = True
        source_image, source_drawable = copy_selection_to_image(source_drawable)

        # Futz with modes if necessary.
        synchronize_modes(image, source_image)

        """
    Old resythesizer required both images to have alpha, or neither.
    synchronize_alphas( drawable, source_drawable)
    """

    """
  TODO For performance, if there is a selection in target, it would be better to copy
  selection to a new layer, and later merge it back (since resynthesizer engine reads
  entire target into memory.  Low priority since rarely does user make a selection in target.
  """

    """
  !!! Note this plugin always sends maps to the resynthesizer,
  and the "percent transfer" setting is always effective.
  However, maps may not be separate,copied images unless converted to grayscale.
  """

    # Copy and reduce maps to grayscale: at the option of the user
    # !!! Or if the target was GRAY and source is RGB, in which case maps give a better result.
    # Note that if the target was GRAY, we already upgraded it to RGB.
    if map_mode == 1 or (
        original_source_base_type == RGB and original_target_base_type == GRAY
    ):
        # print "Map style: source mode: ", original_source_base_type, " target mode: ", original_target_base_type
        # print "Map style: Converting maps to grayscale"
        # Convert mode, but in new temp image and drawable
        target_map_image, target_map_drawable = make_grayscale_map(image, drawable)
        source_map_image, source_map_drawable = make_grayscale_map(
            source_image, source_drawable
        )

        target_map = target_map_drawable
        source_map = source_map_drawable
        # later, delete temp images

        # User control: adjust contrast of source_map as a function of percent transfer
        # Hard to explain why, but experimentation shows result more like user expectation.
        # TODO This could be improved.
        # !!! Don't change the original source, only a temporary map we created
        synchronize_contrast(drawable, source_map, percent_transfer)
    else:
        # !!! Maps ARE the target and source, not copies
        source_map = source_drawable
        target_map = drawable

    """
  Parameters to resynthesizer:

  htile and vtile = 1 since it reduces artifacts around edge

  map_weight I linearize since easier on users than an exponential

  use_border = 1 since there might be a selection and context (outside target).

  9 neighbors (a 3x3 patch) and 200 tries for speed

  """

    map_weight = calculate_map_weight(percent_transfer)

    # !!! This is for version of resynthesizer, with an uninverted selection
    pdb.plug_in_resynthesizer(
        image,
        drawable,
        1,
        1,
        1,
        source_drawable.ID,
        source_map.ID,
        target_map.ID,
        map_weight,
        0.117,
        9,
        200,
    )

    # Clean up.
    # Delete working images: separate map images and copy of source image
    if not debug:
        if map_mode == 1:  # if made working map images
            pdb.gimp_image_delete(target_map_image)
            pdb.gimp_image_delete(source_map_image)
        if is_source_copy:  # if created a copy earlier
            pdb.gimp_image_delete(source_image)

    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_displays_flush()


register(
    "python_fu_map_style",
    N_("Transfer style (color and surface) from a chosen source to the active layer. "),
    "Transforms image using art media and style from another image.  Maps or synthesizes texture or theme from one image onto another. Requires separate resynthesizer plugin.",
    "Lloyd Konneker (bootch nc.rr.com)",
    "Copyright 2010 Lloyd Konneker",
    "2010",
    N_("Style..."),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_DRAWABLE, "source_drawable", _("Source of style:"), None),
        (PF_SLIDER, "percent_transfer", _("Percent transfer:"), 0, (10, 90, 10.0)),
        (
            PF_RADIO,
            "map_mode",
            _("Map by:"),
            0,
            ((_("Color and brightness"), 0), (_("Brightness only"), 1)),
        ),
    ],
    [],
    transfer_style,
    menu="<Image>/Filters/Map",
    domain=("resynthesizer", gimp.locale_directory),
)

main()
