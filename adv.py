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
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
def get_traversal_path(visited=None, path=None, count=None):
    if path is None and visited is None and count is None:
        path = []
        visited = {}
        count=0
        
    
    if player.current_room.id not in visited:
        visited[player.current_room.id] = {}
    
    for exit in player.current_room.get_exits():
        if exit not in visited[player.current_room.id]:
            visited[player.current_room.id][exit] = '?'
            count+= 1
    
    # q = Queue()
    # q.enqueue(player.current_room.id)
    exits = player.current_room.get_exits()
    dir = random.choice(exits)

    approve = False
    if len(path) is 0:
            approve = True
            # dir = None
    
    # if len(path) is 0:
    #     approve = True
    # elif dir is 'n' and path[-1] is 's':
    #     approve = False
    # elif dir is 's' and path[-1] is 'n':
    #     approve = False
    # elif dir is 'e' and path[-1] is 'w':
    #     approve = False
    # elif dir is 'w' and path[-1] is 'e':
    #     approve = False
    
    if not approve:
        dir = random.choice(exits)
        if dir is 'n' and path[-1] is 's' and len(exits) > 1:
            approve = False
        elif dir is 's' and path[-1] is 'n' and len(exits) > 1:
            approve = False
        elif dir is 'e' and path[-1] is 'w' and len(exits) > 1:
            approve = False
        elif dir is 'w' and path[-1] is 'e' and len(exits) > 1:
            approve = False
        else:
            approve = True
    
    if dir:
        path.append(dir)
        count -= 1
        new_room = player.current_room.get_room_in_direction(dir).id
        visited[player.current_room.id][dir] = new_room
        # print('Check me', visited[player.current_room.id][dir])
        if dir is 'n':
            visited[new_room] = {'s':player.current_room.id}
        elif dir is 's':
            visited[new_room] = {'n':player.current_room.id}
        elif dir is 'e':
            visited[new_room] = {'w':player.current_room.id}
        elif dir is 'w':
            visited[new_room] = {'e':player.current_room.id}
        player.travel(dir)
    
        if len(visited) < len(room_graph):
            get_traversal_path(visited, path, count)
        else:
            print('Here', count, visited)

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
# print('Hello', len(visited_rooms), len(room_graph))
if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
