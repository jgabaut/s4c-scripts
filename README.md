# s4c-scripts

A collection of sprite helpers for using ncurses with C.

Made for use with [sprites4curses](https://github.com/jgabaut/sprites4curses).

## Table of Contents

+ [Prerequisites](#prerequisites)
+ [Installation](#install)
+ [Scripts usage](#scripts_usage)
+ [Scripts](#scripts)
  + [s4c_cli.py](#s4c_cli_py)
  + [Subscripts](#sub_scripts)
    + [sprites](#sprites_py)
    + [sheet_converter](#sheet_converter_py)
    + [cut_sheet](#cut_sheet_py)
    + [png_resize](#png_resize_py)
    + [palette](#palette_py)


## Prerequisites <a name = "prerequisites"></a>

  You need `Pillow` installed to use the CLI. Run:

  `PY_VENV_BIN_PATH=your/venv/bin/path make`

  To install dependencies.

## Installaton <a name = "install"></a>

  Run:

  `PY_VENV_BIN_PATH=your/venv/bin/path make install`

  To install the package with `pip`.

## Scripts usage <a name = "scripts_usage"></a>

  To run the cli wrapper:

  - `python -m s4c.s4c_cli <subcommand> <subcommand_args>`

  - Some commands may be more useful when their output is redirected:
    `python -m s4c.s4c_cli <subcommand> <subcommand_args> > file.txt`

  To run the subcommands directly:

  - `python -m s4c.core.<SCRIPT> <subcommand_args>`

  If you successfull installed the package with `pip`, you will get a `s4c` executable that calls the `s4c_cli.py` script.

## Scripts <a name = "scripts"></a>

### s4c_cli.py <a name = "s4c_cli_py"></a>

  This is a wrapper script that imports the local scripts and enables calling their main as a subcommand.

### Subscripts <a name = "sub_scripts"></a>

### sprites <a name = "sprites_py"></a>

  This is a python script that converts PNG's to a char representation.
  The output text should be a valid C declaration for a 3D char array.

  It expects as arguments:

  - A mode of operation: `s4c-file`, `C-impl` , `C-header`.
  - A directory with the images to convert.

### sheet_converter <a name = "sheet_converter_py"></a>

  This is a python script that converts a single PNG spritesheet to a char representation.
  The output text should be a valid C declaration for a 3D char array.

  It expects as arguments:

  - A mode of operation: `s4c-file`, `C-impl` , `C-header`.
  - The spritesheet file name
  - The sprite width
  - The sprite height
  - The thickness of the separator between sprites
  - The start coordinate (aka, the first sprite's left corner).

### cut_sheet <a name = "cut_sheet_py"></a>

  This is a python script that cuts a single PNG spritesheet to a number of sprites, and puts them in the passed directory.

  It expects as arguments:

  - The spritesheet file name
  - The output directory name
  - The sprite width
  - The sprite height
  - The thickness of the separator between sprites
  - The start coordinate (aka, the first sprite's left corner).

### png_resize <a name = "png_resize_py"></a>

  This is a python script that resizess PNG's to a desired size.

  It expects as arguments:

  - A directory with the images to resize
  - Two ints for width and height of the resulting PNGs.


### palette <a name = "palette_py"></a>

  This is a python script that generates C files from a `palette.gpl` file.

  It expects as arguments:

  - A mode of operation: `C-impl` , `C-header`.
  - The palette file
  - The relative path to the `sprites4curses` directory, so that the generated header can correctly include `animate.h`
