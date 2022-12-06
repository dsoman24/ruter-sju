from game import *

# INPUTS:

bothands_files = [parse_hand("hand0.csv"), parse_hand("hand1.csv"), parse_hand("hand2.csv"), parse_hand("hand3.csv"), parse_hand("hand4.csv")]

g = Game(
    players=[Bot("0"), Bot("1"), Bot("2"), Bot("3")], # players are put into the list in order left of the dealer. The "dealer" is always last.
    delay=0,
    bothands=bothands_files,
    withRealCards=False # True if giving hands to bots from bothands. This is overwritten to True if there is a Human in the game to avoid errors. False means that cards will be dealt automatically.
)

gamedata = g.ruter_sju()

# Suit guide
# 0 - diamonds (ruter)
# 1 - spades (spader)
# 2 - hearts (hjärter)
# 3 - clubs (klöver)

# NOTES:

# Sample Game 1 Order:
#            Real game    Simulated
# 0: Farmor      1            3
# 1: Farfar      2            1
# 2: Pappa       5            5
# 3: Daniel      4            2
# 4: Anders      3            4

# TO DO:
# Save last 3? gamestates, add feature to go back stages.
# <3 Build gamestates from steps?