from model.mapgen.base_floor_generator import BaseFloorGenerator
from model.dungeon_tile import DungeonTile
from view.canvas_tile import CanvasTile
from model.floor import Floor
from model.entity import Entity
from model.components.stair_component import StairComponent
from model.components.visible_component import VisibleComponent
import tcod
import random
import math

# Basic floor generator will generate rooms, corridors, doors, stairs, and monsters.

class BasicFloorGenerator(BaseFloorGenerator):

    MIN_NUM_ROOMS = 3
    MAX_NUM_ROOMS = 3

    MIN_ROOM_SIZE_RATIO = 0.1
    MAX_ROOM_SIZE_RATIO = 0.4

    MAX_GAP_BETWEEN_ROOMS = 3

    MIN_WIDTH_TO_HEIGHT_ROOM_RATIO = 0.50

    MIN_EXTRA_CORRIDORS = 1
    MAX_EXTRA_CORRIDORS = 1

    def generate_floor(self, width, height):
        self.width = width
        self.height = height
        #all walls at start
        tiles = [[DungeonTile(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '#'), True) for i in range(height)] for j in range(width)]
        #create rooms
        self.rooms = self.generate_room_locations()
        #create corridors
        corridors = self.generate_corridors()

        #Fill in corridors
        for corridor in corridors:
            for coord in corridor:
                tiles[coord[0]][coord[1]].canvas_tile.character = " "
                tiles[coord[0]][coord[1]].canvas_tile.bgcolor = tcod.Color(0, 0, 0)
                tiles[coord[0]][coord[1]].is_obstacle = False
        #Fill in rooms
        for room_num, room in enumerate(self.rooms):
            for i in range(room["x"], room["x"] + room["w"]):
                for j in range(room["y"], room["y"] + room["h"]):
                    tiles[i][j].canvas_tile.character = str(room_num)[0]
                    tiles[i][j].canvas_tile.bgcolor = tcod.Color(0, 0, 0)
                    tiles[i][j].canvas_tile.fgcolor = tcod.Color(70, 70, 70)
                    tiles[i][j].is_obstacle = False

        #return object
        floor = Floor(width, height, tiles)

        #Stairs
        up_stair_x = random.randint(self.rooms[0]["x"], self.rooms[0]["x"] + self.rooms[0]["w"] - 1)
        up_stair_y = random.randint(self.rooms[0]["y"], self.rooms[0]["y"] + self.rooms[0]["h"] - 1)
        while True:
            down_stair_x = random.randint(self.rooms[-1]["x"], self.rooms[-1]["x"] + self.rooms[-1]["w"] - 1)
            down_stair_y = random.randint(self.rooms[-1]["y"], self.rooms[-1]["y"] + self.rooms[-1]["h"] - 1)
            if down_stair_x != up_stair_x or down_stair_y != up_stair_y:
                break
        up_stair = Entity("up_stair", up_stair_x, up_stair_y)
        down_stair = Entity("down_stair", down_stair_x, down_stair_y)
        up_stair.add_component(StairComponent(up_stair, True))
        up_stair.add_component(VisibleComponent(up_stair, CanvasTile(None, tcod.Color(0, 0, 255), '<')))
        down_stair.add_component(StairComponent(up_stair, False))
        down_stair.add_component(VisibleComponent(up_stair, CanvasTile(None, tcod.Color(0, 0, 255), '>')))
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
        while guess_counter < 1000 and len(rooms) < ideal_num_rooms:
            guess_room_width = random.randint(min_room_width, max_room_width)
            guess_room_height = random.randint(min_room_height, max_room_height)
            room_guess = self.generate_potential_room_location(guess_room_width, guess_room_height)
            if self.is_room_location_valid(room_guess, rooms) and self.is_room_in_ratio_bounds(room_guess):
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

    def is_room_in_ratio_bounds(self, room):
        return min(room["w"], room["h"]) / max(room["w"], room["h"]) >= BasicFloorGenerator.MIN_WIDTH_TO_HEIGHT_ROOM_RATIO

    def generate_corridors(self):
        connection_tree = []
        reached_nodes = [self.rooms[0]]
        unreached_nodes = [room for room in self.rooms if room != self.rooms[0]]

        #generate minimum spanning tree between rooms
        while(len(unreached_nodes) > 0):
            shortest_connection = (-1, -1)
            shortest_distance = float("inf")
            for reached_node in reached_nodes:
                for unreached_node in unreached_nodes:
                    dist = self.get_distance_between_room_centers(reached_node, unreached_node)
                    if(dist < shortest_distance):
                        shortest_distance = dist
                        shortest_connection = (reached_node, unreached_node)
            unreached_nodes.remove(shortest_connection[1])
            reached_nodes.append(shortest_connection[1])
            connection_tree.append(shortest_connection)

        #add a few extra connections
        extra_connections = random.randint(BasicFloorGenerator.MIN_EXTRA_CORRIDORS, BasicFloorGenerator.MAX_EXTRA_CORRIDORS)
        print(extra_connections)
        for extra in range(extra_connections):
            print("making a random connection")
            random.shuffle(reached_nodes)
            extra_connection = self.get_random_nonexistant_connection(reached_nodes, connection_tree)
            if not extra_connection:
                print("no connections possible")
                break
            print("adding connection: " + str(extra_connection))
            connection_tree.append(extra_connection)

        corridors = []
        for connection in connection_tree:
            corridors.append(self.generate_corridor(connection[0], connection[1]))
        return corridors

    def get_distance_between_room_centers(self, room1, room2):
        room1_cx = self.get_center(room1["x"], room1["w"])
        room2_cx = self.get_center(room2["x"], room2["w"])
        room1_cy = self.get_center(room1["y"], room1["h"])
        room2_cy = self.get_center(room2["y"], room2["h"])
        return self.get_distance_between_tiles((room1_cx, room1_cy), (room2_cx, room2_cy))

    def get_distance_between_tiles(self, tile1, tile2):
        return math.sqrt(((tile2[0] - tile1[0])**2) + (tile2[1] - tile1[1])**2)

    def generate_corridor(self, source, destination):
        start_pos = (self.get_center(source["x"], source["w"]), self.get_center(source["y"], source["h"]))
        end_pos = (self.get_center(destination["x"], destination["w"]), self.get_center(destination["y"], destination["h"]))
        basic_path = self.generate_L_path(start_pos, end_pos)
        return self.bend_path_around_obstacles(basic_path)

    def generate_L_path(self, start_pos, end_pos):
        path = [start_pos]

        leftmost, rightmost, topmost, bottommost = -1, -1, -1, -1
        if(start_pos[0] <= end_pos[0]):
            leftmost, rightmost = start_pos[0], end_pos[0]
        else:
            leftmost, rightmost = end_pos[0], start_pos[0]
        if(start_pos[1] <= end_pos[1]):
            topmost, bottommost = start_pos[1], end_pos[1]
        else:
            topmost, bottommost = end_pos[1], start_pos[1]

        for x in range(leftmost, rightmost + 1):
            path.append((x, start_pos[1]))
        for y in range(topmost, bottommost + 1):
            path.append((end_pos[0], y))

        return path

    def get_random_nonexistant_connection(self, nodes, connection_tree):
        for node_1 in nodes:
            for node_2 in nodes:
                if not ((node_1, node_2) in connection_tree or (node_2, node_1) in connection_tree) and not node_1 == node_2:
                    return (node_1, node_2)
        print("no space for extra corridors")
        return None

    def bend_path_around_obstacles(self, path):
        for tile in list(path):
            if self.tile_inside_room(tile):
                path.remove(tile)
            else:
                break

        for tile in list(reversed(path)):
            if self.tile_inside_room(tile):
                path.remove(tile)
            else:
                break

        if(len(path) < 3):
            return path

        #find all invalid contiguous sections of the path.  Use pathfind algorithm
        #to find a valid path between the valid portions and replace the invalid section with that
        invalid_sublist = []
        in_invalid_segment = False
        last_valid_tile_index = 0
        for i, tile in enumerate(path[1:-1]):
            current_tile_is_valid = self.is_valid_corridor_tile(tile)
            if in_invalid_segment:
                if current_tile_is_valid:
                    invalid_sublist.append(tile)
                else:
                    in_invalid_segment = False
                    print("replacing " + str(path[last_valid_tile_index]) + " to " + str(tile))
                    valid_replacement_path = self.find_valid_corridor_path(path[last_valid_tile_index], tile)
                    print("replacement: " + str(valid_replacement_path))
                    path[last_valid_tile_index + 1 : i] = valid_replacement_path
            else:
                if not current_tile_is_valid:
                    in_invalid_segment = True
                    invalid_sublist.append(tile)
                    last_valid_tile = i - 1

        return path

    def find_valid_corridor_path(self, start_tile, end_tile):
        closed_set = []
        open_set = [start_tile]
        came_from = {}
        g_score = {}
        g_score[start_tile] = 0
        f_score = {}
        f_score[start_tile] = self.get_distance_between_tiles(start_tile, end_tile)

        while len(open_set) > 0:
            current = self.get_lowest_fscore_tile(open_set, f_score)
            if(current == end_tile):
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)
            closed_set.append(current)

            for neighbor in self.get_neighbor_tiles(current):
                if(neighbor in closed_set):
                    continue

                tentative_g_score = g_score[current] + 1

                if not (neighbor in open_set):
                    open_set.append(neighbor)
                elif tentative_g_score >= g_score[neighbor]:
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self.get_distance_between_tiles(neighbor, end_tile)
        return []


    def get_lowest_fscore_tile(self, open_set, f_score):
        lowest_fscore_tile = open_set[0]
        for tile in open_set:
            if f_score.get(tile, float("inf")) < f_score.get(tile, float("inf")):
                lowest_fscore_tile = tile
        return lowest_fscore_tile

    def reconstruct_path(self, came_from, current_tile):
        path = [current_tile]
        while(came_from.get(path[-1], False)):
            path.append(came_from[path[-1]])
        return path

    def get_neighbor_tiles(self, current_tile):
        neighbors = []
        neighbors.append((current_tile[0] + 1, current_tile[1]))
        neighbors.append((current_tile[0] - 1, current_tile[1]))
        neighbors.append((current_tile[0], current_tile[1] + 1))
        neighbors.append((current_tile[0], current_tile[1] - 1))
        return [neighbor for neighbor in neighbors if self.is_valid_corridor_tile(neighbor)]

    def is_valid_corridor_tile(self, tile):
        if tile[0] > 0 and tile[0] < self.width - 1 and tile[1] > 0 and tile[1] < self.height:
            if not self.tile_inside_room(tile):
                adjacent_room = self.get_id_of_room_adjacent_to_tile(tile)
                return adjacent_room == None
        return False

    def tile_inside_room(self, tile):
        for room in self.rooms:
            if tile[0] >= room["x"] and tile[1] >= room["y"] and tile[0] < room["x"] + room["w"] and tile[1] < room["y"] + room["h"]:
                return True
        return False

    def get_id_of_room_adjacent_to_tile(self, tile):
        for room in self.rooms:
            if ((tile[0] == room["x"] - 1 and tile[1] >= room["y"] - 1 and tile[1] <= room["y"] + room["h"]) or #left adjacent or corner
                (tile[0] == room["x"] + room["w"] and tile[1] >= room["y"] - 1 and tile[1] <= room["y"] + room["h"]) or #right adjacent or corner
                (tile[1] == room["y"] - 1 and tile[0] >= room["x"] and tile[0] <= room["x"] + room["w"] - 1) or #up adjacent
                (tile[1] == room["y"] + room["h"] and tile[0] >= room["x"] and tile[0] <= room["x"] + room["w"] - 1)): #down adjacent
                return room["id"]
        return None

    def tile_on_corner_of_room(self, tile, room):
        return ((tile[0] == room["x"] - 1 and tile[1] == room["y"] - 1) or
            (tile[0] == room["x"] - 1 and tile[1] == room["y"] + room["h"]) or
            (tile[0] == room["x"] + room["w"] and tile[1] == room["y"] - 1) or
            (tile[0] == room["x"] + room["w"] and tile[1] == room["y"] + room["h"]))

    def get_distance_to_room(self, tile, room):
        return self.get_gap_between_rooms(room, {"x": tile[0], "y": tile[1], "w": 1, "h": 1, "id": -1})
