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
    """ Object to represent players """
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

    def get_name(self):
        return self.name


def roll():
    """ roll 2 dice """
    die1 = randint(1, 6)
    die2 = randint(1, 6)
    # print(f"You rolled {die1} and {die2}")
    return (die1, die2)


def main():
    pass


if __name__ == "__main__":
    main()