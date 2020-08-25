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

# find unexplored exits for the given room
def find_unexplored_exits(room, visited):
    unexplored_exits = []
    for exit in room.get_exits():
        if visited[room.id][exit] is '?':
            unexplored_exits.append(exit)

    return unexplored_exits

# get neighbors for the given room
def get_neighbors(room):
    neighbors = {}
    
    if room.n_to is not None:
        neighbors['n'] = room.n_to
    if room.s_to is not None:
        neighbors['s'] = room.s_to
    if room.e_to is not None:
        neighbors['e'] = room.e_to
    if room.w_to is not None:
        neighbors['w'] = room.w_to
    
    return neighbors

# BFS for unexplored room
def find_shortest_paths_to_unexplored_2(visited, curr_room):
    
    new_visited = set()

    q = Queue()
    q_dirs = Queue()
    q.enqueue([curr_room])

    while q.size() > 0:
        room_path = q.dequeue()
        if q_dirs.size() > 0:
            path = q_dirs.dequeue()
        else:
            path = []
        
        room = room_path[-1]
        if room.id not in new_visited:
            new_visited.add(room.id)

            unexplored_exits = find_unexplored_exits(room, visited)

            if len(unexplored_exits) > 0:
                return path
            
            neighbors = get_neighbors(room)
            for dir in neighbors:
                new_room_path = list(room_path) + [neighbors[dir]]
                new_path = list(path) + [dir]
                q.enqueue(new_room_path)
                q_dirs.enqueue(new_path)
    
    return None


def get_traversal_path(visited=None, path=None):
    if path is None and visited is None:
        path = []
        visited = {}
    
    
    # add the current_room to the visited array
    if player.current_room.id not in visited:
        visited[player.current_room.id] = {}
    
    for exit in player.current_room.get_exits():
        room_towards_exit = player.current_room.get_room_in_direction(exit).id
        # for visited rooms set the relevant exits to unexplored
        if room_towards_exit in visited:
            visited[player.current_room.id][exit] = room_towards_exit
            visited[room_towards_exit][get_opposite_dir(exit)] = player.current_room.id
        else:
            # for unexplored exits, add ?
            visited[player.current_room.id][exit] = '?'
    
    # if all rooms visited, return the path
    if len(visited) == len(room_graph):
        return path
    
    # get unexplored exits
    unexplored_exits = find_unexplored_exits(player.current_room, visited)

    # if no unexplored exit, find path to the nearest room with unexplored exit
    if len(unexplored_exits) is 0:
        
        shortest = find_shortest_paths_to_unexplored_2(visited, player.current_room)
        # n = find_unvisited_rooms_in_path(shortest, visited, player.current_room)
        
        
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
        get_traversal_path(visited, path)
        

    return path

# traversal_path = ['n', 'n']
traversal_path = get_traversal_path()

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



#######
# UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")