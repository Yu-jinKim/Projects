""" Monopoly

Implementation of Monopoly game kinda
"""

from random import randint

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
        self.name = name
        self.balance = 1500
        self.position = 0
        self.possessions = []
        self.in_jail = False

    def __str__(self):
        return self.name

    def get_status(self):
        return f"{self.name}:\n- Moneyz: {self.balance}\n- Position on the board: {self.position}\n- Possessions: {self.possessions}"

    def get_balance(self):
        return self.balance

    def move(self, dice_amount):
        self.position += dice_amount
        
        if self.position >= 40:
            self.position -= 40

        print(f"You rolled: {dice_amount}")
        print(f"You are now at the position {self.position}")
        return self.position

    def add_possession(self, land, amount):
        self.balance -= amount
        self.possessions.append(land)
        print(f"You paid {amount} for {land}")
        print(f"you now have these properties: {self.possessions}")

    def remove_possession(self, land, amount):
        self.balance += amount
        self.possessions.remove(land)
        print(f"You removed {amount} for {land}")
        print(f"you now have these properties: {self.possessions}")

    def get_possessions(self):
        return self.possessions

    def pay(self, amount):
        self.balance -= amount
        return self.balance

    def receive(self, amount):
        self.balance += amount
        return self.balance

    def go_to_jail(self, going):
        self.in_jail = going

    def in_jail(self):
        return self.in_jail


def check_if_owned(players: list, land):
    for player in players:
        owned_lands = player.get_possessions()

        if land in owned_lands:
            return True, player

    return False, None


def check_position(players, player, position):
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
            print(f"{player} has now {player_balance} and {owner} has now {owner_balance}")
        else:
            buy = input("Buy? (y/n) ")

            if buy:
                player_balance = player.get_balance()
                if player_balance >= price:
                    player.add_possession(land, price)
                    print(f"You now own {land}")
                else:
                    print(f"You don't have enough money for {land}: {player_balance} <= {price}")
                
    elif position in SPECIAL_CASES:
        if SPECIAL_CASES[position] == "Go to jail":
            player.go_to_jail()
        elif SPECIAL_CASES[position] == "Free Parking":
            player.receive(FREE_PARKING)
            FREE_PARKING = 0
        elif SPECIAL_CASES[position] == "Start":
            player.receive(SPECIAL_CASES[position]["Start"])
        elif SPECIAL_CASES[position] == "Income Tax":
            pay_taxes(player, SPECIAL_CASES[position]["Income Tax"])
        elif SPECIAL_CASES[position] == "Super Tax":
            pay_taxes(player, SPECIAL_CASES[position]["Super Tax"])

    elif position in CHANCES:
        pass

    elif position in COMMUNITY_CHESTS:
        pass

    print("Next turn\n")


def pay_taxes(player, amount):
    player.pay(amount)
    FREE_PARKING += amount


def main():
    nb_players = input("How many players? ")
    names_of_players = []

    try:
        nb_players = int(nb_players)
    except Exception as e:
        print(f"Something wrong in the nb of players: {e}")
        return -1

    for i in range(nb_players):
        name = input(f"Name of player {i+1} ? ")
        names_of_players.append(name)

    players = [Player(name) for name in names_of_players]

    print("\nGame is starting")

    while True:
        for player in players:
            print(f"Turn of {player.get_status()}")
            input("Press enter to roll...")
            dice_amount = randint(1, 6) + randint(1, 6)
            new_position = player.move(dice_amount)
            check_position(players, player, new_position)


if __name__ == "__main__":
    main()
