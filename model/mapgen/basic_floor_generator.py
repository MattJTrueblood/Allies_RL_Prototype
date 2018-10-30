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

    MIN_NUM_ROOMS = 2
    MAX_NUM_ROOMS = 3

    MIN_ROOM_SIZE_RATIO = 0.15
    MAX_ROOM_SIZE_RATIO = 0.5

    MAX_GAP_BETWEEN_ROOMS = 3

    def generate_floor(self, width, height):
        self.width = width
        self.height = height
        #all walls at start
        tiles = [[DungeonTile(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '#'), True) for i in range(height)] for j in range(width)]
        #create rooms
        self.rooms = self.generate_room_locations()

        #Fill in rooms
        for room in self.rooms:
            for i in range(room["x"], room["x"] + room["w"]):
                for j in range(room["y"], room["y"] + room["h"]):
                    tiles[i][j].canvas_tile.character = '.'
                    tiles[i][j].canvas_tile.bgcolor = tcod.Color(50, 50, 50)
                    tiles[i][j].is_obstacle = False
        #create corridors
        corridors = self.generate_corridors()
        for corridor in corridors:
            for coord in corridor:
                tiles[coord[0]][coord[1]].canvas_tile.character = "*"
                tiles[coord[0]][coord[1]].canvas_tile.fgcolor = tcod.Color(255, 255, 0)

        floor = Floor(width, height, tiles)

        #Stairs
        up_stair_x = random.randint(self.rooms[0]["x"], self.rooms[0]["x"] + self.rooms[0]["w"] - 1)
        up_stair_y = random.randint(self.rooms[0]["y"], self.rooms[0]["y"] + self.rooms[0]["h"] - 1)
        while True:
            down_stair_x = random.randint(self.rooms[0]["x"], self.rooms[0]["x"] + self.rooms[0]["w"] - 1)
            down_stair_y = random.randint(self.rooms[0]["y"], self.rooms[0]["y"] + self.rooms[0]["h"] - 1)
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

    def generate_room_locations(self):
        rooms = []
        min_room_width = int(self.width * BasicFloorGenerator.MIN_ROOM_SIZE_RATIO)
        max_room_width = int(self.width * BasicFloorGenerator.MAX_ROOM_SIZE_RATIO)
        min_room_height = int(self.height * BasicFloorGenerator.MIN_ROOM_SIZE_RATIO)
        max_room_height = int(self.height * BasicFloorGenerator.MAX_ROOM_SIZE_RATIO)

        ideal_num_rooms = random.randint(BasicFloorGenerator.MIN_NUM_ROOMS, BasicFloorGenerator.MAX_NUM_ROOMS)

        guess_counter = 0 #if you have 100 failed placement attempts, give up and use what you have.
        while guess_counter < 100 and len(rooms) < ideal_num_rooms:
            guess_room_width = random.randint(min_room_width, max_room_width)
            guess_room_height = random.randint(min_room_height, max_room_height)
            room_guess = self.generate_potential_room_location(guess_room_width, guess_room_height)
            if self.is_room_location_valid(room_guess, rooms):
                room_guess["id"] = len(rooms)
                rooms.append(room_guess)
                guess_counter = 0
            guess_counter += 1
        return rooms

    def generate_potential_room_location(self, guess_width, guess_height):
        guess_room_x = random.randint(1, self.width - guess_width - 1)
        guess_room_y = random.randint(1, self.height - guess_height - 1)
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

    def generate_corridors(self):
        connections = []
        corridors = []
        #for source_room in self.rooms:
            #for destination_room in self.rooms:
        #room position is already totally random.
        directions = ["up", "down", "left", "right"]
        random.shuffle(directions)
        for direction in directions:
            corridor = self.generate_corridor(self.rooms[0], self.rooms[1], direction)
            if corridor:
                connections.append((self.rooms[0], self.rooms[1]))
                corridors.append(corridor)
                #if self.all_rooms_connected(rooms, connections):
                #return corridors
        return corridors


    def generate_corridor(self, source, destination, direction):
        start_pos = (-1, -1)
        if direction == "up":
            if source["y"] < 3:
                return None
            start_pos = (random.randint(source["x"], source["x"] + source["w"] - 1), source["y"] - 1)
        elif direction == "down":
            if source["y"] + source["h"] - 1 > self.height - 4:
                return None
            start_pos = (random.randint(source["x"], source["x"] + source["w"] - 1), source["y"] + source["h"])
        elif direction == "left":
            if source["x"] < 3:
                return None
            start_pos = (source["x"] - 1, random.randint(source["y"], source["y"] + source["h"] - 1))
        elif direction == "right":
            if source["x"] + source["w"] - 1 > self.width - 4:
                return None
            start_pos = (source["x"] + source["w"], random.randint(source["y"], source["y"] + source["h"] - 1))

        visited = [[False for i in range(self.height)] for j in range(self.width)]
        return self.pathfind_to_destination_room([start_pos], destination, visited)

    def pathfind_to_destination_room(self, path, destination_room, visited):
        if len(path) == 0:
            return None
        valid_neighbors = self.get_possible_corridor_neighbor_tiles(path[-1], destination_room, visited)
        random.shuffle(valid_neighbors)
        for neighbor in valid_neighbors:
            visited[neighbor[0]][neighbor[1]] = True
            path = self.pathfind_to_destination_room(path + [neighbor], destination_room, visited)
        if not self.get_id_of_room_adjacent_to_tile(path[-1]) == destination_room["id"]:
            path.pop()
        return path

    def get_possible_corridor_neighbor_tiles(self, head_of_path, destination_room, visited):
        all_neighbors = [
            (head_of_path[0] - 1, head_of_path[1]),
            (head_of_path[0] + 1, head_of_path[1]),
            (head_of_path[0], head_of_path[1] - 1),
            (head_of_path[0], head_of_path[1] + 1)]
        return [neighbor for neighbor in all_neighbors if self.is_valid_neighbor_corridor_tile(neighbor, destination_room, visited)]

    def is_valid_neighbor_corridor_tile(self, neighbor, destination_room, visited):
        if neighbor[0] > 0 and neighbor[0] < self.width - 1 and neighbor[1] > 0 and neighbor[1] < self.height:
            if not self.tile_inside_room(neighbor):
                adjacent_room = self.get_id_of_room_adjacent_to_tile(neighbor)
                if adjacent_room == None or adjacent_room == destination_room["id"]:
                    print(str(neighbor) + " is valid, either nonadjacent or adjacent to " + str(destination_room["id"]))
                    return not visited[neighbor[0]][neighbor[1]]
        print(str(neighbor) + " is invalid")
        return False

    def tile_inside_room(self, tile):
        for room in self.rooms:
            if tile[0] >= room["x"] and tile[1] >= room["y"] and tile[0] < room["x"] + room["w"] and tile[1] < room["y"] + room["h"]:
                return True
        return False

    def get_id_of_room_adjacent_to_tile(self, tile):
        for room in self.rooms:
            if ((tile[0] == room["x"] - 1 and tile[1] >= room["y"] and tile[1] <= room["y"] + room["h"] - 1) or #left adjacent
                (tile[0] == room["x"] + room["w"] and tile[1] >= room["y"] and tile[1] <= room["y"] + room["h"] - 1) or #right adjacent
                (tile[1] == room["y"] - 1 and tile[0] >= room["x"] and tile[0] <= room["x"] + room["w"] - 1) or #up adjacent
                (tile[1] == room["y"] + room["h"] and tile[0] >= room["x"] and tile[0] <= room["x"] + room["w"] - 1)): #down adjacent
                print(str(tile) + " is ajacent to " + str(room["id"]))
                return room["id"]
        return None
