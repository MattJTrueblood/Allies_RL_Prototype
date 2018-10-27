from model.components.base_component import BaseComponent
import model.dungeon as dungeon

class HealthComponent(BaseComponent):

    def __init__(self, parent_entity, health):
        super().__init__(parent_entity)
        self.health = health

    def receiveAttack(self, attackPower):
        self.health -= attackPower
        if self.health <= 0:
            dungeon.current_floor.remove_entity(self.parent_entity)
