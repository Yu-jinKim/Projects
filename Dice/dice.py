# Project Dice

# Have a Dice roll
# Ask user which number they guess and roll

import sys, random

repeat="Y"

while repeat.upper()=="Y":
    guess=int(input("What do you guess? "))

    roll=random.randrange(1,7)

    print("Rolling...\n...\n{}".format(roll))

    if roll==guess:
        print("You guess right!")
    else:
        print("You guess wrong!")
    
    repeat=input("Play again? (Y/N) ")
    print("\n")