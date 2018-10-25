from controllers.base_controller import BasePanelController

class StartMenuController(BasePanelController):

    def __init__(self):
        super().__init__()

    def handle_key_event(self, key_event):
        print("key_event_for_start_menu!")

    def handle_mouse_event(self, mouse_event):
        print("mouse_event_for_start_menu!")
