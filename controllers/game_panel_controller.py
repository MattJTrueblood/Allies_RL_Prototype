from controllers.base_controller import BasePanelController
import tcod
import model.game as game
import core
import controllers.world_lighting_controller as world_lighting_controller
from view.panel_canvas import PanelCanvas
from model.components.player_component import PlayerComponent
from model.components.visible_component import VisibleComponent
from model.components.interfaces import GroundInteractive
from model.components.interfaces import AdjacentInteractive
from model.components.interfaces import UpdateOnTick
from model.components.door_component import DoorComponent

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
        world_lighting_controller.draw_canvas_with_lighting(self.canvas, self.panel_center_x, self.panel_center_y)

    KEY_SWITCH = {
        tcod.KEY_UP: (0, -1),
        tcod.KEY_DOWN: (0, 1),
        tcod.KEY_RIGHT: (1, 0),
        tcod.KEY_LEFT: (-1, 0)
    }

    def handle_key_event(self, key_event):
        direction_to_move = GamePanelController.KEY_SWITCH.get(key_event.vk, None)
        if(direction_to_move):
            game.player.get_component(PlayerComponent).move(direction_to_move[0], direction_to_move[1])

        if(key_event.vk == tcod.KEY_SPACE):
            for entity in game.current_floor.get_entities():
                if entity.get_component(GroundInteractive) and self.entity_in_same_tile_as_player(entity):
                    entity.get_component(GroundInteractive).interact_ground(game.player)
                    break
            else: #if no ground entity
                for entity in game.current_floor.get_entities():
                    if entity.get_component(AdjacentInteractive) and self.entity_adjacent_to_player(entity):
                        entity.get_component(AdjacentInteractive).interact_adjacent(game.player)
                        break

    def entity_in_same_tile_as_player(self, entity):
        return self.entity_manhattan_distance_from_player(entity) == 0

    def entity_adjacent_to_player(self, entity):
        return self.entity_manhattan_distance_from_player(entity) == 1

    def entity_manhattan_distance_from_player(self, entity):
        return (abs(entity.x - game.player.x) + abs(entity.y - game.player.y))

    def handle_mouse_event(self, mouse_event):
        pass #TODO

    def update(self):
        while self.game_tick < core.master_tick:
            self.do_tick()
        self.redraw_canvas()

    def do_tick(self):
        entities_to_update = [entity for entity in game.current_floor.get_entities() if entity.get_component(UpdateOnTick)]
        entities_to_update.sort(key=lambda x: x.get_component(UpdateOnTick).get_priority(), reverse = True)
        for entity in entities_to_update:
            component_to_update = entity.get_component(UpdateOnTick)
            if component_to_update:
                component_to_update.update()
        self.game_tick += 1
