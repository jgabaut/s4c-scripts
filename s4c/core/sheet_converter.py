#!/usr/bin/python3
"""! @brief Parses pngs from a spritesheet, to encode each color to a char per pixel."""

##
# @file sheet_converter.py
#
# @brief Parses pngs from a spritesheet, to encode each color to a char per pixel.
#
# @section description_spritesheet Description
# The png parsing uses Pillow, and the mapping is done against a preset color list.
# The list is described in palette.gpl to aid in exporting images with the correct color indexing.
#
# Program expects the spritesheet filename as first argument, then
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
# @section notes_spritesheet Notes
# - Color map should have the same order as the palette used to index the sprites.
#
# @section todo_spritesheet TODO
# - Check if the encoded value is exceeding latin literals.
#
# @section author_spritesheet Author(s)
# - Created by jgabaut on 24/02/2023.
# - Modified by jgabaut on 19/01/2024.

# Imports
import sys
import os
from PIL import Image
from s4c.core.utils import convert_mode_lit
from s4c.core.utils import print_animation_header
from s4c.core.utils import get_converted_char
from s4c.core.utils import new_char_map
from s4c.core.utils import log_wrong_argnum
from s4c.core.utils import intparse_args
from s4c.core.utils import SheetArgs

## The file format version.
FILE_VERSION = "0.2.2"
SCRIPT_VERSION = "0.1.0"
F_STR_ARGS = "<mode> <sheet> <sprite_width> <sprite_heigth> <separator_size> <start_x> <start_y>"
EXPECTED_ARGS = 7

# Functions
def usage():
    """! Prints correct invocation."""
    f_string_usage = "mode,\
 filename,\
 sprite width,\
 sprite height,\
 sep size,\
 left corner of first sprite's X, Y."
    print(f"Wrong arguments. Needed: {f_string_usage}")
    print(f"\nUsage:\tpython {os.path.basename(__file__)} {F_STR_ARGS}")
    print("\n    mode:\n\t  s4c-file\n\t  C-header\n\t  C-impl")


def print_sprites(mode, sprites, target_name):
    """! Prints the wanted mode output for passed sprites array."""
    if mode == "s4c" :
        print(f"{FILE_VERSION}")
    elif mode == "header":
        print_animation_header(target_name, FILE_VERSION)
        #print(f"extern char {target_name}[{len(sprites)+1}][{sprite_h+1}][{sprite_w+1}];")
        print(f"extern char {target_name}[{len(sprites)+1}][MAXROWS][MAXCOLS];")
        print("\n#endif")
        return
    elif mode == "cfile":
        print(f"#include \"{target_name}.h\"\n")

    #print(f"char {target_name}[{len(sprites)+1}][{sprite_h+1}][{sprite_w+1}] = ", "{\n")
    print("char {target_name}[{len(sprites)+1}][MAXROWS][MAXCOLS] = ", "{\n")
    for i, sprite in enumerate(sprites):
        print(f"\t//Sprite {i+1}, index {i}")
        print("\t{")
        for row in sprite:
            print("\t\t\"" + row + "\",")
        print("\t}," + "\n")
    print("};")
    return


def parse_sprite(sprite, rgb_palette, char_map):
    """! Parse sprite using the palette and charmap, returns char array."""
    chars = []
    curr_color = (0, 0, 0)
    for y in range(sprite.size[1]):
        line = ""
        for x in range(sprite.size[0]):
            color_index = sprite.getpixel((x, y))
            curr_color = rgb_palette[color_index]
            char = get_converted_char(char_map, curr_color[0], curr_color[1], curr_color[2])
            line += char
        chars.append(line)
    return chars


def convert_spritesheet(mode, filename, s: SheetArgs):
    """! Converts a spritesheet to a 3D char array repr of pixel color.
    The prints it with the needed brackets and commas.
      Depending on mode (s4c-file, C-header, C-impl) there will be a different output.
    @param mode    The mode for output generation.
    @param filename   The input spritesheet file.
    """
    target_name = os.path.splitext(os.path.basename(filename))[0].replace("-","_")


    img = Image.open(filename)
    sprites = []

    img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)
    palette = img.getpalette()
    rgb_palette = [(palette[n], palette[n+1], palette[n+2]) for n in range(0, len(palette), 3)]
    # Create the char_map dictionary based on the color values
    char_map = new_char_map(rgb_palette)

    #for i in range(img.size[1] // (sprite_h + sep_size * (sprites_per_column - 1))):

    for k in range((img.size[0] - s.start_x + s.sep_size) // (s.sprite_width + s.sep_size)):
        for j in range((img.size[1] - s.start_y + s.sep_size) // (s.sprite_height + s.sep_size)):
            spr_x = s.start_x + j * (s.sprite_width + s.sep_size)
            #+ (sep_size if j > 0 else 0)
            spr_y = s.start_y + k * (s.sprite_height + s.sep_size)
            #+ k * (sprite_h + sep_size * (sprites_per_column - 1))
                # + (sep_size if k > 0 else 0)
            sprite = img.crop((spr_x, spr_y, spr_x + s.sprite_width , spr_y + s.sprite_height))

            chars = parse_sprite(sprite, rgb_palette, char_map)

            sprites.append(chars)

    print_sprites(mode, sprites, target_name)

def main(argv):
    """! Main program entry."""
    if (len(argv) -1) != EXPECTED_ARGS:
        if (len(argv) == 2 and argv[1] in ('version', '-v', '--version')):
            print(f"sheet_converter v{SCRIPT_VERSION}")
            print(f"FILE_VERSION v{FILE_VERSION}")
            sys.exit(0)
        log_wrong_argnum(EXPECTED_ARGS, argv)
        usage()
    else:
        mode = argv[1]
        mode = convert_mode_lit(mode)
        filename = argv[2]
        ints = intparse_args(argv[3], argv[4], argv[5], argv[6], argv[7])
        convert_spritesheet(mode,filename,SheetArgs(ints[0],ints[1],ints[2],ints[3],ints[4]))

if __name__ == "__main__":
    main(sys.argv)
