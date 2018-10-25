from controllers.base_controller import BasePanelController
import tcod
import model.dungeon as dungeon

class GamePanelController(BasePanelController):

    def __init__(self):
        super().__init__()

    def init_canvas(self, x, y, width, height):
        super().init_canvas(x, y, width, height)
        self.draw_dungeon()

    def draw_dungeon(self):
        #Draw player
        panel_center_x = int(self.canvas.width / 2)
        panel_center_y = int(self.canvas.height / 2)
        self.canvas.put_char(panel_center_x, panel_center_y, tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '@')
        #Draw dungeon relative to player
        dungeon_tiles = dungeon.current_floor.body
        for i in range(self.canvas.width):
            for j in range(self.canvas.height):
                if (dungeon.player.x - i > 0 and dungeon.player.x + i < self.canvas.width and
                    dungeon.player.y - j > 0 and dungeon.player.y + j < self.canvas.height):
                    print(str(i) + ", " + str(j))
                    self.canvas.put_char(i, j, tile_to_draw.bgcolor, tile_to_draw.fgcolor, tile_to_draw.character)


    def handle_key_event(self, key_event):
        pass #TODO

    def handle_mouse_event(self, mouse_event):
        pass #TODO
