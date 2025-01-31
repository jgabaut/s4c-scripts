#!/usr/bin/python3
"""! @brief Parses pngs from a directory, to encode each color to a char per pixel."""

##
# @file sprites.py
#
# @brief Parses pngs from a directory, to encode each color to a char per pixel.
#
# @section description_sprites Description
# The png parsing uses Pillow, and the mapping is done against a preset color list.
# The list is described in palette.gpl to aid in exporting images with the correct color indexing.
#
# @section libraries_main Libraries/Modules
# - Pillow (https://pillow.readthedocs.io/en/stable/)
#   - Access to image manipulation functions.
# - sys standard library (https://docs.python.org/3/library/sys.html)
#   - Access to command line arguments.
# - glob standard library (https://docs.python.org/3/library/glob.html)
#   - Access to pattern expansion.
# - re standard library (https://docs.python.org/3/library/re.html)
#   - Access to regular expressions.
# - os standard library (https://docs.python.org/3/library/os.html)
#   - Access to program name.
# - math standard library (https://docs.python.org/3/library/math.html)
#   - Access to sqrt.
#
# @section notes_sprites Notes
# - Color map should have the same order as the palette used to index the sprites.
#
# @section todo_sprites TODO
# - Check if the encoded value is exceeding latin literals.
#
# @section author_sprites Author(s)
# - Created by jgabaut on 24/02/2023.
# - Modified by jgabaut on 19/01/2024.

# Imports
import sys
import glob
import re
import os
from PIL import Image
from .utils import convert_mode_lit
from .utils import print_heading
from .utils import get_converted_char
from .utils import new_char_map
from .utils import log_wrong_argnum

## The file format version.
FILE_VERSION = "0.2.3"
SCRIPT_VERSION = "0.1.1"
EXPECTED_ARGS = 2

# Expects the sprite directory name as first argument.
# File names format inside the directory should be "imageNUM.png".

# Functions
def usage():
    """! Prints correct invocation."""
    print("Wrong arguments. Needed: mode, sprites directory")
    print(f"\nUsage:\tpython {os.path.basename(__file__)}\
 [--s4c_path <s4c_path>]\
 <mode> <sprites_directory>")
    print("\n  mode:  \n\ts4c-file\n\tC-header\n\tC-impl")
    sys.exit(1)

def convert_sprite(file,chars):
    """! Takes a image and converts each pixel to a char for its color (closest match to char_map).

    @param file   The image file to convert.

    @return  A tuple of : char matrix, width, height, rbg palette, palette size.
    """
    img = Image.open(file)

    # Convert the image to an RGB mode image with 256 colors
    img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)

    # Get the color palette
    palette = img.getpalette()

    # Map the color indices to their RGB values in the palette
    rgb_palette = [(palette[i], palette[i+1], palette[i+2]) for i in range(0, len(palette), 3)]

    palette_size = len(rgb_palette)

    # Create the char_map dictionary based on the color values
    char_map = new_char_map(rgb_palette)

    # Convert each pixel to its corresponding character representation
    r, g, b = 0, 0, 0
    for y in range(img.size[1]): #Height
        line = ""
        for x in range(img.size[0]): #Width
            color_index = img.getpixel((x, y))
            r, g, b = rgb_palette[color_index]
            char = get_converted_char(char_map, r, g, b)
            line += char

        chars.append(line)

    return (chars, img.size[0], img.size[1], rgb_palette, palette_size)

def print_palette_as_s4c_color_array(rgb_palette, palette_name):
    """! Takes an rgb palette (r,g,b), and a name for the palette.
    Replaces dashes in palette_name with underscores.
    Outputs the palette to stdout, with the needed brackets for a valid C array decl.
    @param rgb_palette   The rgb palette to print
    @param palette_name The name for the palette
    """
    palette_name.replace("-","_")

    for color_idx, color in enumerate(rgb_palette):
        color_name = f"{color_idx}_COLOR_{palette_name}"
        print(f"\t\t\t(S4C_Color){{ .name = \"{color_name[:50]}\",\
                .r = {color[0]}, .g = {color[1]}, .b = {color[2]} }},")

def print_converted_sprites(mode, direc, *args):
    """! Takes a mode (s4c, header, cfile) and a dir with images, calls convert_sprite on each one.
    Outputs the converted sprites to stdout, with the needed brackets for a valid C array decl.
    According to the mode, the file generated is:
      the C header,
      the C file,
      or the version-tagged s4c-file.
    @param direc   The directory of image files to convert and print.
    """
    if mode not in ('s4c', 'header', 'cfile', 'header-exp', 'cfile-exp') :
        print(f"Unexpected mode value in print_converted_sprites: {mode}")
        usage()
    if mode in ('header-exp', 'cfile-exp') and len(args) < 1:
        print(f"Missing s4c_path in print_converted_sprits: {mode}")
        usage()
    # We start the count from one so we account for one more cell for array declaration
    frames = 1
    target_name = os.path.basename(os.path.normpath(direc)).replace("-","_")

    for file in sorted(glob.glob(f"{direc}/*.png"),
                       key=lambda f:
                       int(re.search(r'\d+', f).group())):
        #if frames == 1 :
            #ref_img = Image.open(file) #Open reference file to get output dimension. WIP
            #xsize = ref_img.size[0]+1
            #ysize = ref_img.size[1]+1
        frames += 1

    # Start file output, beginning with version number

    if print_heading(mode, target_name, FILE_VERSION, frames, args[0]):
        return

    if mode == "cfile":
        #print("char {}[{}][{}][{}] = ".format(target_name,frames,ysize,xsize) + "{\n")
        print(f"char {target_name}[{frames}][MAXROWS][MAXCOLS] = ", "{\n")
    elif mode == "cfile-exp":
        #s4c_path = args[0]
        print(f"\nS4C_Sprite {target_name}[{frames}] = ", "{\n")

    for idx, file in enumerate(sorted(glob.glob(f"{direc}/*.png"),
                      key=lambda f:
                      int(re.search(r'\d+', f).group()))):
        # convert a sprite and print the result
        chars = []
        (_conv_chars, frame_width, frame_height, rbg_palette,
         palette_size) = convert_sprite(file,chars)
        print(f"\t//Frame {idx}")
        if mode == "cfile":
            print("\t{")
            for row in chars:
                print("\t\t\""+row+"\",")
        elif mode == "cfile-exp":
            print("\t(S4C_Sprite) {")
            print("\t\t.data = {")
            for row in chars:
                print("\t\t\t{ \""+row+"\" },")
            print("\t\t},")
            print(f"\t\t.frame_height = {frame_height},")
            print(f"\t\t.frame_width = {frame_width},")
            print("\t\t.palette = {")
            print_palette_as_s4c_color_array(rbg_palette, target_name)
            print("\t\t}")
            print(f"\t\t.palette_size = {palette_size},")
        print("\t},"+ "\n")
        idx += 1
    print("};")
    return


def main(argv):
    """! Main program entry."""
    if (len(argv) -1) != EXPECTED_ARGS:
        if (len(argv) == 2 and argv[1] in ('version', '-v', '--version')):
            print(f"sprites v{SCRIPT_VERSION}")
            print(f"FILE_VERSION v{FILE_VERSION}")
            sys.exit(0)
        elif len(argv) == 5:
            s4c_path = argv[2]
            mode = argv[3]
            mode = convert_mode_lit(mode)
            directory = argv[4]
            print_converted_sprites(mode,directory,s4c_path)
            sys.exit(0)
        log_wrong_argnum(EXPECTED_ARGS,argv)
        usage()
    else:
        mode = argv[1]
        mode = convert_mode_lit(mode)
        directory = argv[2]
        print_converted_sprites(mode,directory)

if __name__ == '__main__':
    main(sys.argv)
