from controllers.base_controller import BasePanelController
import tcod
import time
from random import shuffle

#This Controller draws a cool depth-first maze.  Probably useless but cool anyways
class MazePanelController(BasePanelController):

    def __init__(self):
        super().__init__()

    def init_canvas(self, x, y, width, height):
        super().init_canvas(x, y, width, height)
        self.draw_cool_map()

    def draw_cool_map(self):
        #draw blips
        for i in range(1, self.canvas.width, 2):
            for j in range(1, self.canvas.height, 2):
                self.canvas.put_char(i, j, tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '.')
        #draw a cool maze thingy
        self.visitxmax = len(range(1, self.canvas.width, 2))
        self.visitymax = len(range(1, self.canvas.height, 2))
        visited_array = [[{"x": x, "y": y, "visited": False} for y in range(self.visitymax)] for x in range(self.visitxmax)]
        stack = []

        stack.append(self.visit_tile(visited_array[3][2], visited_array))
        while stack:
            if not self.visit_adjacent(stack, visited_array):
                stack.pop()

    def visit_tile(self, tile, visited_array):
        self.canvas.put_char((tile["x"] * 2) + 1, (tile["y"] * 2) + 1, tcod.Color(0, 100, 0), tcod.Color(255, 255, 255), '.')
        visited_array[tile["x"]][tile["y"]]["visited"] = True
        return visited_array[tile["x"]][tile["y"]]

    def visit_adjacent(self, stack, visited_array):
        current_tile = stack[-1]
        dirs = [i for i in range(4)]
        shuffle(dirs)
        for dir in dirs:
            if dir == 0 and current_tile["x"] < self.visitxmax - 1 and not visited_array[current_tile["x"] + 1][current_tile["y"]]["visited"]:
                stack.append(self.visit_tile(visited_array[current_tile["x"] + 1][current_tile["y"]], visited_array))
                self.canvas.put_char((current_tile["x"] * 2) + 2, (current_tile["y"] * 2) + 1, tcod.Color(0, 100, 0), tcod.Color(255, 255, 255), '.')
                return True
            if dir == 1 and current_tile["x"] > 0 and not visited_array[current_tile["x"] - 1][current_tile["y"]]["visited"]:
                stack.append(self.visit_tile(visited_array[current_tile["x"] - 1][current_tile["y"]], visited_array))
                self.canvas.put_char((current_tile["x"] * 2), (current_tile["y"] * 2) + 1, tcod.Color(0, 100, 0), tcod.Color(255, 255, 255), '.')
                return True
            if dir == 2 and current_tile["y"] < self.visitymax - 1 and not visited_array[current_tile["x"]][current_tile["y"] + 1]["visited"]:
                stack.append(self.visit_tile(visited_array[current_tile["x"]][current_tile["y"] + 1], visited_array))
                self.canvas.put_char((current_tile["x"] * 2) + 1, (current_tile["y"] * 2) + 2, tcod.Color(0, 100, 0), tcod.Color(255, 255, 255), '.')
                return True
            if dir == 3 and current_tile["y"] > 0 and not visited_array[current_tile["x"]][current_tile["y"] - 1]["visited"]:
                stack.append(self.visit_tile(visited_array[current_tile["x"]][current_tile["y"] - 1], visited_array))
                self.canvas.put_char((current_tile["x"] * 2) + 1, (current_tile["y"] * 2), tcod.Color(0, 100, 0), tcod.Color(255, 255, 255), '.')
                return True
        return False

    def handle_key_event(self, key_event):
        pass #TODO

    def handle_mouse_event(self, mouse_event):
        pass #TODO
