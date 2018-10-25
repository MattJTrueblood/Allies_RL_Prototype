import constants
import tcod

#A few things within the project should be globally accessible, and as such should even be outside of engine.py which contains the main function.
#This file should be used very sparingly.

def init_console():
    screen_width = constants.CONSOLE_WIDTH
    screen_height = constants.CONSOLE_HEIGHT
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    return tcod.console_init_root(screen_width, screen_height, 'Game main window title text?')

root_console = init_console()
