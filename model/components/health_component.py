from model.components.base_component import BaseComponent
import model.game as game

class HealthComponent(BaseComponent):

    def __init__(self, parent_entity, health):
        super().__init__(parent_entity)
        self.health = health

    def receiveAttack(self, attackPower):
        self.health -= attackPower
        if self.health <= 0:
            game.add_message(self.parent_entity.name + " was destroyed!")
            game.current_floor.remove_entity(self.parent_entity)
