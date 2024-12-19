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
import io
from PIL import Image
from .utils import convert_mode_lit
from .utils import print_animation_header
from .utils import get_converted_char
from .utils import new_char_map
from .utils import log_wrong_argnum
from .palette import main as palette_main

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
    print(f"\nUsage:\tpython {os.path.basename(__file__)} [--palette <palette_path> --s4c_path <s4c_path>] <mode> <sprites_directory>")
    print("\n  mode:  \n\ts4c-file\n\tC-header\n\tC-impl")
    sys.exit(1)

def convert_sprite(file,chars):
    """! Takes a image and converts each pixel to a char for its color (closest match to char_map).

    @param file   The image file to convert.

    @return  A tuple of : the converted sprite as a char matrix, the sprite width, the sprite height, the rbg palette used, the palette size.
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
    img_width = img.size[0]
    img_height = img.size[1]
    for y in range(img_height):
        line = ""
        for x in range(img_width):
            color_index = img.getpixel((x, y))
            r, g, b = rgb_palette[color_index]
            char = get_converted_char(char_map, r, g, b)
            line += char

        chars.append(line)

    return (chars, img_width, img_height, rgb_palette, palette_size)

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
    if mode in ('header-exp', 'cfile-exp') and len(args) < 2:
        if len(args) == 1:
            print(f"Missing s4c_path in print_converted_sprits: {mode}")
        else:
            print(f"Missing palette_path, s4c_path in print_converted_sprits: {mode}")
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

    if mode == "s4c" :
        print(f"{FILE_VERSION}")
    elif mode == "header":
        print_animation_header(target_name, FILE_VERSION)
        #print("extern char {}[{}][{}][{}];".format(target_name,frames,ysize,xsize))
        print(f"extern char {target_name}[{frames}][MAXROWS][MAXCOLS];")
        print(f"\n#endif // {target_name.upper()}_S4C_H_")
        return
    elif mode == "header-exp":
        print_animation_header(target_name, FILE_VERSION)
        print(f"extern S4C_Sprite {target_name}[{frames}];")
        print("\n/**")
        print(f" * Declares palette for {target_name}.")
        print(" */")
        palette_path = args[0]
        s4c_path = args[1]
        palette_main(["sprites.py", "C-header", palette_path, s4c_path])
        print(f"\n#endif // {target_name.upper()}_S4C_H_")
        return
    elif mode == "cfile" or mode == "cfile-exp":
        print(f"#include \"{target_name}.h\"\n")

    if mode == "cfile":
        #print("char {}[{}][{}][{}] = ".format(target_name,frames,ysize,xsize) + "{\n")
        print(f"char {target_name}[{frames}][MAXROWS][MAXCOLS] = ", "{\n")
    elif mode == "cfile-exp":

        palette_path = args[0]
        s4c_path = args[1]
        palette_main(["sprites.py", "--cfile-no-include", "C-impl", palette_path, s4c_path])
        print(f"\nS4C_Sprite {target_name}[{frames}] = ", "{\n")

    idx = 1
    for file in sorted(glob.glob(f"{direc}/*.png"),
                      key=lambda f:
                      int(re.search(r'\d+', f).group())):
        # convert a sprite and print the result
        chars = []
        (conv_chars, frame_width, frame_height, rbg_palette, palette_size) = convert_sprite(file,chars)
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

            palette_path = args[0]
            palette_name = os.path.splitext(
                os.path.basename(
                    os.path.normpath(palette_path))
            )[0].replace("-","_")

            print(f"\t\t.palette = &{palette_name},") #TODO: build the palette
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
        elif (len(argv) == 7 and argv[1] in ('--palette')):
            if argv[3] != "--s4c_path":
                print(f"Wrong arguments. Expecting --s4c_path, found: {argv[3]}")
                usage()
            palette_path = argv[2]
            s4c_path = argv[4]
            mode = argv[5]
            mode = convert_mode_lit(mode)
            directory = argv[6]
            print_converted_sprites(mode,directory,palette_path, s4c_path)
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
