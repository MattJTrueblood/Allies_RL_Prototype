from controllers.base_controller import BasePanelController
from view.canvas_tile import CanvasTile
import model.game as game
import tcod

class MessagePanelController(BasePanelController):

    def __init__(self):
        super().__init__()

    def init_canvas(self, x, y, width, height):
        super().init_canvas(x, y, width, height)
        self.displayed_lines = height - 1 #to account for divider line
        self.redraw_canvas()

    def redraw_canvas(self):
        #Divider line at top
        for i in range(self.canvas.width):
            self.canvas.put_tile(i, 0, CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '-'))

        for j, message in enumerate(game.messages):
            if(j > self.displayed_lines):
                break
            if(j == 0):
                self.canvas.put_string(0, self.canvas.height - (j + 1), message, tcod.Color(255, 255, 255), bgcolor=tcod.Color(50, 50, 100))
            else:
                self.canvas.put_string(0, self.canvas.height - (j + 1), message, tcod.Color(255, 255, 255))

    def handle_key_event(self, key_event):
        pass

    def handle_mouse_event(self, mouse_event):
        pass

    def update(self):
        self.redraw_canvas()
