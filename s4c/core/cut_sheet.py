#!/usr/bin/python3
"""! @brief Program to cut passed png spritesheet, and save the sprites to a passed directory."""

##
# @file cut_sheet.py
#
# @brief Program that cut a passed png spritesheet, and saves the sprites to a passed directory.
#
# @section description_cut_spritesheet Description
# The png parsing uses Pillow, and the mapping is done against a preset color list.
# The list is described in palette.gpl to aid in exporting images with the correct color indexing.
#
# Program expects the spritesheet filename as first argument, then
#   the output directory,
#   the sprite width,
#   the sprite height,
#   separator size (thickness),
#   X coord of left corner of the first sprite (0 if sheet has no edge separator),
#   Y coord of left corner of the first sprite (0 if sheet has no edge separator).
#
# @section libraries_main Libraries/Moodules
# - Pillow (https://pillow.readthedocs.io/en/stable/)
#   - Access to image manipulation functions.
# - sys standard library (https://docs.python.org/3/library/sys.html)
#   - Access to command line arguments.
# - os standard library (https://docs.python.org/3/library/os.html)
#   - Access to program name.
# - math standard library (https://docs.python.org/3/library/math.html)
#   - Access to sqrt.
#
# @section notes_cut_spritesheet Notes
# - Color map should have the same order as the palette used to index the sprites.
#
# @section todo_cut_spritesheet TODO
# - Check if the encoded value is exceeding latin literals.
#
# @section author_cut_spritesheet Author(s)
# - Created by jgabaut on 17/04/2023.
# - Modified by jgabaut on 19/01/2024.

# Imports
import sys
import os
from PIL import Image
from .utils import log_wrong_argnum
from .utils import intparse_args
from .utils import SheetArgs

SCRIPT_VERSION="0.1.0"

F_ARG_OUTD = "<output_directory>"
F_ARG_SW = "<sprite_width>"
F_ARG_SH = "<sprite_height>"
F_STRING_ARGS = f"<sheet_file> {F_ARG_OUTD} {F_ARG_SW} {F_ARG_SH} <sep_size> <start_x> <start_y>"
EXPECTED_ARGS = 7

# Functions
def usage():
    """! Prints correct invocation."""
    print("Wrong arguments.")
    print(f"\nUsage:\tpython {os.path.basename(__file__)} {F_STRING_ARGS}")


def cut_spritesheet(filename, output_dir, s: SheetArgs):
    """! Converts a spritesheet to a set of individual sprite images.
    @param filename   The input spritesheet file.
    @param output_dir  The directory where output images will be saved.
    """
    img = Image.open(filename)
    sprites_per_row = (img.size[0] - s.start_x + s.sep_size) // (s.sprite_width + s.sep_size)
    sprites_per_column = (img.size[1] - s.start_y + s.sep_size) // (s.sprite_height + s.sep_size)

    img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)

    #sprite_index = 1
    for i in range(sprites_per_row):
        for j in range(sprites_per_column):
            spr_x = s.start_x + j * (s.sprite_width + s.sep_size)
            spr_y = s.start_y + i * (s.sprite_height + s.sep_size)
            sprite = img.crop((spr_x, spr_y, spr_x + s.sprite_width, spr_y + s.sprite_height))
            output_file = os.path.join(output_dir, f"image{i * sprites_per_column + j + 1}.png")
            sprite.save(output_file)

def main(argv):
    """! Main program entry."""
    if (len(argv)-1) != EXPECTED_ARGS:
        if (len(argv) == 2 and argv[1] in ('version', '-v', '--version')):
            print(f"cut_sheet v{SCRIPT_VERSION}")
            sys.exit(0)

        log_wrong_argnum(EXPECTED_ARGS, argv)
        usage()
    else:
        file = argv[1]
        outdir = argv[2]
        ints = intparse_args(argv[3], argv[4], argv[5], argv[6], argv[7])
        cut_spritesheet(file,outdir,SheetArgs(ints[0],ints[1],ints[2],ints[3],ints[4]))

if __name__ == "__main__":
    main(sys.argv)
