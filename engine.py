import tcod
import constants
import core
from view import renderer
from view.frame import Frame
from view.panel import Panel
from controllers.game_panel_controller import GamePanelController

def main():
    key_event = tcod.Key()
    mouse_event = tcod.Mouse()

    #Build start menu
    start_frame = Frame("start frame")
    start_panel = Panel(0, 0, constants.CONSOLE_WIDTH, constants.CONSOLE_HEIGHT)
    start_panel.set_controller(GamePanelController())
    start_frame.add_panel(start_panel)
    core.add_frame(start_frame)
    core.set_current_frame("start frame")

    #Main Loop
    while not tcod.console_is_window_closed():
        #Get input
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key_event, mouse_event)
        if key_event.vk == tcod.KEY_ESCAPE:
            return True;
        else:
            core.current_frame.receive_events(key_event, mouse_event)

        core.current_frame.update()
        renderer.render()

if __name__ == '__main__':
    main()
