from model.stub_floor import StubFloor
from model.player import Player
import random

floors = []
for i in range(10):
    floors.append(StubFloor(random.randint(5,20), random.randint(5,20)))
current_floor_index = 0

player = Player()

def go_to_next_floor():
    global current_floor_index
    current_floor_index += 1
    put_player_on_upstair()
    print("down")

def go_to_prev_floor():
    global current_floor_index
    current_floor_index -= 1
    put_player_on_downstair()
    print("up")

def get_current_floor():
    return floors[current_floor_index]

def put_player_on_upstair():
    player.set_position(get_current_floor().upstair_x, get_current_floor().upstair_y)

def put_player_on_downstair():
    player.set_position(get_current_floor().downstair_x, get_current_floor().downstair_y)

put_player_on_upstair()
