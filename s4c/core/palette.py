#!/usr/bin/python3
"""! @brief Program that parses a palette file into a C header."""

##
# @file palette.py
#
# @brief Program that parses a palette file into a C header.
#
# @section description_sprites Description
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
# @section notes_palette Notes
#
# @section todo_palette TODO
#
# @section author_palette Author(s)
# - Created by jgabaut on 01/09/2023.
# - Modified by jgabaut on 31/01/2025.

# Imports
import sys
import os
from .utils import convert_mode_lit
from .utils import print_wrapped_s4c_inclusion

## The file format version.
FILE_VERSION = "0.2.3"
SCRIPT_VERSION = "0.1.2"
F_STRING_ARGS = "[--cfile-no-include] <mode> <palette> <s4c path>"

# Expects the palette name as first argument, output directory as second argument.

# Functions
def usage():
    """! Prints correct invocation."""
    print("Wrong arguments. Needed: mode, palette file, s4c path")
    print(f"\nUsage:\tpython {os.path.basename(__file__)} {F_STRING_ARGS}")
    print("\n  mode:  \n\tC-header\n\tC-impl")
    sys.exit(1)


def convert_palette(mode, palette_path, s4c_path, *args):
    """! Takes a mode and a palette file, plus the path to s4c dir (for includes) and prints C code.
    @param mode The mode of operation
    @param palette_path   The path to palette file
    @param s4c_path The path to sprites4curses dir (for includes)
    """
    if mode not in ('header' , 'cfile'):
        print("Unexpected mode value in convert_palette: {mode}")
        usage()
    # We start the count from one so we account for one more cell for array declaration
    target_name = os.path.splitext(
            os.path.basename(
                os.path.normpath(palette_path))
            )[0].replace("-","_")

    with open(palette_path, encoding="utf-8") as palette_fp:
        read_lines = 0
        read_colors = 0

        colors = []
        while True:

            # Get next line from file
            line = palette_fp.readline()
            read_lines += 1

            if read_lines == 1:
                continue #Ignore first line

            # if line is empty
            # end of file is reached
            if not line:
                #print("Read [{}] colors.".format(read_colors))
                break
            #print("Line [{}]: stripped \"{}\"".format(read_lines,s_line))
            tks = line.strip().split()
            h_tks = []
            if read_lines < 5:
                #print("Still parsing header")
                h_tks += tks
                #print("h_tks: \"{}\"".format(h_tks))
                #if read_lines == 2:
                    #r_palette_name = h_tks[1]
                    #print("r_palette_name: [{}]\n".format(r_palette_name))
            else:
                #print("Line [{}]: tokens \"{}\"".format(read_lines,tks))
                r_color_name_tks = tks[3].split("-")
                r_color_name = r_color_name_tks[0]
                colors.insert(read_colors,(tks[0], tks[1], tks[2], r_color_name.upper()))
                read_colors += 1


    #print("Colors: [{}]".format(colors))
    # Start file output, beginning with version number

    if mode == "header":
        print(f"#ifndef {target_name.upper()}_S4C_H_")
        print(f"#define {target_name.upper()}_S4C_H_\n")
        print_wrapped_s4c_inclusion(s4c_path)
        print(f"#define {target_name.upper()}_S4C_H_VERSION \"{FILE_VERSION}\"")
        print(f"#define {target_name.upper()}_S4C_H_TOTCOLORS {read_colors}")
        print("\n/**")
        print(f" * Declares S4C_Color array for {target_name}.")
        print(" */")
        print(f"extern S4C_Color {target_name}[{read_colors+1}];")
        print(f"\n#endif // {target_name.upper()}_S4C_H_")
    if mode == "cfile":
        if len(args) > 0 and args[0] is False:
            print(f"#include \"{target_name}.h\"\n")
        print(f"S4C_Color {target_name}[{read_colors+1}] = {{")
        for color in colors:
            print(f"    {{ {color[0]}, {color[1]}, {color[2]}, \"{color[3]}\" }},")
        print("};")


def main(argv):
    """! Main program entry."""
    if (len(argv)-1) != 3:
        if (len(argv) == 2 and argv[1] in ('version', '-v', '--version')):
            print(f"palette v{SCRIPT_VERSION}")
            print(f"FILE_VERSION v{FILE_VERSION}")
            sys.exit(0)
        if (len(argv) == 5 and argv[1] in ('--cfile-no-include')):
            if argv[2] != 'C-impl':
                print("Wrong arguments. Can't use --cfile-no-include outside C-impl mode")
                usage()
            mode = 'cfile'
            cfile_no_include = True
            palette_path = argv[3]
            s4c_path = argv[4]
            convert_palette(mode,palette_path,s4c_path, cfile_no_include)
            return
        print(f"Wrong number of arguments. Expected 3, got {len(argv)-1}.")
        print(f"--> {argv[1:]}\n")
        usage()
    else:
        mode = argv[1]
        mode = convert_mode_lit(mode)
        if mode not in ('header', 'cfile'):
            print(f"Invalid mode: {mode}")
            sys.exit(1)
        palette_path = argv[2]
        s4c_path = argv[3]
        convert_palette(mode,palette_path,s4c_path)

if __name__ == '__main__':
    main(sys.argv)
