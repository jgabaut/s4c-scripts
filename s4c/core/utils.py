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
# - Modified by jgabaut on 12/02/2025.

import math
from typing import NamedTuple

class SheetArgs(NamedTuple):
    """! Defines a spritesheet."""
    sprite_width: int
    sprite_height: int
    sep_size: int
    start_x: int
    start_y: int
    sprites_num: int

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

def print_heading(mode, target_name, file_version, sizes, s4c_path):
    """! Print the actual header for a target."""
    num_frames = sizes[0]
    num_colors = sizes[1]
    frame_width = sizes[2]
    frame_height = sizes[3]
    if mode == "s4c":
        print(f"{file_version}")
    elif mode == "header":
        print_animation_header(target_name, file_version)
        #print("extern char {}[{}][{}][{}];".format(target_name,frames,ysize,xsize))

        ###
        #We'd like to print s4c header inclusion but 0.1.x CLI interface does not require
        # it for header mode
        #
        #print_wrapped_s4c_inclusion(s4c_path)
        ###

        print(f"#define {target_name.upper()}_TOT_FRAMES {num_frames}")
        #Instead of accurately using the sprite's num of frames, we use the defined macro
        # since we expect them to be the same
        #print(f"extern char {target_name}[{num_frames}][MAXROWS][MAXCOLS];")
        print(f"extern char {target_name}[{target_name.upper()}_TOT_FRAMES+1][MAXROWS][MAXCOLS];\n")
        print(f"\n#endif // {target_name.upper()}_S4C_H_")
        return True
    elif mode == "header-exp":
        print_animation_header(target_name, file_version)
        #s4c_path = args[0]
        print_wrapped_s4c_inclusion(s4c_path)
        print(f"#define {target_name.upper()}_TOT_FRAMES {num_frames}")
        print(f"#define {target_name.upper()}_TOT_COLORS {num_colors}")
        print(f"#define {target_name.upper()}_FRAME_WIDTH {frame_width}")
        print(f"#define {target_name.upper()}_FRAME_HEIGHT {frame_height}")
        #Instead of accurately using the sprite's num of frames, we use the defined macro
        # since we expect them to be the same
        #print(f"extern S4C_Sprite {target_name}[{num_frames}];\n")
        print(f"extern S4C_Sprite {target_name}[{target_name.upper()}_TOT_FRAMES+1];\n")
        print(f"extern S4C_Color {target_name}_palette[{target_name.upper()}_TOT_COLORS+1];\n")
        print(f"\n#endif // {target_name.upper()}_S4C_H_")
        return True
    elif mode in ('cfile', 'cfile-exp'):
        print(f"#include \"{target_name}.h\"\n")
    return False

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
        print(f"\t(S4C_Color){{\n\t\t.name = \"{color_name[:50]}\",")
        print(f"\t\t.red = {color[0]},\n\t\t.green = {color[1]},\n\t\t.blue = {color[2]}")
        print("\t},")

def print_impl_ending(mode, target_name, _num_frames, target_sprites):
    """! Print the actual impl ending for a target.
    Replaces dashes in target_name with underscores.
    @param mode The impl mode
    @param target_name The name for the target
    @param num_frames The number of frames
    @param target_sprites Array matrix: [conv_chars, frame_width, frame_height,
                               rgb_palette, palette_size]
    """
    target_name.replace("-","_")
    if mode == "cfile":
        #print("char {}[{}][{}][{}] = ".format(target_name,frames,ysize,xsize) + "{\n")
        #Instead of accurately using the sprite's num of frames, we use the defined macro
        # since we expect them to be the same
        #print(f"char {target_name}[{num_frames}][MAXROWS][MAXCOLS] = ", "{\n")
        print(f"char {target_name}[{target_name.upper()}_TOT_FRAMES+1][MAXROWS][MAXCOLS] = ", "{\n")
    elif mode == "cfile-exp":
        #s4c_path = args[0]
        #Using the first sprite's palette since they must be all equal
        print(f"\nS4C_Color {target_name}_palette[{target_name.upper()}_TOT_COLORS+1] = {{")
        print_palette_as_s4c_color_array(target_sprites[0][3], target_name)
        print("};\n")
        #Instead of accurately using the sprite's num of frames, we use the defined macro
        # since we expect them to be the same
        #print(f"\nS4C_Sprite {target_name}[{num_frames}] = ", "{\n")
        print(f"\nS4C_Sprite {target_name}[{target_name.upper()}_TOT_FRAMES+1] = ", "{\n")

    for idx, target in enumerate(target_sprites):
        print(f"\t//Frame {idx}")
        if mode == "cfile":
            print("\t{")
            for row in target[0]:
                print("\t\t\""+row+"\",")
        elif mode == "cfile-exp":
            print("\t(S4C_Sprite) {")
            print("\t\t.data = {")
            for row in target[0]:
                print("\t\t\t{ \""+row+"\" },")
            print("\t\t},")
            #Instead of accurately using the sprite's height, we use the defined macro
            # since we expect them to be the same
            #print(f"\t\t.frame_height = {target[2]},")
            print(f"\t\t.frame_height = {target_name.upper()}_FRAME_HEIGHT,")
            #Instead of accurately using the sprite's width, we use the defined macro
            # since we expect them to be the same
            #print(f"\t\t.frame_width = {target[1]},")
            print(f"\t\t.frame_width = {target_name.upper()}_FRAME_WIDTH,")
            print(f"\t\t.palette = &({target_name}_palette[0]),")

            #Instead of accurately using the sprite's palette size, we use the defined macro
            # since we expect them to be the same
            #print(f"\t\t.palette_size = {target[4]},")
            print(f"\t\t.palette_size = {target_name.upper()}_TOT_COLORS,")
        print("\t},"+ "\n")
    print("};")

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

def intparse_arg(arg):
    """! Parse string arg as int."""
    int_arg = int(arg)
    return int_arg

def validate_sprite(palette, width, height, target_palette, target_size):
    """! Ensure a sprite has the same palette and size as the target values."""
    target_width = target_size[0]
    target_height = target_size[1]
    if palette != target_palette: #Must have same palette as first sprite
        print(f"\texpected: {target_palette}")
        print(f"\tfound: {palette}\n")
        print("All frames must use the same palette.\n")
        return False
    if width != target_width: #Must have same width as first sprite
        print(f"\texpected: {target_width}")
        print(f"\tfound: {width}\n")
        print("All frames must have the same width.\n")
        return False
    if height != target_height: #Must have same height as first sprite
        print(f"\texpected: {target_height}")
        print(f"\tfound: {height}\n")
        print("All frames must have the same height.\n")
        return False
    return True
