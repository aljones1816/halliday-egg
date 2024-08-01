import time
import sys

def typewriter_effect(text, delay=0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after the text is printed

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
            "talk": "speak", "speak": "speak","greet":"speak"
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
            "paper": "leaflet",
            "window": "window",
            "wall": "wall",
            "man": "anorak",
            "wizard": "anorak",
            "old man": "anorak",
            "anorak": "anorak"
        }  

    def interpret(self, user_input):
        # Split input into words
        words = user_input.lower().split()

        action = None
        direction = None
        obj = None
        recipient = None

        for word in words:
            if word in self.action_map and action is None:
                action = self.action_map[word]
            elif word in self.direction_map and direction is None:
                direction = self.direction_map[word]
            elif word in self.object_map and obj is None:
                obj = self.object_map[word]
            elif word in self.object_map and obj is not None:
                recipient = self.object_map[word]

        # Compile a valid command based on the given logic
        if action == "move" and direction:
            return {"type": "move", "direction": direction, "error": None}
        elif direction and not action:
            return {"type": "move", "direction": direction, "error": None}
        elif action in ["take", "drop", "open", "examine", "close","speak"] and obj:
            return {"type": action, "object": obj, "error": None}
        elif action in ["place"] and obj and recipient:
            return {"type": action, "object": obj, "recipient": recipient, "error": None}
        else:
            return {"error": "Invalid command"}


class Game:
    def __init__(self, rooms):
        self.rooms = rooms
        self.player = Player()
        self.current_room = rooms["West of House"]
        self.input_interpreter = InputInterpreter()
        self.game_ended = False
        self.render()

        while not self.game_ended:
            user_input = input(">")
            self.handle_input(user_input)
            for item in self.player.inventory:
                if item.name == "leaflet":
                    self.update_game_ended()
        # victory scroll
        typewriter_effect("----------------------------------------------------", delay=0.05)
        typewriter_effect("You place the egg into the trophy case and a glow begins to emanate from inside.",delay=0.05)
        typewriter_effect("\n", delay=0.08)
        typewriter_effect("Behind you, Anorak appears in a whirl of smoke and a clap of thunder.",delay=0.05)
        typewriter_effect("\n", delay=0.08)
        typewriter_effect("'Congratulations Parzival... er... Claire!' He bellows.",delay=0.05)
        typewriter_effect("'You have completed the challenge and won my game! As a reward, I will share with you the secret passcode for the Green Lock Box'",delay=0.05)
        typewriter_effect("Anorak leans forward and says in an almost whisper, 'The code is:",delay=0.05)
        typewriter_effect("\n", delay=0.08)
        typewriter_effect("4   2   0", delay=0.08)
        typewriter_effect("\n", delay=0.08)
        typewriter_effect("'Remember it well, and good luck on the rest of you quest! Farewell!'",delay=0.05)
        typewriter_effect("\n", delay=0.08)
        typewriter_effect("Anorak's avatar fades into mist, which forms itself in letters reading: ",delay=0.05)
        print("""
 __ __   ____  ____  ____  __ __      ____   ____  ____  ______  __ __  ___     ____  __ __ 
|  |  | /    ||    \|    \|  |  |    |    \ |    ||    \|      ||  |  ||   \   /    ||  |  |
|  |  ||  o  ||  o  )  o  )  |  |    |  o  ) |  | |  D  )      ||  |  ||    \ |  o  ||  |  |
|  _  ||     ||   _/|   _/|  ~  |    |     | |  | |    /|_|  |_||  _  ||  D  ||     ||  ~  |
|  |  ||  _  ||  |  |  |  |___, |    |  O  | |  | |    \  |  |  |  |  ||     ||  _  ||___, |
|  |  ||  |  ||  |  |  |  |     |    |     | |  | |  .  \ |  |  |  |  ||     ||  |  ||     |
|__|__||__|__||__|  |__|  |____/     |_____||____||__|\_| |__|  |__|__||_____||__|__||____/ 
                                                                                            
    __  _       ____  ____  ____     ___  __  __  __                                        
   /  ]| |     /    ||    ||    \   /  _]|  ||  ||  |                                       
  /  / | |    |  o  | |  | |  D  ) /  [_ |  ||  ||  |                                       
 /  /  | |___ |     | |  | |    / |    _]|__||__||__|                                       
/   \_ |     ||  _  | |  | |    \ |   [_  __  __  __                                        
\     ||     ||  |  | |  | |  .  \|     ||  ||  ||  |                                       
 \____||_____||__|__||____||__|\_||_____||__||__||__|                                       
                                                                                            
""")
        while True:
            pass


    def handle_input(self, user_input):
        command = self.input_interpreter.interpret(user_input)
        if command["error"]:
            print("I don't understand that command. Alan didn't program me good.")
            return
        if command["type"] == "move":
            self.move(command["direction"])
        elif command["type"] == "take":
            self.take_item(command["object"])
        elif command["type"] == "drop":
            self.drop_item(command["object"])
        elif command["type"] == "place":
            self.place_item_in(command["object"],command["recipient"])
        elif command["type"] == "open":
            self.open(command["object"])
        elif command["type"] == "close":
            self.close(command["object"])
        elif command["type"] == "examine":
            self.examine(command["object"])
        elif command["type"] == "speak":
            self.speak(command["object"])
        else:
            print("I don't understand that command. Alan didn't program me good.")

    def render(self):
        print(self.current_room.description)

    def update_game_ended(self):
        self.game_ended = not self.game_ended
        print("Game Over")

    def move(self, direction):
        for exit in self.current_room.exits:
            if exit.direction == direction:
                if not exit.closed:
                    self.current_room = self.rooms[exit.destination]
                    if not self.current_room.visited:
                        self.current_room.visited = True
                    self.current_room.update_description()
                    self.render()
                    return
                else:
                    print("That way is closed")
                    return
        print("You can't go that way")

    def take_item(self, item_name):
        item = self.current_room.get_item_by_name(item_name)
        if item and item.is_moveable:
            self.current_room.remove_item(item)
            self.player.inventory.append(item)
            print(f"you take {item_name}.")
            return
        elif item and not item.is_moveable:
            print(f"You can't take that.")
    
        else: 
            for room_item in self.current_room.inventory:
                if not room_item.closed:
                    item = room_item.get_item_by_name(item_name)
                    if item:
                        room_item.remove_item(item)
                        self.player.inventory.append(item)
                        print(f"You take {item_name} from {room_item.name}")
                        return
                    
        print(f"{item_name} is not in the room")

    def drop_item(self, item_name):
        item = self.player.get_item_by_name(item_name)
        if item:
            self.current_room.inventory.append(item)
            self.player.remove_item(item)
            print(f"you drop {item_name}.")
            return
        else:
            print(f"You don't have that item.")
            return
        
    def place_item_in(self,item_name, recipient):
        item = self.player.get_item_by_name(item_name)
        if item:
            for room_item in self.current_room.inventory:
                if room_item.name == recipient:
                    self.player.remove_item(item)
                    room_item.inventory.append(item)
                    print(f"You place the {item_name} into the {recipient}")
                    return
                print(f"There isn't a {recipient} in this room.")
                return
        print(f"You don't have that item")
        return
    
    def open(self, item_name):
        item = self.current_room.get_item_by_name(item_name)
        if item and item.is_openable:
            if item.closed:
                item.open()
                print(f"You open the {item_name}")
                return
            print(f"The {item_name} is already open")
        elif item and not item.is_openable:
            print(f"You can't do that")
            return

        else:
            for exit in self.current_room.exits:
                if exit.gate == item_name:
                    if exit.closed:
                            exit.open()
                            return
                    print(f"{item_name} is already open")
                    return
        print(f"There is nothing to open by that name in the current room.")

    def close(self,item_name):
        item = self.current_room.get_item_by_name(item_name)
        if item and item.is_openable:
            if not item.closed:
                item.close()
                print(f"You close the {item_name}")
                return
            print(f"The {item_name} is already closed")
        elif item and not item.is_openable:
            print(f"You can't do that")
            return

        else:
            for exit in self.current_room.exits:
                if exit.gate == item_name:
                    if not exit.closed:
                            exit.close()
                            return
                    print(f"{item_name} is already closed")
                    return
        print(f"There is nothing to close by that name in the current room.")
    
    def speak(self, item_name):
        item = self.current_room.get_item_by_name(item_name)
        if item :
            item.speak()
            return
        else: 
            for room_item in self.current_room.inventory:
                if not room_item.closed:
                    item = room_item.get_item_by_name(item_name)
                    if item:
                        item.speak()
                        return
                    
        print(f"{item_name} is not in the room, you're speaking to air.")

    # TODO: add method to examine - case for item and case for room and case for self (inventory)

class Room:
    def __init__(self, initial_description, visited_description, exits, inventory = [], visited = False):
        self.description = initial_description
        self.visited_description = visited_description
        self.exits = exits
        self.inventory = inventory
        self.visited = visited
    
    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def update_description(self):
        if self.visited:
            self.description = self.visited_description

    def get_item_by_name(self, name):
        for item in self.inventory:
            if item.name == name:
                return item
        return None

class Item:
    def __init__(self, name, description,inventory=[], moveable=True, closed=False, is_openable=False):
        self.name = name
        self.description = description
        self.moveable = moveable
        self.inventory = inventory
        self.closed = closed
        self.is_openable = is_openable

    def get_description(self):
        return self.description

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def get_item_by_name(self, name):
        for item in self.inventory:
            if item.name == name:
                return item
        return None
    
    def open(self):
        self.closed=False
    
    def close(self):
        self.closed=True

    def speak(self):
        print("Umm... this is an inanimate object, Claire.")
    
    def attack(self):
        print("You attack visciously but miss, falling over and hitting your head in the process.")

class Anorak(Item):
    def __init__(self, name, description,inventory=[], moveable=False, closed=True, is_openable=False):
        super().__init__(name, description,inventory, moveable, closed, is_openable)
        self.spoken = False
        self.initial_conversation = """'Hey, kid!' The wizard says jovially, smiling in greeting.
        'The name's Halliday, James Halliday, although right now I'm more recognizeable as my avatar, Anorak the wizard.
        You look just like Wade Watts' famous avatar, Parzival, although I know it's actually Claire behind that headset, not Wade.
        You must be wondering why you're here, and why Wade lent you his OASIS account.
        Well, the fact is, before the real me passed away, he created a special version of the game ZORK!, right here in the OASIS.
        ZORK! is a classic text-based video game, where players like you type commands into the prompt to explore the world, solve puzzles, and have adventures.
        In this version of ZORK!, I've modified the game and hidden a special easter egg inside for any gunter clever enough to find it.
        I think you'll find the easter egg super helpful to the quest you're currently on, so get cracking!
        You can come talk to me again if you need help understanding how to play the game.
        Good luck!'
        """
        self.help_conversation = """
        'Hah!' The wizard laughs. 
        'I figured you'd be back for help sooner or later, I've devised a real doosy of a challenge, here.'
        He looks more serious. 'Well, the clock is ticking, so here's some advice to help you:
        To move around the game world, you can type in direction commands, like 'walk north' or 'go south.'
        Sometimes there are doors or objects you want to get inside of that are shut, trying commanding them to 'open!' There's that mailbox nearby that might have something inside...
        You can also pick up many items you find around in the environment - try i on the... thing you might find in the mailbox!

        Hmph, well, that should be enough to get you going. Text adventure games are all about exploration and trying out different commands, so, get to experimenting!'
        """
        self.attack_conversation = """Your pitiful attack has no effect whatsoever on Anorak's mighty form.
        He moves his hands in mysterious circular motions and a gigantic fireball swells into the space between you, engulfing you and everything else around.
        Anorak throws his hands wide and sends the fireball - and your avatar - spinning across the field, where you come crashing down in a pile, your health nearly gone.
        You get unsteadily to your feet and gulp down one of your dwindling health potions.
        Anorak laughs, 'Hah! Best not be trying that again, little one!"""

    def speak(self):
        if not self.spoken:
            print(self.initial_conversation)
            self.spoken = True
            return
        else:
            print(self.help_conversation)
            return

    def attack(self):
        print(self.attack_conversation)
        return
            
class Exit():
    def __init__(self, direction, destination, closed=True, gate=None):
        self.gate = gate
        self.direction = direction
        self.destination = destination
        self.closed = closed
    
    def open(self):
        self.closed = False
        print(f"You open the {self.gate}")

    def close(self):
        self.closed = True
        print(f"You close the {self.gate}")


class Player:
    def __init__(self, inventory = []):
        self.inventory = inventory

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def get_item_by_name(self, name):
        for item in self.inventory:
            if item.name == name:
                return item
        return None
    

def main():
    anorak = Anorak("anorak","A tall wizard in black robes who looks like an older, more handomse version of James Halliday, creator of the OASIS.")
    leaflet = Item("leaflet", "Welcome to Zork!")
    mailbox = Item("mailbox", "A nice mailbox", [leaflet], False, True, True)
    rooms = {
        "West of House": Room(
            "You are standing in an open field west of a white house, with a boarded front door.\nThere is a small mailbox here.\nA figure dressed in dark robes leans casually against the mailbox and beckons you over.",
            "You are standing in an open field west of a white house, with a boarded front door.\nThere is a small mailbox here.\nAnorak leans casually against the mailbox.",
            [
            Exit("north", "North of House",True,"window"),
            Exit("south", "South of House",False,"wall")
        ],
        [mailbox, anorak]
        ),
        "North of House": Room(
            "You are facing the north side of a white house. There is no door here, and all the windows are boarded up.",
             "You are facing the north side of a white house. There is no door here, and all the windows are boarded up.", [
            Exit("west", "West of House",False)
        ]),
        "South of House": Room(
            "You are facing the south side of a white house.",
             "You are facing the south side of a white house.",
              [
            Exit("west", "West of House",False),
        ])
    }
    
    
    print("Ready Player One")
    input("Press enter to start...")

    print("\n")
    print("ZORK I: The Great Underground Empire")
    print("Copyright (c) 1981, 1982, 1983 Infocom, Inc. All rights reserved.")
    print("ZORK is a registered trademark of Infocom, Inc.")
    print("Revision 88 / Serial number 840726")
    print("\n")
    print("West of House")
    
    game = Game(rooms)
    
        

if __name__ == "__main__":
    main()