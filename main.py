"""
To-Do:
    
    meow
    
Primer for humans reading this code:
    
    This is my attempt for bringing to life a system of permanence 
    in a roguelike/rpg type setting, with no prior reading of similar code,
    using a functional paradigm
    
    I do understand that this goal would be best accomplished with OOP,
    but I'm not very advanced in OOP programming, and I'm looking for peer 
    review for my current practices, before I move on to finding a tutor
    or self teaching how to accomplish these same functionalities with class
    based structures
    
    I'm very open to best practice suggestions! A better and easier way to 
    accomplish a goal I'm perhaps walking circles around for lack of thought
    or experience
    
NOTE:
    
     a normal coordinates system is x, y, with x as the 'length' and y 
     as the 'height''
      
     using a nested list structure for the map is resulting in me 
     using the y coordinate first, and x coordinate second
      
     it is unnatural but I dont think its too eggregious, just takes
     a bit of getting used to 
      
     Forgive my typos :)
    
Design Note:
    
    I intend to create the systems that encompass an action loop
    (the actual function that moves the game state and contains
    the players choice of actions) before I create the action loop
    and state system, so I can keep the system in mind when writing the
    game state function
"""

import random
from data import item_dictionary, move_options, life_list, class_dict

direction_list = ["north", "west", "south", "east"]

basic_map = []
y_dim = 0
x_dim = 0

#when calling this function, pass 2 integers for map size
def map_gen(y = 10, x = 10):
    """
    purpose: generates a nested list structure of map objects
    y - the y coordinate (height)
    x - the x coordinate (width)
    """
    for value in range(x):
        #this list is essentially a container for map objects
        basic_map.append(list())

    for num in range(y):
        for num in range(y):
            basic_map[num].append({
                #accessible is essentially a collision variable
                "accessible": True,
                "type:": "ground",
                "contents": {
                             #itemName: quantity
                             },
                "occupied": False,
                "occupant": None
                        })
    return y, x


def free_space():
    """
    y: map coordinate y size
    x: map coordinate x size
    
    The purpose of this function is to randomly choose
    a non occupied map square coordinate if we want to generate
    a mob or NPC
    
    returns:
        a valid set of existable coordinates (idealy)
    """
    y, x = y_dim, x_dim
    while True:
        rand_y = random.randint(0, y-1)
        rand_x = random.randint(0, x-1)
        if move_check((rand_y, rand_x)):
            coordinates = [rand_y, rand_x]
            return coordinates
        else:
            continue


def location_state_change(coordinates, name):
    """
    this function serves the purpose of altering the state
    of a square that an npc or player either begins on, or moves to
    """
    basic_map[coordinates[0]][coordinates[1]]["occupied"] = True
    basic_map[coordinates[0]][coordinates[1]]["occupant"] = name


def return_location(coordinates):
    """
    purpose: to make a commonly used ugly piece of code bareable
    
    coordinates: a location to be called up
    """
    return basic_map[coordinates[0]][coordinates[1]]


def npc_generator(name):
    """
    name:      a string to identify a living entity by
    hp:        health points
    inventory: a list containing possessed items
    
    returns:
        nothing
    """
    name = name.lower()
    
    coordinates = free_space()
    
    hp = random.randint(25, 50)
    life_list[name] = {
                       "hp": hp,
                       "defense": 10,
                       "dexterity": random.randint(1, 6),
                       "strength": random.randint(1, 6),
                       "constitution": random.randint(1, 6),
                       "intelligence": random.randint(1, 6),
                       "charisma": random.randint(1, 6),
                       "luck": 5,
                       "attack": 1,
                       "inventory": {1: 10}, #item_dictionary ID 1: quantity 10
                       "hostile": False,
                       "npc": True  ,
                       "location": coordinates
                       }
    basic_map[coordinates[0]][coordinates[1]]["occupied"] = True
    basic_map[coordinates[0]][coordinates[1]]["occupant"] = name
    

#Barebones right now, will need more information when main_loop exists
def pc_generator(name = None, pc_class = None):
    """
    Function Needs:
        create the player character
        name, base stats, inventory,
        location 
    """
    class_list = ["fighter", "rogue", "random"]
    
    if name == None and pc_class == None:
        name = input("Enter a name for your character: ").lower()
        while True:
            pc_class = input("Enter your choice of class: Fighter, Rogue, Random\n").lower()
            if pc_class in class_list:
                break
            else:
                print("Please enter one of the options printed.")
    
    stats = class_dict[pc_class]
    
    start_location = free_space()
    
    life_list[name] = stats
    life_list[name]["location"] = start_location
    life_list[name]["npc"] = False
    life_list[name]["inventory"] = {}
    location_state_change(start_location, name)


#Needs Writing
def npc_level_up(npc_class, name):
    """
    will take an npc object in the life_list
    and raise stats according to their class,
    with an emphasis on randomization
    """
    pass


def is_adjacent(name):
    """
    TODO:
        make the returns of isadjacent a dictionary where
        the coordinates is a value of the key "direction"
        ie.. east: [3, 2]
    
    this functional will determine whether or not a square
    adjacent to a specific entity on life_list
    if yes, this will allow the picking up of ground inventory
    from adjacent squares, and allow for the interaction with
    npcs whether friend or foe
    """
    #this sets coordinates to an entity we want to find adjacent squares of
    coordinates = life_list[name]["location"]
    
    #test print for clarity
    print("current coordinates: " + str(coordinates))
    
    adjacent_options = { "south": [coordinates[0] + 1, coordinates[1]],
                         "north": [coordinates[0] - 1, coordinates[1]],
                        "east": [coordinates[0], coordinates[1] + 1],
                        "west": [coordinates[0], coordinates[1] - 1]}
    
    adjacent_locations = {"location_list": []}
    
    for direction in adjacent_options:
        if move_check(adjacent_options[direction], is_adjacent = False):
            adjacent_locations["location_list"].append(adjacent_options[direction])
            adjacent_locations[direction] = adjacent_options[direction]
    
    return adjacent_locations


#Needs Writing
def npc_inventory_management():
    """
    will be ran upon npc creation and provide
    randomized inventory generation based on 
    class derived needs
    """    
    pass
    

def look_inventory(coordinates):
    """
    this function will run after look to call up and format the 
    inventory of a location square
    """
    contents = basic_map[coordinates[0]][coordinates[1]]["contents"]
    
    if contents:
        print(item_dictionary[contents[0]])


def look(name, direction = None):
    """
    this function will be a command in the game loop
    it will allow you to observe the properties of adjacent squares
    and will lead into the ability to grab objects off the ground 
    """
    direction_options = ["north", "south", "east", "west"]
    
    if direction == None:
        while True:
            direction = input("Which direction would you like to look?\n").lower()
            if direction not in direction_options:
                print("Please enter North East South or West.")
            else:
                break
    
    relavant = is_adjacent(name)
    
    for key in relavant:
        if key == direction:
            print("{} is: {}".format(direction, relavant[key]))
            look_inventory(relavant[key])
            return relavant[key]
        
    print("This square is not lookable")

    
#Needs Writing
def pc_inventory_management(name, action, direction):
    """
    will contain functionality that allows inventory
    to transfer from the ground or a trader, into the player
    inventory
    or from player inventory to the ground
    
    viable_locations: a list of coordinate values for adjacent squares
    """
    
    viable_locations = is_adjacent(name)
    if action == "loot":
        
        print("action is loot")
        print(direction)
        
        if direction in direction_list:
            
            try:
                location = viable_locations[direction]
                print(location)
            except:
                print("That's not a viable direction from your current position")
                return None
            
            if return_location(location)["contents"]:
                
                buffer = basic_map[location[0]][location[1]]["contents"]
                basic_map[location[0]][location[1]]["contents"] = []
                life_list[name]["inventory"] = buffer
    
    if action == "drop":
        pass
    
    if action == "trade":
        pass
        


def populate_ground():
    """
    this function will deal with random list generation on the ground

    """
    y_count = -1
    
    for y in basic_map:
        
        x_count = -1
        y_count += 1
        
        for x in basic_map:
            
            x_count += 1
            
            item = random.randint(1, len(item_dictionary))
            chance = random.random()
            
            if chance >= 0.25 and item != 1:
                basic_map[y_count][x_count]["contents"] = [item, 1]
            elif item == 1:
                basic_map[y_count][x_count]["contents"] = [item, random.randint(1, 50)]


#Needs Writing
def equip():
    """
    this function will take a weapon and or armor from 
    a living object's inventory and place it into their active
    use slot, which will then boost their stats by its 
    associated value
    NPC handling will be automated, with best weapon and armor available
    per equip slot
    PC handling will be manual, and will be an available command for use
    when the player is able to input an action
    """
    pass


#Needs Writing
def trading():
    """
    this functional will initially serve the purpose of transfering 
    inventory between PC and an adjacent non-hostile npc
    """
    pass


#Needs Writing
def attack_action():
    """
    this function will execute an attack from 1 living entity
    upon another
    """
    pass


#Needs Writing
def npc_ai(name):
    """
    name: the living object in reference
    
    this will take some consideration into the idea
    of code optimization, considering how many times this 
    functional will be ran
    """
    if life_list[name]["hostile"] == True:
        pass
    else:
        #friendly_ai: villagers/traders/followers/travelers
        pass


#needs fixed
def value_query(meta):
    """
    meta: metadata must be a dictionary of an item
    
    returns:
        total value in integer
    """
    #Expected meta input format: (item_id, item_quantity)
    identifyer = meta["id"]
    quantity = meta["quantity"]
    value = item_dictionary[identifyer]["value"]
    total_value = value * quantity
    return total_value


def move_check(coordinates, is_adjacent = False):
    """
    will check the desired coordinates for occupied and accessible values
    if occupied and or innaccessible, function will return False
    if not occupied AND accessible, will return True
    
    the purpose of is_adjacent being checked here is to recycle code
    a nuance for the is_adjacent use of this function is to return True
    
    
    is_adjacent: passed as True when using the is_adjacent function
    coordinates: a list containing the x and y coordinates of the player
    """
    try:
        #print(coordinates)
        
        #returns false (cant move to this location) if either coordinate is negative
        #reason: indexing a list with a negative value returns the last element
        for num in coordinates:
            if num > -1:
                pass
            else:
                return False
        
        if is_adjacent:
            return True
        
        #checks for 2 prerequisite variables for a square to be movable
        if basic_map[coordinates[0]][coordinates[1]]["accessible"] == True:
            if basic_map[coordinates[0]][coordinates[1]]["occupied"] == False:
                return True
        
        else:
            return False
        
    except Exception as e:
        print("WE ARE AT MOVE_CHECK EXCEPT STATEMENT:")
        print(e)
        return False
    
    
#note: coordinates must be a list
def move_logic(direction, name):
    """
    coordinates: starting coordinates before move_logic function
    
    Explanation of purpose:
        this function serves the purpose of moving a coordinate pair to 
        a viable new location
        
        can and will be applied to the player character, npcs or mobs
    
    direction: 
    
    returns:
        a new coordinates for an entity
    """
    
    coordinates = life_list[name]["location"]
    coord_string = "New coordinates are: {}"
    bad_location = "This direction is not accessable"
    direction = direction.lower()
    
    #each "option" is a dictionary key that signifies a direction:
    #                north, east, south, west
    #the contents of each dictionary is a list of acceptable responses
    #to trigger movement in that direction, ie, "up" = "north", "n" = "north"
    
    if coordinates[0] > (y_dim -1):
        print("Location is out of boundaries")
        return None
    
    if coordinates[1] > (x_dim -1):
        print("Location is out of boundaries")
        return None
    
    for option in move_options:
        if direction in move_options[option]:
            
            #these 2 lines will take the old occupied space and remove occupation
            basic_map[coordinates[0]][coordinates[1]]["occupied"] = False
            basic_map[coordinates[0]][coordinates[1]]["occupant"] = None
            
            if option == "north":
                coordinates[0] -= 1
                if move_check(coordinates):
                    print(coord_string.format(coordinates))
                    location_state_change(coordinates, name)
                    return coordinates
                else:
                    print(bad_location, "NORTH")
                    break
                    
            elif option == "east":
                coordinates[1] += 1
                if move_check(coordinates):
                    print(coord_string.format(coordinates))
                    location_state_change(coordinates, name)
                    return coordinates
                else:
                    print(bad_location, "EAST")
                    break
                    
            elif option == "south":
                coordinates[0] += 1
                if move_check(coordinates):
                    print(coord_string.format(coordinates))
                    location_state_change(coordinates, name)
                    return coordinates
                else:
                    print(bad_location, "SOUTH")
                    break
                
            elif option == "west":
                coordinates[1] -=1
                if move_check(coordinates):
                    print(coord_string.format(coordinates))
                    location_state_change(coordinates, name)
                    return coordinates
                else:
                    print(bad_location, "WEST")
                    break
                    
    print("That is not a viable Direction input")


def randomizer(y_range, x_range):
    """
    *INTENDED FOR COMMAND PROMPT USE*
    
    this function exists to generate random coordinates for
    "test_function" to test movement possibilities with
    
    y_range: the height of numbers that can be generated in the y coordinate
    x_range: the range of numbers that can be generates for the x coordinate
    
    returns: y, x
    """
    y = random.randint(0, y_range)
    x = random.randint(0, x_range)
    return y, x


y_dim, x_dim = map_gen()

pc_generator(name = "ian",  pc_class = "fighter")

populate_ground()
