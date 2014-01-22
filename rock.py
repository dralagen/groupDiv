#!/usr/bin/env python2.7
#0 - rock
#1 - Spock
#2 - paper
#3 - lizard
#4 - scissors

def name_to_number(name):
    number = ''
    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    else:
        number = 4
    return number

def number_to_name(num):
    string = ''
    if num == 0:
        string = "rock"
    elif num == 1:
        string = "Spock"
    elif num == 2:
        string = "paper"
    elif num == 3:
        string = "lizard"
    else:
        string = "scissors"
    return string

#Build the first part of the main function rpsls(guess) that converts guess into the number player_number between 0 and 4 using the helper function name_to_number.
def rpsls(guess):
    import random
    player_number = name_to_number(guess)
    
#Build the second part of rpsls(guess) that generates a random number comp_number between 0 and 4 using the function random.randrange(). I suggest experimenting with randrange in a separate CodeSkulptor window before deciding on how to call it to make sure that you do not accidently generate numbers in the wrong range.

    comp_number = random.randrange(0, 5)

#Build the last part of rpsls(guess) that determines and prints out the winner. This test is actually very simple if you apply modular arithmetic (% in Python) to the difference between comp_number and player_number. If this is not immediately obvious to you, I would suggest reviewing our discussion of remainder / modular arithmetic and experimenting with the remainder operator % in a separate CodeSkulptor window to understand its behavior.

    winner = (comp_number - player_number) % 5

#Using the helper function number_to_name, you should produce four print statements; print a blank line, print out the player's choice, print out the computer's choice and print out the winner.

    print ""
    print "Player chooses " + number_to_name(player_number)
    print "Computer chooses " + number_to_name(comp_number)
    if winner == 1 or winner == 2:
        print "Computer wins!"
    elif winner == 0:
        print "Player and computer tie!"
    else:
        print "Player wins!"


# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric
