import tcod
import constants
from render import renderer
import core
from render.frame import Frame
from render.panel import Panel

def main():
    #Events used for inputs
    key_event = tcod.Key()
    mouse_event = tcod.Mouse()

    #set up start menu
    start_frame = Frame("start frame")
    start_panel = Panel(0, 0, constants.CONSOLE_WIDTH, constants.CONSOLE_HEIGHT)
    start_panel.set_bg_color(tcod.Color(0, 100, 0))
    start_frame.add_panel(start_panel)
    renderer.add_frame(start_frame)
    renderer.set_current_frame("start frame")

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

if __name__ == '__main__':
    main()
