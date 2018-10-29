# Project Coin flip

# Flip coin x times, do some basic stats

import random

times = int(input("How many times do you want to flip the coin? "))

nbHeads = len([i for i in range(times) if random.randrange(0,2)==1])

print("You flipped {} heads".format(nbHeads))