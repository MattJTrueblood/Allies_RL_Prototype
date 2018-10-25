import tcod
import constants
import core
from view import renderer
from view.frame import Frame
from view.panel import Panel
from controllers.start_menu_controller import StartMenuController

def main():
    #Events used for inputs
    key_event = tcod.Key()
    mouse_event = tcod.Mouse()

    #set up start menu
    start_frame = Frame("start frame")
    start_panel = Panel(0, 0, constants.CONSOLE_WIDTH, constants.CONSOLE_HEIGHT)
    start_panel.set_controller(StartMenuController())
    start_frame.add_panel(start_panel)
    core.add_frame(start_frame)
    core.set_current_frame("start frame")

    while not tcod.console_is_window_closed():
        #Get inputs
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key_event, mouse_event)

        #Handle any console-level changes (including quit)
        if key_event.vk == tcod.KEY_ESCAPE:
            return True;
        else:
            core.current_frame.receive_events(key_event, mouse_event)

        #Render everything
        renderer.render()

if __name__ == '__main__':
    main()
