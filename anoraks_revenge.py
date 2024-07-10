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
            elif word in self.object_list and obj is None:
                obj = word

        # Compile a valid command based on the given logic
        if action == "move" and direction:
            return {"type": "move", "direction": direction}
        elif direction and not action:
            return {"type": "move", "direction": direction}
        elif action in ["take", "drop", "use"] and obj:
            return {"type": action, "object": obj}
        else:
            return {"error": "Invalid command"}

def main():
    interpreter = InputInterpreter()

    
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
        print(command)

if __name__ == "__main__":
    main()