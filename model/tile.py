import tcod

class Tile:

    def __init__(self, bgcolor, fgcolor, character):
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.character = character
