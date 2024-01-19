#!/usr/bin/python3
"""! @brief Parses pngs from a spritesheet, encoding each color to a char per pixel."""

##
# @file png_resize.py
#
# @brief Program that resizes pngs to a desired size and overwrites them.
#
# @section description_png_resize Description
# The program overwrites the passed pngs with the resized version.
#
# Program expects the spritesheet filename as first argument, then
#   the sprite width,
#   the sprite heigth.
#
# @section libraries_main Libraries/Moodules
# - Pillow (https://pillow.readthedocs.io/en/stable/)
#   - Access to image manipulation functions.
# - sys standard library (https://docs.python.org/3/library/sys.html)
#   - Access to command line arguments.
# - os standard library (https://docs.python.org/3/library/os.html)
#   - Access to program name.
#
# @section notes_png_resize Notes
# - The pngs are overwritten by default.
#
# @section todo_png_resize TODO
# - Offer option to output to new files and not overwrite.
#
# @section author_spritesheet Author(s)
# - Created by jgabaut on 24/02/2023.
# - Modified by jgabaut on 19/01/2024.

# Imports
import os
import sys
from PIL import Image

SCRIPT_VERSION = "0.1.0"
STRING_ARGS = "<sprites_directory> <sprite_width> <sprite_height>"

# Functions
def usage():
    """! Prints correct invocation."""
    print("Wrong arguments. Needed: directory, desired sprite width, desired sprite height.")
    print(f"\nUsage:\tpython {os.path.basename(__file__)} {STRING_ARGS}")

def resize_sprites(directory, target_size_x, target_size_y):
    """! Resizes all png files in the passed directory to the specified size.
    @param directory   The input directory with the pngs.
    @param target_size_x   The target width.
    @param target_size_y   The target height.
    """
    # Set the target size
    size = (target_size_x, target_size_y)

    # Loop through all PNG files in the current directory
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            # Open the file
            with Image.open(os.path.join(directory, filename)) as im:
                # Convert to RGB mode
                im = im.convert('RGB')
                # Get the bounding box of the non-transparent pixels
                bbox = im.getbbox()
                # Crop the image to the bounding box
                im = im.crop(bbox)
                # Resize the image to the target size
                im = im.resize(size, Image.Resampling.BICUBIC)
                # Save the image with the same filename
                im.save(os.path.join(directory, filename))

def main(argv):
    """! Main program entry."""
    if (len(argv)-1) != 3:
        if (len(argv) == 2 and argv[1] in ('version', '-v', '--version')):
            print(f"png_resize v{SCRIPT_VERSION}")
            sys.exit(0)
        print(f"Wrong number of arguments. Expected 3, got {len(argv)-1}")
        print(f"--> {argv[1:]}\n")
        usage()
    else:
        direc = argv[1]
        sprite_w = int(argv[2])
        sprite_h = int(argv[3])
        resize_sprites(direc,sprite_w, sprite_h)


if __name__ == "__main__":
    main(sys.argv)
