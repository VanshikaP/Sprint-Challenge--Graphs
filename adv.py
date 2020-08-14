from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# helper function to get opposite direction
def get_opposite_dir(dir):
    if dir is 'n':
        return 's'
    if dir is 's':
        return 'n'
    if dir is 'e':
        return 'w'
    if dir is 'w':
        return 'e'

# check if a room has unexplored exit
def find_unexplored_exits(room, visited):
    unexplored_exits = []
    for exit in room.get_exits():
        if visited[room.id][exit] is '?':
            unexplored_exits.append(exit)

    return unexplored_exits

# find all possible paths to unexplored
def find_paths_to_unexplored(visited, paths=None ,new_visited=None, curr_room=None):
    if curr_room is None:
        curr_room = player.current_room

    if paths is None and new_visited is None:
        paths = []
        new_visited = set()
    
    if curr_room.id in new_visited:
        return paths
    
    new_visited.add(curr_room.id)
    
    exits = curr_room.get_exits()
    for exit in exits:
        if visited[curr_room.id][exit] is '?':
            return paths
    
    new_paths = []
    for exit in exits:
        path2 = list(paths)
        path2.append(exit)
        new_room = curr_room.get_room_in_direction(exit)
        path2 = find_paths_to_unexplored(visited, path2, new_visited, new_room)
        new_items = []
        for item in path2:
            if isinstance(item,list):
                new_paths.append(item)
            else:
                new_items.append(item)
        if len(new_items) > 0:
            new_paths.append(new_items)
    
    return new_paths

# validate paths and find the shortest one
def find_shortest_path_to_unexplored(paths, visited, curr_room):
    # validate paths
    invalid = []
    for path in paths:
        # initialize a new player
        player2 = Player(curr_room)
        
        # traverse through the path
        for dir in path:
            player2.travel(dir)
        
        # find unexplored exits if any
        unexplored_exits = find_unexplored_exits(player2.current_room, visited)
        
        # if no uneexplored exit found, mark the path for removal
        if len(unexplored_exits) is 0:
            invalid.append(path)
    
    # remove invalid paths
    for path in invalid:
        paths.remove(path)
    
    # find shortest valid path
    shortest = paths[0]
    shortest_length = len(paths[0])
    for item in paths:
        if len(item) < shortest_length:
            shortest = item
    
    return shortest

# Test suite to test middleware functions
# ------

# hello = {0: {'n': 1, 's': 5, 'w': 7, 'e': '?'}, 5: {'n': 0, 's': 6}, 6: {'n': 5, 'w': 11}, 11: {'w': 10, 'e': 6}, 10: {'n': 9, 'e': 11}, 9: {'n': 8, 's': 10}, 8: {'s': 9, 'e': 7}, 7: {'w': 8, 'e': 0}, 1: {'n': 2, 's': 0, 'w': 15, 'e': 12}, 12: {'w': 1, 'e': 13}, 13: {'n': 14, 'w': 12}, 14: {'s': 13}, 2: {'s': 1}, 15: {'w': 16, 'e': 1}, 16: {'n': 17, 'e': 15}, 17: {'s': 16}}

# there = ['s', 's', 'w', 'w', 'n', 'n', 'e', 'e', 'n', 'e', 'e', 'n', 's', 'w', 'w', 'n', 's', 'w', 'w', 'n']
# # print('&&&&', player.current_room.id)
# # player = Player(world.starting_room)
# for dir in there:
#     player.travel(dir)
# # print('&&&&', player.current_room.id)
# print('Total rooms', len(room_graph), len(hello))
# print(player.current_room.id, find_paths_to_unexplored(hello))
# # all_paths = find_paths_to_unexplored(hello)
# # print(find_shortest_path_to_unexplored(all_paths))
# all_paths = find_paths_to_unexplored(hello)
# shortest = find_shortest_path_to_unexplored(all_paths, hello, player.current_room)
# print('shortest', shortest)
# # add the new path to the path and move the player
# print('******* Player current room', player.current_room.id)
# for d in shortest:
#     # path.append(d)
#     player.travel(d)
# print('&&&&&&& Player current room', player.current_room.id)
#  ------

def get_traversal_path(visited=None, path=None, count=None):
    if path is None and visited is None and count is None:
        path = []
        visited = {}
        count=0
    
    
    # add the current_room to the visited array
    if player.current_room.id not in visited:
        visited[player.current_room.id] = {}
    
    for exit in player.current_room.get_exits():
        room_towards_exit = player.current_room.get_room_in_direction(exit).id
        # for visited rooms set the relevant exits to unexplored
        if room_towards_exit in visited:
            visited[player.current_room.id][exit] = room_towards_exit
            visited[room_towards_exit][get_opposite_dir(exit)] = player.current_room.id
            count -= 1
        else:
            # for unexplored exits, add ?
            visited[player.current_room.id][exit] = '?'
            count += 1
    
    # if all rooms visited, return the path
    if len(visited) == len(room_graph):
        return path
    
    # get unexplored exits
    unexplored_exits = find_unexplored_exits(player.current_room, visited)

    # if no unexplored exit, find path to the nearest room with unexplored exit
    if len(unexplored_exits) is 0:
        # find shortest path to unexplored exit
        all_paths = find_paths_to_unexplored(visited)
        shortest = find_shortest_path_to_unexplored(all_paths, visited, player.current_room)
        
        # add the new path to the path and move the player
        for d in shortest:
            path.append(d)
            player.travel(d)
        
        # get unexplored exits
        unexplored_exits = find_unexplored_exits(player.current_room, visited)
        
        dir = random.choice(unexplored_exits)
    else:
        dir = random.choice(unexplored_exits)
        
    
    if dir:
        path.append(dir)
        player.travel(dir)
        get_traversal_path(visited, path, count)
        

    return path

traversal_path = get_traversal_path()
print('traversal path here', traversal_path)



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



# #######
# # UNCOMMENT TO WALK AROUND
# #######
# # player.current_room.print_room_description(player)
# # while True:
# #     cmds = input("-> ").lower().split(" ")
# #     if cmds[0] in ["n", "s", "e", "w"]:
# #         player.travel(cmds[0], True)
# #     elif cmds[0] == "q":
# #         break
# #     else:
# #         print("I did not understand that command.")
