from controllers.base_controller import BasePanelController
import tcod
import model.dungeon as dungeon
import core
from view.panel_canvas import PanelCanvas
from model.components.player_component import PlayerComponent
from model.components.visible_component import VisibleComponent
from model.components.interfaces import Interactive
from model.components.interfaces import UpdateOnTick

class GamePanelController(BasePanelController):

    def __init__(self):
        super().__init__()
        self.game_tick = core.master_tick

    def init_canvas(self, x, y, width, height):
        super().init_canvas(x, y, width, height)
        self.panel_center_x =  int(self.canvas.width / 2)
        self.panel_center_y = int(self.canvas.height / 2)
        self.redraw_canvas()

    def redraw_canvas(self):
        #Draw current floor in viewport
        for i in range(self.canvas.width):
            for j in range(self.canvas.height):
                ij_world = self.canvas_coord_to_world_coord(i, j)
                if(self.world_coord_in_bounds(ij_world[0], ij_world[1])):
                    tile_to_draw = dungeon.current_floor.get_tile(ij_world[0], ij_world[1]).canvas_tile
                    self.canvas.put_tile(i, j, tile_to_draw)
                else:
                    self.canvas.put_tile(i, j, PanelCanvas.default_canvas_tile)

        #Draw entities in viewport
        for entity in dungeon.current_floor.get_entities():
            visible_component= entity.get_component(VisibleComponent)
            if visible_component:
                entity_xy_canvas = self.world_coord_to_canvas_coord(entity.x, entity.y)
                if self.canvas_coord_in_bounds(entity_xy_canvas[0], entity_xy_canvas[1]):
                    tile_to_draw = visible_component.get_canvas_tile()
                    self.canvas.put_char(entity_xy_canvas[0], entity_xy_canvas[1],
                        self.canvas.get_tile(entity_xy_canvas[0], entity_xy_canvas[1]).bgcolor,
                        tile_to_draw.fgcolor, tile_to_draw.character)




    def canvas_coord_to_world_coord(self, x_canvas, y_canvas):
        x_world = dungeon.player.x - self.panel_center_x + x_canvas
        y_world = dungeon.player.y - self.panel_center_y + y_canvas
        return (x_world, y_world)

    def world_coord_to_canvas_coord(self, x_world, y_world):
        x_canvas = x_world + self.panel_center_x - dungeon.player.x
        y_canvas = y_world + self.panel_center_y - dungeon.player.y
        return (x_canvas, y_canvas)

    def world_coord_in_bounds(self, world_x, world_y):
        return world_x >= 0 and world_x < dungeon.current_floor.width and world_y >= 0 and world_y < dungeon.current_floor.height

    def canvas_coord_in_bounds(self, canvas_x, canvas_y):
        return canvas_x >= 0 and canvas_x < self.canvas.width and canvas_y >= 0 and canvas_y < self.canvas.height

    KEY_SWITCH = {
        tcod.KEY_UP: (0, -1),
        tcod.KEY_DOWN: (0, 1),
        tcod.KEY_RIGHT: (1, 0),
        tcod.KEY_LEFT: (-1, 0)
    }

    def handle_key_event(self, key_event):
        direction_to_move = GamePanelController.KEY_SWITCH.get(key_event.vk, None)
        if(direction_to_move):
            dungeon.player.get_component(PlayerComponent).move(direction_to_move[0], direction_to_move[1])

        if(key_event.vk == tcod.KEY_SPACE):
            interactive_entity_next_to_player = next((entity for entity in dungeon.current_floor.get_entities()
                if entity.get_component(Interactive) and entity.x == dungeon.player.x and entity.y == dungeon.player.y), None)
            if interactive_entity_next_to_player:
                interactive_entity_next_to_player.get_component(Interactive).interact(dungeon.player)



    def handle_mouse_event(self, mouse_event):
        pass #TODO

    def update(self):
        while self.game_tick < core.master_tick:
            self.do_tick()
        self.redraw_canvas()

    def do_tick(self):
        for entity in dungeon.current_floor.get_entities():
            component_to_update = entity.get_component(UpdateOnTick)
            if component_to_update:
                component_to_update.update()
        self.game_tick += 1
