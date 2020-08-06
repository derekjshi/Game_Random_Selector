from Randomizer import Selector


def main():
    print("Welcome to the random game selector.\n")
    print("Here is the existing list of games the Randomizer will select from:")
    # Initializes an object of class Randomizer, and sets the initial values in List_of_games
    r1 = Selector(["Valorant", "Minecraft", "Runescape", "League of Legends", "L4D2"])
    evaluator = True
    while evaluator is True:
        evaluator = r1.add_item()
    r1.pick_item()


if __name__ == "__main__":
    main()
