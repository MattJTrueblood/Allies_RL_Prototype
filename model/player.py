
class Player:

    MOVE_SWITCH = {
        1: (-1, 1),
        2: (0, 1),
        3: (1, 1,),
        4: (-1, 0),
        5: (0, 0),
        6: (1, 0),
        7: (-1, -1),
        8: (0, -1),
        9: (1, -1),
    }

    def __init__(self):
        self.x = 2
        self.y = 2

    def move(self, dir_numpad):
        #convert direction (numpad keys for now) into (x, y)
        dir_xy = MOVE_SWITCH.get(dir, (0, 0))
        self.x += dir_xy[0]
        self.y += dir_xy[1]
