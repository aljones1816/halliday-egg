class InputInterpreter:
    def __init__(self):
        # Define mappings for actions and directions
        self.action_map = {
            "go": "move", "move": "move", "walk": "move", "run": "move",
            "take": "take", "grab": "take", "pick up": "take", "hold": "take",
            "drop": "drop", "leave": "drop", "discard": "drop","put down": "drop","throw": "drop",
            "place": "place", "put": "place", "set": "place", "install": "place",
            "open": "open", "close": "close",
            "examine": "examine", "look": "examine", "inspect": "examine", "read": "examine",
        }
        self.direction_map = {
            "north": "north", "n": "north",
            "south": "south", "s": "south",
            "east": "east", "e": "east",
            "west": "west", "w": "west",
            "up": "up", "down": "down"
        }
        self.object_map = {
            "mailbox": "mailbox",
            "egg": "egg",
            "jewel encrusted egg": "egg",
            "leaflet": "leaflet",
            "paper": "leaflet"
        }  

    def interpret(self, user_input):
        # Split input into words
        words = user_input.lower().split()

        action = None
        direction = None
        obj = None

        for word in words:
            if word in self.action_map and action is None:
                action = self.action_map[word]
            elif word in self.direction_map and direction is None:
                direction = self.direction_map[word]
            elif word in self.object_map and obj is None:
                obj = word

        # Compile a valid command based on the given logic
        if action == "move" and direction:
            return {"type": "move", "direction": direction}
        elif direction and not action:
            return {"type": "move", "direction": direction, "error": None}
        elif action in ["take", "drop", "place", "open", "examine"] and obj:
            return {"type": action, "object": obj, "error": None}
        else:
            return {"error": "Invalid command"}

class Room:
    def __init__(self, name, description, items):
        self.name = name
        self.description = description
        self.items = items
        self.exits = {}

    def __str__(self):
        return self.description
    
    def set_exit(self, direction, room):
        self.exits[direction] = room
    
    def get_exit(self, direction):
        return self.exits.get(direction)
    
    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

class Player:
    def __init__(self, start_location):
        self.inventory = []
        self.location = start_location

    def move(self, direction):
        new_location = self.location.get_exit(direction)
        if new_location:
            self.location = new_location
            return self.location
        else:
            return None
        
    def take(self, item):
        if item in self.location.items:
            self.location.items.remove(item)
            self.inventory.append(item)
            return item
        else:
            return None
        
    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.location.items.append(item)
            return item
        else:
            return None
    
    def examine(self, item):
        if item in self.location.items:
            return item.get_description()
        elif item in self.inventory:
            return item.get_description()
        else:
            return None
        
    def open(self, item):
        if item in self.location.items:
            return item.open()
        else:
            return None
    
    def place(self, item):
        if item in self.inventory:
            return item.place()
        else:
            return None
        
    def open_exit(self, direction):
        exit = self.location.get_exit(direction)
        if exit:
            return exit.open()
        else:
            return None
        
    def close_exit(self, direction):
        exit = self.location.get_exit(direction)
        if exit:
            return exit.close()
        else:
            return None
    
    def get_inventory(self):
        return self.inventory
    
    def get_location(self):
        return self.location
    
class Item:
    def __init__(self, name, description, inventory={}):
        self.name = name
        self.description = description
        self.inventory = inventory
    
    def __str__(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def open(self):
        return None
    
    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        self.inventory.remove(item)

class Exit:
    def __init__(self, open=False):
        self.open = open
    
    def open(self):
        self.open = True

    def close(self):
        self.open = False
    

def main():
    interpreter = InputInterpreter()
    player = Player()
    leaflet = Item("leaflet", "A leaflet.")
    mailbox = Item("mailbox", "A small mailbox.", [leaflet])
    egg = Item("egg", "A jewel encrusted egg.")
    trophyCase = Item("trophy case", "A trophy case.")
    room1 = Room("West of House", "You are standing in an open field west of a white house, with a boarded front door.", [mailbox])
    room2 = Room("North of House", "You are facing the north side of a white house. There is no door here, and all the windows are boarded up. To the north a narrow path winds through the trees.")
    room3 = Room("Behind House", "You are behind the white house. In one corner of the house there is a small window which is slightly ajar.")
    room4 = Room("Kitchen", "You are in the kitchen of the white house. A table seems to have been used recently for the preparation of food. To the east is a small window which is open.")
    room5 = Room("Living Room", "You are in the living room. There is a doorway to the east, a wooden door with strange gothic lettering to the west, which appears to be nailed shut, a trophy case, and a large oriental rug in the center of the room.", [trophyCase,egg])
    room6 = Room("South of House", "You are facing the south side of a white house. There is no door here, and all the windows are boarded up.")
    
    exit1 = Exit("north", room2)
    

    
    print("Ready Player One")
    input("Press enter to start...")

    print("\n")
    print("ZORK I: The Great Underground Empire")
    print("Copyright (c) 1981, 1982, 1983 Infocom, Inc. All rights reserved.")
    print("ZORK is a registered trademark of Infocom, Inc.")
    print("Revision 88 / Serial number 840726")
    print("\n")
    print("West of House")
    print("You are standing in an open field west of a white house, with a boarded front door.")
    print("There is a small mailbox here.")
    while True:
        playerInput = input("> ")
        command = interpreter.interpret(playerInput)
        if command["error"]:
            print("I don't understand that command.")
        else:
            print(command)

if __name__ == "__main__":
    main()