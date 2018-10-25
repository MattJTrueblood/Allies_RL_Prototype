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
        print("on floor " + str(dungeon.current_floor_index))
        current_floor = dungeon.get_current_floor()
        for i in range(self.canvas.width):
            for j in range(self.canvas.height):
                i_world = dungeon.player.x - self.panel_center_x + i
                j_world = dungeon.player.y - self.panel_center_y + j
                if(i_world >= 0 and i_world < current_floor.width and j_world >= 0 and j_world < current_floor.height):
                    tile_to_draw = current_floor.get_tile(i_world, j_world).canvas_tile
                    self.canvas.put_char(i, j, tile_to_draw.bgcolor, tile_to_draw.fgcolor, tile_to_draw.character)
                else:
                    self.canvas.put_tile(i, j, PanelCanvas.default_canvas_tile)

        #Draw player
        self.canvas.put_char(self.panel_center_x, self.panel_center_y, tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '@')

    KEY_SWITCH = {
        tcod.KEY_UP: (0, -1),
        tcod.KEY_DOWN: (0, 1),
        tcod.KEY_RIGHT: (1, 0),
        tcod.KEY_LEFT: (-1, 0)
    }

    def handle_key_event(self, key_event):
        direction_to_move = GamePanelController.KEY_SWITCH.get(key_event.vk, None)
        if(direction_to_move):
            dungeon.player.move(direction_to_move)

        if(key_event.vk == tcod.KEY_SPACE):
            dungeon.player.interact()


    def handle_mouse_event(self, mouse_event):
        pass #TODO

    def update(self):
        self.redraw_canvas()
