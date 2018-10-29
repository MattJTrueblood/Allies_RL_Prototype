from model.components.base_component import BaseComponent
from model.components.health_component import HealthComponent
from model.components.ally_component import AllyComponent
import model.game as game
from view.canvas_tile import CanvasTile
import tcod
import core

class PlayerComponent(BaseComponent):

    def __init__(self, parent_entity):
        super().__init__(parent_entity)
        self.attackPower = 1

    def move(self, dx, dy):
        if game.current_floor.can_move_into_tile(self.parent_entity.x + dx, self.parent_entity.y + dy):
            self.set_position(self.parent_entity.x + dx, self.parent_entity.y + dy)
            core.master_tick += 1
        else:
            for entity in game.current_floor.get_entities_in_tile(self.parent_entity.x + dx, self.parent_entity.y + dy):
                if entity.get_component(HealthComponent):
                    if entity.get_component(AllyComponent):
                        self.swap_position(AllyComponent)
                    else:
                        self.attack(entity)

    def swap_position(self, entity):
        entity.x, self.parent_entity.x = self.parent_entity.x, entity.x
        entity.y, self.parent_entity.y = self.parent_entity.y, entity.y

    def attack(self, entity):
        healthComponent = entity.get_component(HealthComponent)
        healthComponent.receiveAttack(self.attackPower)

    def interact(self):
        game.current_floor.interact(self.entity.x, self.entity.y)
        core.master_tick += 1

    def set_position(self, x, y):
        self.parent_entity.x = x
        self.parent_entity.y = y
