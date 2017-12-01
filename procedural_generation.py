# 'c' means character position
# 'w' means wall
# 'd' means door
# 'f' means floor
# 'v' means void

import random
import numpy
import battle


ROOM_WIDTH_MIN = 7
ROOM_WIDTH_MAX = 15
ROOM_HEIGHT_MIN = 7
ROOM_HEIGHT_MAX = 15
CORRIDOR_LENGTH_MIN = 3
CORRIDOR_LENGTH_MAX = 10
MONSTER_SPAWN_RATE = 5 #percentage


monsterlist = [
    None,
    battle.rat,
    battle.bug,
    battle.chrome,
    battle.firefox,
    battle.adder,
    battle.clippy,
    battle.explorer,
    battle.harp,
    battle.rat,
]

def add_two_lists(list1, list2):
    assert(len(list1) == len(list2))
    output = []
    for i in range(len(list1)):
        output.append(list1[i] + list2[i])
    return output

def put_2d_list_into_other_2d_list(renderer, small_list, big_list, start_pos):
    # start_pos is a list with the x and y coord in the big list where the small list should start
    assert(len(big_list) > len(small_list))
    assert(len(big_list[0]) > len(small_list[0]))

    small_list_counter_x = 0
    small_list_counter_y = 0
    for y in range(start_pos[1], start_pos[1] + len(small_list)):
        for x in range(start_pos[0], start_pos[0] + len(small_list[0])):
            renderer.print('Changing element: ', x, ' ', y)
            renderer.print('With small list counters: ', small_list_counter_x, ' ', small_list_counter_y)
            big_list[y][x] = small_list[small_list_counter_y][small_list_counter_x]
            small_list_counter_x += 1

        small_list_counter_x = 0
        small_list_counter_y += 1

        

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

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if random.randrange(1, 100) < MONSTER_SPAWN_RATE:
                room[y][x] = str(random.randrange(1, 9))

    return room

def create_corridor(length, orientation):
    # Returns a 2d list with the corridor which is two walls and one floor
    # Orientation is 'horizontal' or 'vertical'
    corridor = []

    if orientation == 'horizontal':
        wall_row = []
        floor_row = []
        for i in range(length):
            wall_row.append('w')
            floor_row.append('f')
        corridor.append(wall_row)
        corridor.append(floor_row)
        corridor.append(wall_row)

    elif orientation == 'vertical':
        row = ['w', 'f', 'w']
        for i in range(length):
            corridor.append(row)

    return corridor
            

def print_map(inp_map, inp_char_pos):
    #inp_map is a 2d list with characters representing the map state in each element
    #inp_char_pos is a list of length 2 with the first element being the x position and the second element being the y position
    old_map_value = inp_map[inp_char_pos[1]][inp_char_pos[0]] 
    inp_map[inp_char_pos[1]][inp_char_pos[0]] = 'c'
    print('Map: ')
    for y in range(len(inp_map)):
        print(inp_map[y])

    inp_map[inp_char_pos[1]][inp_char_pos[0]] = old_map_value

def print_2d_list(renderer, inp_list):
    for y in range(len(inp_list)):
        renderer.print(inp_list[y]) 

def get_input(renderer):
    return renderer.input()

def check_destination(renderer, movement_vector, inp_map, current_player_pos):
    # returns the character of the destination on the map
    if len(inp_map) == 0:
        renderer.print('procedural generation::check_destination given empty map')

    destination = []
    destination.append(current_player_pos[0] + movement_vector[0])
    destination.append(current_player_pos[1] + movement_vector[1])
    return inp_map[destination[1]][destination[0]]

def check_collision(renderer, movement_vector, inp_map, current_player_pos):
    # false for no collision, true for collision
    return not(check_destination(renderer, movement_vector, inp_map, current_player_pos) == 'f')

def extend_map_in_direction(renderer, direction, length, inp_map, start_pos):
    #Checks if the map is defined in the direction given
    # direction is string 'left', 'right', 'up', 'down'
    # length is int. Does not include the start_pos in the count
    # start_pos is list of 2 elements, x and y coord

    renderer.print('procedural_generation::extend_map_in_direction started', 'direction: ', direction, ' length: ', length, ' is inp_map empty: ', len(inp_map)==0, ' start_pos: ', start_pos)

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

        else:
            new_map = inp_map
    elif direction == 'right':
        if start_pos[0] + length >= len(inp_map[0]):
            list_addition = []
            for i in range(start_pos[0] + length - len(inp_map[0]) + 1):
                list_addition.append('v')

            for i in range(len(inp_map)):
                new_map.append(inp_map[i] + list_addition)
        else:
            new_map = inp_map

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
        else:
            new_map = inp_map

    elif direction == 'down':
        if start_pos[1] + length >=len(inp_map):
            renderer.print('Adding new lines down')
            list_addition = []
            for i in range(len(inp_map[0])):
                list_addition.append('v')
            
            for i in range(len(inp_map)):
                new_map.append(inp_map[i])
            for i in range(start_pos[1] + length - len(inp_map) + 1):
                new_map.append(list_addition)
                renderer.print('Added a line at the bottom')
        else:
            renderer.print('start_pos[1]: ', start_pos[1], ' length: ', length, ' len(inp_map): ', len(inp_map))
            renderer.print('Down does not need to add new lines')
            new_map = inp_map

    renderer.print('procedural_generation::extend_map_in_direction returning empty map?: ', len(new_map) == 0)
    return (new_map, char_pos_change_vector)
                
        
    
def check_if_void(renderer, inp_map, search_box_top_left, search_box_bottom_right):
    #Returns true if all the elements in the search boxes are void and false if not
    for y in range(search_box_top_left[1], search_box_bottom_right[1] + 1):
        for x in range(search_box_top_left[0], search_box_bottom_right[0] + 1):
            if not (inp_map[y][x] == 'v'):
                return False
    return True

def add_new_room(renderer, door_location, inp_map):
    #Create a new room spawning off the door location
    #Will do nothing if there is not enough space

    renderer.print('procedural_generation::add_new_room started', ' door_location: ', door_location, ' is inp_map empty: ', len(inp_map)==0)

    #Find the direction in which the new room is spawned
    door_orientation = '' #Either up, down, left, right
    char_pos_change_vector = []
    char_pos_change_vector.append(0)
    char_pos_change_vector.append(0)

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

    step_change_vector= []
    step_change_vector.append(0)
    step_change_vector.append(0)

    if door_orientation == 'left':
        #Make space for the new room

        inp_map, step_change_vector = extend_map_in_direction(renderer, 'left', corridor_length + new_room_width, inp_map, door_location)
        char_pos_change_vector = add_two_lists(char_pos_change_vector, step_change_vector)
        door_location = add_two_lists(door_location, step_change_vector)
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'up', new_room_height, inp_map, door_location)
        char_pos_change_vector = add_two_lists(char_pos_change_vector, step_change_vector)
        door_location = add_two_lists(door_location, step_change_vector)
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'down', new_room_height, inp_map, door_location)
        char_pos_change_vector = add_two_lists(char_pos_change_vector, step_change_vector)
        door_location = add_two_lists(door_location, step_change_vector)
        
        
        #Check whether the new room intersects an existing room

        search_box_top_left = [door_location[0] - new_room_width - corridor_length, door_location[1] - int(new_room_height/2) - 1]
        search_box_bottom_right = [door_location[0] - 1, door_location[1] + int(new_room_height/2) + 1]
        if check_if_void(renderer, inp_map, search_box_top_left, search_box_bottom_right):
            # Add the corridor and room
            renderer.print('There is space to the left for a new room')
            corridor = create_corridor(corridor_length, 'horizontal')
            corridor_start_top_left_x = door_location[0] - corridor_length
            corridor_start_top_left_y = door_location[1] - 1
            put_2d_list_into_other_2d_list(renderer, corridor, inp_map, [corridor_start_top_left_x, corridor_start_top_left_y]) 
            inp_map[door_location[1]][door_location[0]] = 'f'

            room = create_room(new_room_width, new_room_height)
            room_start_top_left_x = door_location[0] - corridor_length - new_room_width
            room_start_top_left_y = door_location[1] - int(new_room_height/2)
            put_2d_list_into_other_2d_list(renderer, room, inp_map, [room_start_top_left_x, room_start_top_left_y])

            inp_map[door_location[1]][door_location[0] - corridor_length - 1] = 'f'
        else:
            renderer.print('There is no space to the left for a new room')




    elif door_orientation == 'right':
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'right', 4, inp_map, door_location)
        char_pos_change_vector[0] += step_change_vector[0]
        char_pos_change_vector[1] += step_change_vector[1]
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'up', new_room_height, inp_map, door_location)
        char_pos_change_vector[0] += step_change_vector[0]
        char_pos_change_vector[1] += step_change_vector[1]
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'down', new_room_height, inp_map, door_location)
        char_pos_change_vector[0] += step_change_vector[0]
        char_pos_change_vector[1] += step_change_vector[1]
    elif door_orientation == 'up':
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'up', 4, inp_map, door_location)
        char_pos_change_vector[0] += step_change_vector[0]
        char_pos_change_vector[1] += step_change_vector[1]
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'left', new_room_width, inp_map, door_location)
        char_pos_change_vector[0] += step_change_vector[0]
        char_pos_change_vector[1] += step_change_vector[1]
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'right', new_room_width, inp_map, door_location)
        char_pos_change_vector[0] += step_change_vector[0]
        char_pos_change_vector[1] += step_change_vector[1]
    elif door_orientation == 'down':
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'down', 4, inp_map, door_location)
        char_pos_change_vector[0] += step_change_vector[0]
        char_pos_change_vector[1] += step_change_vector[1]
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'left', new_room_width, inp_map, door_location)
        char_pos_change_vector[0] += step_change_vector[0]
        char_pos_change_vector[1] += step_change_vector[1]
        inp_map, step_change_vector = extend_map_in_direction(renderer, 'right', new_room_width, inp_map, door_location)
        char_pos_change_vector[0] += step_change_vector[0]
        char_pos_change_vector[1] += step_change_vector[1]


        
    if len(inp_map) == 0:
        renderer.print('add_new_room returning 0 length inp_map')
    return (inp_map, char_pos_change_vector)
        
def main(renderer):
    random.seed()


    #create the starting room
    starting_room_width = random.randrange(15, 20)
    starting_room_height = random.randrange(15, 20)
    g_map = create_room(starting_room_width, starting_room_height)

    #place the character
    char_pos = [] # first element is x pos, second element is y pos
    char_pos.append(int(starting_room_width/2))
    char_pos.append(int(starting_room_height/2))


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
            renderer.print('unexpected key: ', player_input)

        destination_char = check_destination(renderer, movement_vector, g_map, char_pos)

        if check_destination(renderer, movement_vector, g_map, char_pos) == 'd':
            door_location = []
            door_location.append(char_pos[0] + movement_vector[0])
            door_location.append(char_pos[1] + movement_vector[1])
            g_map, char_pos_change_vector = add_new_room(renderer, door_location, g_map) 
            char_pos[0] += char_pos_change_vector[0]
            char_pos[1] += char_pos_change_vector[1]

        is_dest_monster = False
        try:
            int(destination_char)
            is_dest_monster = True
        except:
            dummy = 0
        
        if is_dest_monster:
            renderer.print('*******Battle start')
            battle.fight(battle.PLAYER, monsterlist[int(destination_char)], renderer)


        if not(check_collision(renderer, movement_vector, g_map, char_pos)):
            char_pos[0] += movement_vector[0]
            char_pos[1] += movement_vector[1]

        renderer.draw_map(g_map, char_pos, [])
             
