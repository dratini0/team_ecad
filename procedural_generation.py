# 'c' means character position
# 'w' means wall
# 'd' means door
# 'f' means floor
# 'v' means void

import random
import numpy


ROOM_WIDTH_MIN = 7
ROOM_WIDTH_MAX = 15
ROOM_HEIGHT_MIN = 7
ROOM_HEIGHT_MAX = 15
CORRIDOR_LENGTH_MIN = 3
CORRIDOR_LENGTH_MAX = 10



def create_room(width, height):
    # Returns a 2d list with the room
    # The width and height includes the walls i.e. the walkable space is smaller than the given width and height
    # The room will have 4 doors

    assert(width >= 3)
    assert(height >= 3)

    room = [] 
    for y in range(height):
        line_to_add = []
        for x in range(width):
            char_to_add = 'v'
            if x == 0 or y == 0 or x == width -1 or y == height -1:
                char_to_add = 'w' 
            else:
                char_to_add = 'f'
            line_to_add.append(char_to_add)
        room.append(line_to_add)

    width_middle = int(width/2)
    height_middle = int(height/2)
    room[0][width_middle] = 'd'
    room[height - 1][width_middle] = 'd'
    room[height_middle][0] = 'd'
    room[height_middle][width -1 ] = 'd'

    return room

def print_map(inp_map, inp_char_pos):
    #inp_map is a 2d list with characters representing the map state in each element
    #inp_char_pos is a list of length 2 with the first element being the x position and the second element being the y position
    old_map_value = inp_map[inp_char_pos[1]][inp_char_pos[0]] 
    inp_map[inp_char_pos[1]][inp_char_pos[0]] = 'c'
    print('Map: ')
    for y in range(len(inp_map)):
        print(inp_map[y])

    inp_map[inp_char_pos[1]][inp_char_pos[0]] = old_map_value

def get_input(renderer):
    return renderer.input()

def check_destination(movement_vector, inp_map, current_player_pos):
    # returns the character of the destination on the map
    destination = []
    destination.append(current_player_pos[0] + movement_vector[0])
    destination.append(current_player_pos[1] + movement_vector[1])
    return inp_map[destination[1]][destination[0]]

def check_collision(movement_vector, inp_map, current_player_pos):
    # false for no collision, true for collision
    return not(check_destination(movement_vector, inp_map, current_player_pos) == 'f')

def extend_map_in_direction(direction, length, inp_map, start_pos):
    #Checks if the map is defined in the direction given
    # direction is string 'left', 'right', 'up', 'down'
    # length is int. Does not include the start_pos in the count
    # start_pos is list of 2 elements, x and y coord

    new_map = []
    char_pos_change_vector = [] # The vector which is to be added to the character position to keep them in the correct position on the map
    char_pos_change_vector.append(0)
    char_pos_change_vector.append(0)

    if direction == 'left':
        if start_pos[0] - length < 0:
            # Create the new list that will be added to the start of each row
            list_addition = []
            for i in range(abs(start_pos[0] - length)):
                list_addition.append('v')
                char_pos_change_vector[0] += 1

            # Add the addition to the start of each row in the new map
            for i in range(len(inp_map)):
                new_map.append(list_addition + inp_map[i])
    elif direction == 'right':
        if start_pos[0] + length >= len(inp_map[0]):
            list_addition = []
            for i in range(start_pos[0] + length - len(inp_map[0]) + 1):
                list_addition.append('v')

            for i in range(len(inp_map)):
                new_map.append(inp_map[i] + list_addition)

    elif direction == 'up':
        if start_pos[1] - length < 0:
            list_addition = []
            for i in range(len(inp_map[0])):
                list_addition.append('v')

            for i in range(abs(start_pos[1] - length)):
                new_map.append(list_addition)
                char_pos_change_vector[1] += 1
            for i in range(len(inp_map)):
                new_map.append(inp_map[i])

    elif direction == 'down':
        if start_pos[1] + length >=len(inp_map):
            list_addition = []
            for i in range(len(inp_map[0])):
                list_addition.append('v')
            
            for i in range(len(inp_map)):
                new_map.append(inp_map[i])
            for i in range(start_pos[1] + length - len(inp_map) + 1):
                new_map.append(list_addition)


    return (new_map, char_pos_change_vector)
                
        
    

def add_new_room(door_location, inp_map):
    #Create a new room spawning off the door location
    #Will do nothing if there is not enough space

    #Find the direction in which the new room is spawned
    door_orientation = '' #Either up, down, left, right
    char_pos_change_vector = []

    if door_location[0] == 0:
        door_orientation = 'left' 
    else:
        char_to_left_of_door = inp_map[door_location[1]][door_location[0] - 1]
        if char_to_left_of_door == 'v':
            door_orientation = 'left'
        elif char_to_left_of_door == 'w':
            if door_location[1] == 0:
                door_orientation = 'up'
            else:
                char_on_top_of_door = inp_map[door_location[1] - 1][door_location[0]]
                if char_on_top_of_door == 'v':
                    door_orientation = 'up'
                else:
                    door_orientation = 'down'

        elif char_to_left_of_door == 'f':
            door_orientation = 'right'

    print('door orienation is: ', door_orientation)

    corridor_length = random.randrange(CORRIDOR_LENGTH_MIN, CORRIDOR_LENGTH_MAX)
    new_room_width = random.randrange(ROOM_WIDTH_MIN, ROOM_WIDTH_MAX)
    new_room_height = random.randrange(ROOM_HEIGHT_MIN, ROOM_HEIGHT_MAX)

    if door_orientation == 'left':
        # inp_map, char_pos_change_vector = extend_map_in_direction('left', corridor_length + new_room_width, inp_map, door_location)
        inp_map, char_pos_change_vector = extend_map_in_direction('left', 4, inp_map, door_location)
    elif door_orientation == 'right':
        inp_map, char_pos_change_vector = extend_map_in_direction('right', 4, inp_map, door_location)
    elif door_orientation == 'up':
        inp_map, char_pos_change_vector = extend_map_in_direction('up', 4, inp_map, door_location)
    elif door_orientation == 'down':
        inp_map, char_pos_change_vector = extend_map_in_direction('down', 4, inp_map, door_location)
        
    if len(inp_map) == 0:
        print('add_new_room returning 0 length inp_map')
    return (inp_map, char_pos_change_vector)
        
def main(renderer):
    random.seed()


    #create the starting room
    starting_room_width = random.randrange(7, 10)
    starting_room_height = random.randrange(7, 10)
    g_map = create_room(starting_room_width, starting_room_height)

    #place the character
    char_pos = [] # first element is x pos, second element is y pos
    char_pos.append(int(starting_room_width/2))
    char_pos.append(int(starting_room_height/2))

    print_map(g_map, char_pos)

    while(1):
        player_input = get_input(renderer)
        movement_vector = []
        if player_input == 'KEY_UP':
            movement_vector.append(0)
            movement_vector.append(-1)
        elif player_input == 'KEY_DOWN':
            movement_vector.append(0)
            movement_vector.append(1)
        elif player_input == 'KEY_LEFT':
            movement_vector.append(-1)
            movement_vector.append(0)
        elif player_input == 'KEY_RIGHT':
            movement_vector.append(1)
            movement_vector.append(0)
        else:
            print('unexpected key: ', player_input)

        if check_destination(movement_vector, g_map, char_pos) == 'd':
            door_location = []
            door_location.append(char_pos[0] + movement_vector[0])
            door_location.append(char_pos[1] + movement_vector[1])
            g_map, char_pos_change_vector = add_new_room(door_location, g_map) 
            char_pos[0] += char_pos_change_vector[0]
            char_pos[1] += char_pos_change_vector[1]

        if not(check_collision(movement_vector, g_map, char_pos)):
            char_pos[0] += movement_vector[0]
            char_pos[1] += movement_vector[1]

        renderer.draw_map(g_map, char_pos, [])
             
