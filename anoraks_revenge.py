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
            return {"type": "move", "direction": direction, "error": None}
        elif direction and not action:
            return {"type": "move", "direction": direction, "error": None}
        elif action in ["take", "drop", "place", "open", "examine"] and obj:
            return {"type": action, "object": obj, "error": None}
        else:
            return {"error": "Invalid command"}

# game class should render itself
# while game not ended await input
# game class has game ended
# dictionary of locations so can do O(1) lookup
# for any location need an array of exits
# then game state will update
# rerender
# wait for input
# player location should be in game state not player
# game.render will call print(current_location.description)
#YAGNI follow this principle You Ain't Gonna Need It
# think of interfaces - a weapon interface and anything that implements a weapon interface has an attack function
# e.g. consumable interface, e.g. drink potion or destroy door
# exits can implement openable interface

class Game:
    def __init__(self, rooms):
        self.rooms = rooms
        self.player = Player()
        self.current_room = rooms["West of House"]
        self.input_interpreter = InputInterpreter()
        self.game_ended = False

    def render(self):
        print(self.current_room.description)

    def update_game_ended(self):
        self.game_ended = not self.game_ended
        print("Game Over")

    def move(self, direction):
        for exit in self.current_room.exits:
            if exit.direction == direction:
                if exit.is_open:
                    self.current_room = self.rooms[exit.destination]
                    return
                else:
                    print("That way is closed")
                    return
        print("You can't go that way")

class Room:
    def __init__(self, description, exits, inventory = []):
        self.description = description
        self.exits = exits
        self.inventory = inventory
    
    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        self.inventory.remove(item)


class Exit():
    def __init__(self, direction, destination, is_open=True):
        self.direction = direction
        self.destination = destination
        self.is_open = is_open
    
    def open(self):
        self.is_open = True
        print("You open the door")

    def close(self):
        self.is_open = False
        print("You close the door")

class Window(Exit):
    def open(self):
        self.is_open = True
        print("With great effort, you open the window far enough to allow entry")

    def close(self):
        self.is_open = False
        print("You close the window")

class Player:
    def __init__(self, inventory = []):
        self.inventory = inventory

    def add_item(self, item):
        self.inventory.append(item)
    
    def remove_item(self, item):
        self.inventory.remove(item)
    

def main():
    
    rooms = {
        "West of House": Room("You are standing in an open field west of a white house, with a boarded front door.\nThere is a small mailbox here", [
            Exit("north", "North of House")
        ]),
        "North of House": Room("You are facing the north side of a white house. There is no door here, and all the windows are boarded up. To the north a narrow path winds through the trees.", [
            Exit("west", "West of House"),
            Exit("east", "Behind House")
        ]),
        "Behind House": Room("You are behind the white house. A path leads into the forest to the east. In one corner of the house there is a small window which is slightly ajar.", [
            Exit("north", "North of House"),
            Exit("south", "South of House"),
            Window("east", "Kitchen", is_open=False)
        ]),
        "South of House": Room("You are facing the south side of a white house. There is a wooden door here. To the east there is a small window which is slightly ajar.", [
            Exit("west", "West of House"),
            Exit("east", "Behind House")
        ]),
        "Kitchen": Room("You are in the kitchen of the white house. A table seems to have been used recently for the preparation of food. A passage leads to the west and a dark staircase can be seen leading upward. To the east is a small window which is open.", [
            Exit("east", "Behind House"),
            Exit("west", "Living Room")
        ]),
        "Living Room": Room("You are in the living room. There is a doorway to the east, a wooden door with strange gothic lettering to the west, which appears to be nailed shut, a trophy case, and a large oriental rug in the center of the room.", [
            Exit("east", "Kitchen")
        ]),
    }
    game = Game(rooms)
    
    print("Ready Player One")
    input("Press enter to start...")

    print("\n")
    print("ZORK I: The Great Underground Empire")
    print("Copyright (c) 1981, 1982, 1983 Infocom, Inc. All rights reserved.")
    print("ZORK is a registered trademark of Infocom, Inc.")
    print("Revision 88 / Serial number 840726")
    print("\n")
    print("West of House")
    
    while not game.game_ended:
        game.render()
        user_input = input(">")
        command = game.input_interpreter.interpret(user_input)
        if command["error"]:
            print(command["error"])
        elif command["type"] == "move":
            game.move(command["direction"])
        elif command["type"] == "take":
            print("You take the " + command["object"])
        elif command["type"] == "drop":
            print("You drop the " + command["object"])
        elif command["type"] == "place":
            print("You place the " + command["object"])
        elif command["type"] == "open":
            print("You open the " + command["object"])
        elif command["type"] == "examine":
            print("You examine the " + command["object"])
        else:
            print("Invalid command")
        game.update_game_ended()
        

if __name__ == "__main__":
    main()