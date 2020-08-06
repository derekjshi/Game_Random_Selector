import random


# This is a random game selector from a pre-set list of common games played with an option to add additional games
class Selector:
    def __init__(self, list_of_games):
        self.list_of_games = list_of_games

    def list_print(self):
        for i in range(len(self.list_of_games)):
            print("\t", i + 1, ":", self.list_of_games[i])

    def add_item(self):
        self.list_print()
        new_input = str(input("\nProvide a game to either add to the list or remove a game from the list.\n" "Type 'ready' to have the Randomizer select a game to play!\n"))
        if len(new_input.replace(" ", "")) == 0:
            return True
        elif new_input.lower() == "ready":
            return False
        else:
            list_of_games_upper = [x.upper() for x in self.list_of_games]
            if new_input.upper() not in list_of_games_upper:
                self.list_of_games.append(new_input)
            elif new_input.upper() in list_of_games_upper:
                index = 0
                for z in range(len(list_of_games_upper)):
                    if list_of_games_upper[z] == new_input.upper():
                        index = z
                del self.list_of_games[index]
        return True

    def pick_item(self):
        print("This is the final list the game will be selected from:")
        for x in range(len(self.list_of_games)):
            print("\t", x + 1, ":", self.list_of_games[x])
        print("\nYou shall play....", self.list_of_games[random.randint(0, (len(self.list_of_games)-1))])


