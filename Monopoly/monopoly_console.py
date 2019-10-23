""" Monopoly

Implementation of Monopoly game kinda
"""

from random import randint
import sys

PROPERTIES = {
    1: {"Old Kent Road": {"Rent": 2, "Price": 60}},
    3: {"Whitechapel Road": {"Rent": 4, "Price": 80}},
    5: {"King's Cross station": {"Rent": 25, "Price": 200}},
    6: {"The Angel Islington": {"Rent": 6, "Price": 100}},
    8: {"Euston Road": {"Rent": 6, "Price": 100}},
    9: {"Pentonville Road": {"Rent": 8, "Price": 120}},
    11: {"Pall Mall": {"Rent": 10, "Price": 140}},
    12: {"Electric Company": {"Rent": 1, "Price": 150}},
    13: {"Whitehall": {"Rent": 10, "Price": 140}},
    14: {"Northumberland Avenue": {"Rent": 12, "Price": 160}},
    15: {"Marylebine station": {"Rent": 25, "Price": 200}},
    16: {"Bow Street": {"Rent": 14, "Price": 180}},
    18: {"Marlborough Street": {"Rent": 14, "Price": 180}},
    19: {"Vine Street": {"Rent": 16, "Price": 200}},
    21: {"Strand": {"Rent": 18, "Price": 220}},
    23: {"Fleet Street": {"Rent": 18, "Price": 220}},
    24: {"Trafalgar Square": {"Rent": 20, "Price": 240}},
    25: {"Fenchurch Street station": {"Rent": 25, "Price": 200}},
    26: {"Leicester Square": {"Rent": 22, "Price": 260}},
    27: {"Coventry Street": {"Rent": 22, "Price": 260}},
    28: {"Water Works": {"Rent": 1, "Price": 150}},
    29: {"Piccadilly": {"Rent": 24, "Price": 280}},
    31: {"Regent Street": {"Rent": 26, "Price": 300}},
    32: {"Oxford Street": {"Rent": 26, "Price": 300}},
    34: {"Bond Street": {"Rent": 28, "Price": 320}},
    35: {"Liverpool Street station": {"Rent": 25, "Price": 200}},
    37: {"Park Lane": {"Rent": 35, "Price": 350}},
    39: {"Mayfair": {"Rent": 50, "Price": 400}}
}

SPECIAL_CASES = {
    0: {"Start": 200},
    4: {"Income Tax": 200},
    10: {"Visit Jail": 0},
    20: {"Free Parking": 0},
    30: {"Go to jail": None},
    38: {"Super Tax": 100}
}

CHANCES = [7, 22, 36]

COMMUNITY_CHESTS = [2, 17, 33]

FREE_PARKING = 0


class Player:
    def __init__(self, name):
        """ Setup the player """
        self.name = name
        self.balance = 1500
        self.position = 0
        self.possessions = []
        self.in_jail = 0

    def __str__(self):
        return self.name

    def get_status(self):
        return (f"{self.name}:\n"
                f"- Moneyz: {self.balance}\n"
                f"- Position on the board: {self.position}\n"
                f"- Possessions: {self.possessions}"
                f"- In jail?: {self.in_jail}")

    def get_balance(self):
        return self.balance

    def move(self, dice_amount):
        """ Move the player (take into account the board is a circle)"""
        self.position += dice_amount

        if self.position >= 40:
            self.position -= 40

            if self.position == 0:
                self.balance += 400
                print("You landed on the Go tile, lucky: "
                      f"{self.balance - 400} --> {self.balance}")
            else:
                self.balance += 200
                print("You passed through the Go tile "
                      f"{self.balance - 200} --> {self.balance}")

        return self.position

    def get_possessions(self):
        return self.possessions

    def get_jail_status(self):
        return self.in_jail

    def add_possession(self, land, amount):
        self.balance -= amount
        self.possessions.append(land)
        print(f"You paid {amount} for {land}")
        print(f"you now have these properties: {self.get_possessions()}")

    def remove_possession(self, land, amount):
        self.balance += amount
        self.possessions.remove(land)
        print(f"You removed {land} for {amount}")
        print(f"you now have these properties: {self.possessions}")

    def pay(self, amount):
        self.balance -= amount
        return self.balance

    def receive(self, amount):
        self.balance += amount
        return self.balance

    def go_to_jail(self):
        self.in_jail = 3
        self.position = 10

    def out_of_jail(self):
        self.in_jail = 0

    def turn_passing(self):
        self.in_jail -= 1


def check_if_owned(players: list, land):
    """ check if the land is owned
    Args:
    - list of players
    - land
    Returns:
    - bool (is land owned)
    - owner (player)
    """

    for player in players:
        owned_lands = player.get_possessions()

        if land in owned_lands:
            return True, player

    return False, None


def check_position(players, player, position):
    """ check the position of the player

    Do the right thing according to the tile the player landed on

    Args:
    - list of players
    - current player
    - position
    """

    if position in PROPERTIES:
        land = list(PROPERTIES[position].keys())[0]
        price = PROPERTIES[position][land]["Price"]
        rent = PROPERTIES[position][land]["Rent"]
        owned, owner = check_if_owned(players, land)
        print(f"You landed on {land}")

        if owned:
            print(f"You owe {owner} {rent}")
            player_balance = player.pay(rent)
            owner_balance = owner.receive(rent)
            print((f"{player} has now {player_balance} "
                   f"and {owner} has now {owner_balance}"))
        else:
            buy = input("Buy? (y/n) ")

            if buy:
                player_balance = player.get_balance()

                if player_balance >= price:
                    player.add_possession(land, price)
                else:
                    print(("You don't have enough money for "
                           f"{land}: {player_balance} <= {price}"))

    elif position in SPECIAL_CASES:
        case = list(PROPERTIES[position].keys())[0]
        print(f"You landed on {case}")

        if case == "Go to jail":
            player.go_to_jail()
        elif case == "Free Parking":
            player.receive(FREE_PARKING)
            FREE_PARKING = 0
        elif case == "Start":
            player.receive(case["Start"])
        elif case == "Income Tax":
            pay_taxes(player, case["Income Tax"])
        elif case == "Super Tax":
            pay_taxes(player, case["Super Tax"])

    elif position in CHANCES:
        print("You landed on a Chance")

    elif position in COMMUNITY_CHESTS:
        print("You landed on a Community Chest")


def check_if_bankrupt(player):
    """ check if the player goes bankrupt

    Check the player's possession to see if i can not go bankrupt

    Args:
    - player
    Returns:
    - bool
    """

    if player.get_balance() <= 0:
        possible_mortgages = {}
        player_possessions = player.get_possessions()

        for land in player_possessions:
            land_values = PROPERTIES.values()

            for land_value in land_values:
                if land in land_value:
                    possible_mortgages[land] = land_value[land]["Price"] / 2

        if player.get_balance() + sum(possible_mortgages.values()) < 0:
            print("You're bankrupt")
            return True

        print(f"You're possibly bankrupt: {player.get_balance()}")
        print("Here are your possible mortgages:")

        for mortgage in possible_mortgages:
            print(f" - {mortgage}: {possible_mortgages[mortgage]}")

        mortgage = input("Do you want to mortgage your house? (Y/N) ").upper()

        if mortgage == "Y":
            while player.get_balance() <= 0:
                mortgaged_property = input(
                    "Which property do you want to mortgage? "
                ).capitalize()

                if mortgaged_property in possible_mortgages:
                    player.remove_possession(
                        mortgaged_property,
                        possible_mortgages[mortgaged_property]
                    )

            return False

        else:
            print("You decided to be bankrupt")
            return True

    else:
        return False


def roll():
    """ roll 2 dice """
    die1 = randint(1, 6)
    die2 = randint(1, 6)
    # print(f"You rolled {die1} and {die2}")
    return (die1, die2)


def pay_taxes(player, amount):
    """ special cases for taxes tiles """
    player.pay(amount)
    FREE_PARKING += amount


def main():
    """ play the game """
    nb_players = input("How many players? ")
    names_of_players = []

    try:
        nb_players = int(nb_players)
    except Exception as e:
        print(f"Something wrong in the nb of players: {e}")
        return -1

    if nb_players > 6:
        print("Too many players")
        sys.exit()

    for i in range(nb_players):
        name = input(f"Name of player {i+1} ? ")
        names_of_players.append(name)

    players = [Player(name) for name in names_of_players]
    rolls = []

    for player in players:
        rolls.append(roll())

    rolls_players = sorted(set(zip(rolls, players)), key=lambda x: -x[0])
    ordered_players = [player[1] for player in rolls_players]

    print("\nGame is starting")

    while True:
        for player in ordered_players:
            doubles = 0

            while True:
                print(f"Turn of {player.get_status()}")
                input("Press enter to roll...")
                die1, die2 = roll()

                if player.get_jail_status() != 0:
                    print(f"{player} is in prison: "
                          f"{player.get_jail_status()} turn(s) left")

                    if die1 == die2:
                        player.out_of_jail()
                        print("You are free")
                    else:
                        player.turn_passing()
                        print("Tough luck")

                    break

                else:
                    if die1 == die2:
                        doubles += 1

                        if doubles == 3:
                            player.go_to_jail()
                            break

                    dice_amount = sum(die1, die2)
                    new_position = player.move(dice_amount)
                    check_position(players, player, new_position)
                    print("Next turn\n")

                    if doubles == 0:
                        break

        for player in ordered_players:
            bankrupt = check_if_bankrupt(player)

            if bankrupt:
                ordered_players.remove(player)

        if len(ordered_players) == 1:
            print(f"{ordered_players[0]} is the winner !")
            break
        elif len(ordered_players) == 0:
            print("Savages")
            break


if __name__ == "__main__":
    main()
