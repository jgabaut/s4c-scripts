#!/usr/bin/python3
"""! @brief Program that handle s4c scripts as subcommands. WIP."""

##
# @file s4c_cli.py
#
# @brief Program that handle s4c scripts as subcommands. WIP.
#
# @section description_s4c_cli Description
# The png parsing scripts use Pillow, and the mapping is done against a preset color list.
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
# @section notes_s4c_cli Notes
# - Color map should have the same order as the palette used to index the sprites.
#
# @section todo_s4c_cli TODO
# - Check if the encoded value is exceeding latin literals.
#
# @section author_s4c_cli Author(s)
# - Created by jgabaut on 02/01/2024.
# - Modified by jgabaut on 17/01/2024.

import sys
import os
from .core.cut_sheet import main as cut_sheet_main
from .core.palette import main as palette_main
from .core.sprites import main as sprites_main
from .core.sheet_converter import main as sheet_converter_main
from .core.png_resize import main as png_resize_main

S4C_CLI_VERSION = "0.1.2"

EXPECTED_S4C_ANIMATE_V = "0.4.2"

subcoms = ["cut_sheet", "palette", "sprites", "sheet_converter", "png_resize", "help", "version"]
f_prog_str = f"{os.path.basename(__file__)}"
f_usage_str = f"\nUsage:\tpython {f_prog_str} <subcommand>"
f_string_s4c_cli_v = f"s4c-cli v{S4C_CLI_VERSION}"
f_string_s4c_anim = f"s4c-animate v{EXPECTED_S4C_ANIMATE_V}"
f_string_s4c_cmpt = f"Compatible with {f_string_s4c_anim}"

def print_subcommands():
    """! Prints available subcommands."""
    print("Subcommands:\n")
    print("\t{}".format('\n\t'.join(subcoms)))

def usage():
    """! Prints correct invocation."""
    print("Wrong arguments.")
    print(f_usage_str)
    print_subcommands()

def run_subcommand(query,args):
    """! Tries running the query string as a subcommand, with the passed args."""
    if query == "cut_sheet":
        cut_sheet_main(args)
    elif query == "palette":
        palette_main(args)
    elif query == "sprites":
        sprites_main(args)
    elif query == "sheet_converter":
        sheet_converter_main(args)
    elif query == "png_resize":
        png_resize_main(args)
    else:
        print("Unreachable!")
        usage()
        sys.exit(1)

def main(argv=sys.argv):
    """! Main program entry. Run s4c scripts as subcommands."""
    if len(argv) < 2:
        usage()
        sys.exit(1)
    else:
        subcommand = argv[1]
        sub_args = []
        if subcommand.lower() in ('version', '-v', '--version'):
            print(f_string_s4c_cli_v)
            print(f_string_s4c_cmpt)
            sys.exit(0)
        elif subcommand.lower() in ('help', '-h', '--help'):
            print_subcommands()
            sys.exit(0)
        elif subcommand.lower() in subcoms:
            #Won't log subcommand pick, dirtying stdout
            #print("Running subcommand: \"{}\"".format(subcommand))
            sub_args.append(subcommand)
            for arg in argv[2:]:
                sub_args.append(arg)
            query = subcommand.lower()
            run_subcommand(query,sub_args)
        else:
            print("Unknown subcommand: ", subcommand)
            usage()
            sys.exit(1)
        # End of program
        sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
