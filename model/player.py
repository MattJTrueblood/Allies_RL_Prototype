import model.dungeon as dungeon

class Player:
    def __init__(self):
        self.x = -1
        self.y = -1

    def move(self, dir):
        #convert direction (numpad keys for now) into (x, y)
        if not dungeon.get_current_floor().get_tile(self.x+dir[0], self.y + dir[1]).is_obstacle:
            self.x += dir[0]
            self.y += dir[1]

    def interact(self):
        dungeon.get_current_floor().get_tile(self.x, self.y).on_interact()

    def set_position(self, x, y):
        self.x = x
        self.y = y
