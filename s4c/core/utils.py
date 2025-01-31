"""! @brief Utility functions for internal usage."""

##
# @file utils.py
#
# @brief Utility functions for internal usage.
#
# @section description_sprites Description
#
# @section libraries_main Libraries/Modules
#
# @section notes_utils Notes
#
# @section todo_utils TODO
#
# @section author_utils Author(s)
# - Created by jgabaut on 19/01/2024.
# - Modified by jgabaut on 31/01/2025.

import math
from typing import NamedTuple

class SheetArgs(NamedTuple):
    """! Defines a spritesheet."""
    sprite_width: int
    sprite_height: int
    sep_size: int
    start_x: int
    start_y: int

def color_distance(c1, c2):
    """! Calculates the distance in color between two rgb tuples.
    @param c1   The first input color to measure.
    @param c2   The second input color to measure.
    @return  The color distance between the two.
    """
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    red_distance = r1 - r2
    green_distance = g1 - g2
    blue_distance = b1 - b2
    distance = math.sqrt(red_distance ** 2 + green_distance ** 2 + blue_distance ** 2)
    return distance

def convert_mode_lit(mode):
    """! Try converting the passed mode string to the internal representation."""
    if mode == "s4c-file":
        return "s4c"
    if mode == "C-header":
        return "header"
    if mode == "C-header-exp":
        return "header-exp"
    if mode == "C-impl":
        return "cfile"
    if mode == "C-impl-exp":
        return "cfile-exp"
    print("Error: wrong mode request")
    print(f"--> Found: {mode}")
    print("--> Expected: \'C-impl\' | \'C-header\' | \'s4c-file\'\n")
    return "INVALID"

def print_animation_header(target_name, file_version):
    """! Print the beginning of animation header for a target."""
    print(f"#ifndef {target_name.upper()}_S4C_H_")
    print(f"#define {target_name.upper()}_S4C_H_")
    print(f"#define {target_name.upper()}_S4C_H_VERSION \"{file_version}\"")
    print("")
    print("/**")
    print(f" * Declares animation matrix vector for {target_name}.")
    print(" */")

def print_wrapped_s4c_inclusion(s4c_path):
    """! Print the wrapped s4c.h inclusion."""
    print("#ifndef S4C_HAS_ANIMATE")
    print("#define S4C_SCRIPTS_PALETTE_ANIMATE_CLEANUP")
    print("#define S4C_HAS_ANIMATE")
    print("#endif //!S4C_HAS_ANIMATE")
    print(f"#include \"{s4c_path}/sprites4curses/src/s4c.h\"")
    print("#ifdef PALETTE_ANIMATE_CLEANUP")
    print("#undef S4C_HAS_ANIMATE")
    print("#undef S4C_SCRIPTS_PALETTE_ANIMATE_CLEANUP")
    print("#endif //PALETTE_ANIMATE_CLEANUP\n")

def print_heading(mode, target_name, file_version, num_frames, s4c_path):
    """! Print the actual header for a target."""
    if mode == "s4c":
        print(f"{file_version}")
    elif mode == "header":
        print_animation_header(target_name, file_version)
        #print("extern char {}[{}][{}][{}];".format(target_name,frames,ysize,xsize))
        print(f"extern char {target_name}[{num_frames}][MAXROWS][MAXCOLS];")
        print(f"\n#endif // {target_name.upper()}_S4C_H_")
        return True
    elif mode == "header-exp":
        print_animation_header(target_name, file_version)
        #s4c_path = args[0]
        print_wrapped_s4c_inclusion(s4c_path)
        print(f"extern S4C_Sprite {target_name}[{num_frames}];\n")
        print(f"\n#endif // {target_name.upper()}_S4C_H_")
        return True
    elif mode in ('cfile', 'cfile-exp'):
        print(f"#include \"{target_name}.h\"\n")
    return False

def get_converted_char(char_map, r, g, b):
    """"! Returns a char looking up char_map, for passed color."""
    if (r, g, b) in char_map:
        return char_map[(r, g, b)]
    # Get the closest color in the char_map
    closest_color = min(char_map,
                        key=lambda c:
                        color_distance(c, (r, g, b)))
    return char_map[closest_color]

def new_char_map(rgb_palette):
    """! Creates a new char map for the palette."""
    char_map = {}
    char_index = 0
    for color in rgb_palette:
        if color not in char_map:
            if chr(ord('1') + char_index) == '?':
                char_map[color] = '\\?'
            else:
                char_map[color] = chr(ord('1') + char_index)
            char_index += 1
    return char_map

def log_wrong_argnum(expected, args):
    """! Logs an error message for passing wrong number of arguments."""
    print(f"Wrong number of arguments. Expected {expected}, got {len(args)-1}.")
    print(f"--> {args[1:]}\n")


def intparse_args(s_spr_w, s_spr_h, s_sep_size, s_start_x, s_start_y):
    """! Parse string arguments as int."""
    sprite_w = int(s_spr_w)
    sprite_h = int(s_spr_h)
    sep_size = int(s_sep_size)
    start_x = int(s_start_x)
    start_y = int(s_start_y)
    return (sprite_w, sprite_h, sep_size, start_x, start_y)
