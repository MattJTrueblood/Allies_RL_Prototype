import tcod
import constants
from render.renderer import Renderer

def main():
    #Console object for tcod
    root_console = init_console()

    #Renderer object for graphics
    renderer = Renderer(root_console)

    #Events used for inputs
    key_event = tcod.Key()
    mouse_event = tcod.Mouse()

    while not tcod.console_is_window_closed():
        #Get inputs
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key_event, mouse_event)

        #Handle any console-level changes (including quit)
        if key_event.vk == tcod.KEY_ESCAPE:
            return True;

        #Update world model
        ###TODO###

        #Render everything
        renderer.render()


def init_console():
    screen_width = constants.CONSOLE_WIDTH
    screen_height = constants.CONSOLE_HEIGHT
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    return tcod.console_init_root(screen_width, screen_height, 'Game main window title text?')

if __name__ == '__main__':
    main()
