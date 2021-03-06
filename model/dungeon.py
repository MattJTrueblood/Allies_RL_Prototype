from model.floor import Floor
from model.blank_floor_generator import BlankFloorGenerator
from model.components.player_component import PlayerComponent
from model.components.stair_component import StairComponent
from model.components.visible_component import VisibleComponent
from model.entity import Entity
from view.canvas_tile import CanvasTile
import tcod
import random

NUM_FLOORS = 10

floors = []
generator = BlankFloorGenerator()
for i in range(NUM_FLOORS):
    newfloor = generator.generate_floor(random.randint(15, 25), random.randint(15, 25))
    floors.append(newfloor)

for i in range(NUM_FLOORS):
    if i > 0:
        floors[i].get_entity("up_stair").get_component(StairComponent).set_destination_floor(floors[i-1])
    if i < NUM_FLOORS - 1:
        floors[i].get_entity("down_stair").get_component(StairComponent).set_destination_floor(floors[i+1])

current_floor = floors[0]
player = Entity("player", current_floor.get_entity("up_stair").x, current_floor.get_entity("up_stair").y, True)
player.add_component(PlayerComponent(player))
player.add_component(VisibleComponent(player, CanvasTile(None, tcod.Color(0, 255, 0), '@')))
current_floor.add_entity(player)

def go_up_to_floor(new_floor):
    change_floor(new_floor)
    put_player_on_downstair()

def go_down_to_floor(new_floor):
    change_floor(new_floor)
    put_player_on_upstair()

def change_floor(new_floor):
    global current_floor
    current_floor.remove_entity(player)
    new_floor.add_entity(player)
    current_floor = new_floor

def put_player_on_upstair():
    current_floor_up_stair = current_floor.get_entity("up_stair")
    player.get_component(PlayerComponent).set_position(current_floor_up_stair.x, current_floor_up_stair.y)

def put_player_on_downstair():
    current_floor_down_stair = current_floor.get_entity("down_stair")
    player.get_component(PlayerComponent).set_position(current_floor_down_stair.x, current_floor_down_stair.y)
