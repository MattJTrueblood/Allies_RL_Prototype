import tcod
import constants
import core
from view import renderer
from view.frame import Frame
from view.panel import Panel
from controllers.game_panel_controller import GamePanelController
from controllers.message_panel_controller import MessagePanelController

def main():
    key_event = tcod.Key()
    mouse_event = tcod.Mouse()

    #Build start menu
    main_frame = Frame("main frame")

    game_panel = Panel(0, 0, constants.CONSOLE_WIDTH, constants.CONSOLE_HEIGHT - constants.MESSAGE_BOX_HEIGHT)
    game_panel.set_controller(GamePanelController())
    main_frame.add_panel(game_panel)

    messages_panel = Panel(0, constants.CONSOLE_HEIGHT - constants.MESSAGE_BOX_HEIGHT, constants.CONSOLE_WIDTH, constants.MESSAGE_BOX_HEIGHT)
    messages_panel.set_controller(MessagePanelController())
    main_frame.add_panel(messages_panel)

    core.add_frame(main_frame)
    core.set_current_frame("main frame")

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
