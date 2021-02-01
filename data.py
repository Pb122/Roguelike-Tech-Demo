# -*- coding: utf-8 -*-
import random

#The idea here is to have a searchable ID per disctinct item
item_dictionary = {
    
    1: {
        "name": "gold",
        "type": "currency",
        "value": 1
        },

    2: {
        "name": "dagger",
        "type": "weapon",
        "attack": 1,
        "speed": 4,
        "value": 2
        },

    3: {
        "name": "short sword",
        "type": "weapon",
        "attack": 2,
        "speed": 2,
        "value": 3
        },
    
    4: {
        "name": "long sword",
        "type": "weapon",
        "attack": 4,
        "speed": 2,
        "value": 5
        },
    
    5: {
        "name": "leather armor",
        "type": "armor",
        "defense": 2,
        "mobility": 4,
        "value": 5
        }

}


move_options = {"north": ["up", "north", "n"],
               "south": ["down", "south", "s"],
               "east": ["right", "east", "e"],
               "west": ["left", "west", "w"]}


#The idea behind inventory structure is to use the item_dictionary ID
#as the key, and the quantity of item in the inventory as the value
generic_inventory = {
                     1: 35,
                     4: 1
                     }


life_list = {
    
    }


class_dict = {"fighter": {"hp": 50,
                         "strength": 6,
                         "constitution": 6,
                         "defense": 5,
                         "dexterity": 3,
                         "intelligence": 3,
                         "charisma": 3,
                         "luck": 1},
                         
              "rogue": {"hp": 30,
                        "strength": 3,
                        "constitution": 2,
                        "defense": 4,
                        "dexterity": 6,
                        "intelligence": 5,
                        "charisma": 3,
                        "luck": 6},
                  
              "random": {"hp": random.randint(30, 50),
                         "strength": random.randint(1, 6),
                         "constitution": random.randint(1,6),
                         "defense": random.randint(1, 5),
                         "dexterity": random.randint(1, 6),
                         "intelligence": random.randint(1, 6),
                         "charisma": (1, 6),
                         "luck": random.randint(3, 6)}  
              }

