from controllers.base_controller import BasePanelController
import tcod
import model.dungeon as dungeon
from view.panel_canvas import PanelCanvas

class GamePanelController(BasePanelController):

    def __init__(self):
        super().__init__()

    def init_canvas(self, x, y, width, height):
        super().init_canvas(x, y, width, height)
        self.panel_center_x =  int(self.canvas.width / 2)
        self.panel_center_y = int(self.canvas.height / 2)
        self.redraw_canvas()

    def redraw_canvas(self):

        #Draw dungeon relative to player
        dungeon_tiles = dungeon.current_floor.body
        for i in range(self.canvas.width):
            for j in range(self.canvas.height):
                i_world = dungeon.player.x - self.panel_center_x + i
                j_world = dungeon.player.y - self.panel_center_y + j
                if(i_world >= 0 and i_world < dungeon.current_floor.width and j_world >= 0 and j_world < dungeon.current_floor.height):
                    tile_to_draw = dungeon.current_floor.body[j_world][i_world]
                    self.canvas.put_char(i, j, tile_to_draw.bgcolor, tile_to_draw.fgcolor, tile_to_draw.character)
                else:
                    self.canvas.put_tile(i, j, PanelCanvas.default_canvas_tile)

        #Draw player
        self.canvas.put_char(self.panel_center_x, self.panel_center_y, tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '@')

    KEY_SWITCH = {
        tcod.KEY_KP8: 8,
        tcod.KEY_KP2: 2,
        tcod.KEY_KP4: 4,
        tcod.KEY_KP6: 6
    }

    def handle_key_event(self, key_event):
        numpad_pressed_key = GamePanelController.KEY_SWITCH.get(key_event.vk, None)
        if(numpad_pressed_key):
            dungeon.player.move(numpad_pressed_key)


    def handle_mouse_event(self, mouse_event):
        pass #TODO

    def update(self):
        self.redraw_canvas()
