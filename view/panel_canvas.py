import tcod
import core

class PanelCanvas:

    default_canvas_tile = {
        "bgcolor": tcod.Color(0, 100, 0),
        "fgcolor": tcod.Color(255, 255, 0),
        "char": '#'
    }

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.body = [[None for i in range(self.width)] for j in range(self.height)]

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                tile = self.body[j][i]
                if not tile:
                    tile = PanelCanvas.default_canvas_tile
                self.draw_tile(tile, i, j)

    def draw_tile(self, tile, tile_x, tile_y):
        tcod.console_put_char_ex(core.root_console, self.x + tile_x, self.y + tile_y, ord(tile["char"]), tile["fgcolor"], tile["bgcolor"])
