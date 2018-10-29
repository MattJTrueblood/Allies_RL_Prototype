from model.mapgen.base_floor_generator import BaseFloorGenerator
from model.dungeon_tile import DungeonTile
from view.canvas_tile import CanvasTile
from model.floor import Floor
from model.entity import Entity
from model.components.stair_component import StairComponent
from model.components.visible_component import VisibleComponent
import tcod
import random

# Basic floor generator will generate rooms, corridors, doors, stairs, and monsters.

class BasicFloorGenerator(BaseFloorGenerator):

    MIN_NUM_ROOMS = 3
    MAX_NUM_ROOMS = 9

    MIN_ROOM_SIZE_RATIO = 0.15
    MAX_ROOM_SIZE_RATIO = 0.5

    MAX_GAP_BETWEEN_ROOMS = 3

    def generate_floor(self, width, height):
        #all walls at start
        tiles = [[DungeonTile(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '#'), True) for i in range(height)] for j in range(width)]
        #create rooms
        rooms = self.generate_room_locations(width, height)
        #foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar
        for room_num, room in enumerate(rooms):
            for i in range(room["x"], room["x"] + room["w"]):
                for j in range(room["y"], room["y"] + room["h"]):
                    tiles[i][j].canvas_tile.character = chr(room_num)
                    tiles[i][j].is_obstacle = False

        floor = Floor(width, height, tiles)

        #Stairs
        up_stair_x = random.randint(rooms[0]["x"], rooms[0]["x"] + rooms[0]["w"])
        up_stair_y = random.randint(rooms[0]["y"], rooms[0]["y"] + rooms[0]["h"])
        while True:
            down_stair_x = random.randint(rooms[0]["x"], rooms[0]["x"] + rooms[0]["w"])
            down_stair_y = random.randint(rooms[0]["y"], rooms[0]["y"] + rooms[0]["h"])
            if down_stair_x != up_stair_x or down_stair_y != up_stair_y:
                break
        up_stair = Entity("up_stair", up_stair_x, up_stair_y)
        down_stair = Entity("down_stair", down_stair_x, down_stair_y)
        up_stair.add_component(StairComponent(up_stair, True))
        up_stair.add_component(VisibleComponent(up_stair, CanvasTile(None, tcod.Color(255, 0, 0), '<')))
        down_stair.add_component(StairComponent(up_stair, False))
        down_stair.add_component(VisibleComponent(up_stair, CanvasTile(None, tcod.Color(255, 0, 0), '>')))
        floor.add_entity(up_stair)
        floor.add_entity(down_stair)

        return floor

    def generate_room_locations(self, width, height):
        rooms = []
        min_room_width = int(width * BasicFloorGenerator.MIN_ROOM_SIZE_RATIO)
        max_room_width = int(width * BasicFloorGenerator.MAX_ROOM_SIZE_RATIO)
        min_room_height = int(height * BasicFloorGenerator.MIN_ROOM_SIZE_RATIO)
        max_room_height = int(height * BasicFloorGenerator.MAX_ROOM_SIZE_RATIO)

        ideal_num_rooms = random.randint(BasicFloorGenerator.MIN_NUM_ROOMS, BasicFloorGenerator.MAX_NUM_ROOMS)

        guess_counter = 0 #if you have 100 failed placement attempts, give up and use what you have.
        while guess_counter < 100 and len(rooms) < ideal_num_rooms:
            guess_room_width = random.randint(min_room_width, max_room_width)
            guess_room_height = random.randint(min_room_height, max_room_height)
            room_guess = self.generate_potential_room_location(guess_room_width, guess_room_height, width, height)
            if self.is_room_location_valid(room_guess, rooms):
                print("found valid room!")
                rooms.append(room_guess)
                guess_counter = 0
            guess_counter += 1
        return rooms

    def generate_potential_room_location(self, guess_width, guess_height, floor_width, floor_height):
        guess_room_x = random.randint(0, floor_width - guess_width)
        guess_room_y = random.randint(0, floor_height - guess_height)
        return {
            "w": guess_width,
            "h": guess_height,
            "x": guess_room_x,
            "y": guess_room_y
        }

    def is_room_location_valid(self, check_room, rooms):
        for room in rooms:
            if self.get_gap_between_rooms(room, check_room) < BasicFloorGenerator.MAX_GAP_BETWEEN_ROOMS:
                return False
        return True

    def get_gap_between_rooms(self, room1, room2):
        room1_cx = self.get_center(room1["x"], room1["w"])
        room2_cx = self.get_center(room2["x"], room2["w"])
        room1_cy = self.get_center(room1["y"], room1["h"])
        room2_cy = self.get_center(room2["y"], room2["h"])
        return max((abs(room1_cx - room2_cx) - (int(room1["w"] + room2["w"]) / 2)),
            (abs(room1_cy - room2_cy) - (int(room1["h"] + room2["h"]) / 2)))

    def get_center(self, coord, width_or_height):
        return coord + int(width_or_height / 2)
