from game import *
import sys, os

############# PARAMETERS TO CONTROL: #############

numSuits = 4 # number of suits in the game
cardsPerSuit = 13 # number of cards per suit
minNumPlayers = 3 # minimum number of players to investigate
maxNumPlayers = 6 # maximum number of players to investigate
regularGames = 5000
intelligenceStudyGames = 400
filename = "ruter-sju-data-large.csv"
##################################################


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


categories = [
    "numPlayers",
    "numSmart",
    "numDumb",
    "numRandom",
    "game",
    "turns",
    "rounds",
    "playerName",
    "kind",
    "cardsDealt",
    "roundsPlayer",
    "startingPosition",
    "finalPosition",
    "timesBlockTaken",
    "totalRoundsWithBlock",
    "totalRoundsWithBlockProp",
    "mostRoundsWithBlock",
    "mostRoundsWithBlockProp",
    "turnWithFirstBlock",
    "turnWithFirstBlockProp",
    "numCenter",
    "numOpener",
    "numExtremes"
]

header = ""
for category in categories:
    header += category + ","
for suit in range(numSuits):
    header += f",suit{suit}Extremes"
header += "\n"
# opener cards are cards directly above and below center card.
# extreme cards are cards like aces and kings in a normal deck
file = open(filename, "w")
file.write(header)
file.close()

file = open(filename, "a")

total = (maxNumPlayers-minNumPlayers+1)*(regularGames+7*intelligenceStudyGames)
progress = 0

def displayProgress(current):
    print(f"Progress: {round((current/total)*100,1)}%")

for numPlayers in range(minNumPlayers, maxNumPlayers+1):
    # Permutations for intelligence study:
    permutations = [
        {"s":numPlayers, "d":0, "r":0, "games":regularGames}, # regular game, all smart bots - for regular game analysis
        {"s":1, "d":numPlayers-1, "r":0, "games":intelligenceStudyGames}, # 1 smart, rest dumb
        {"s":numPlayers//2, "d":numPlayers-numPlayers//2, "r":0, "games":intelligenceStudyGames}, # half smart, half dumb
        {"s":1, "d":0, "r":numPlayers-1,"games":intelligenceStudyGames}, # 1 smart, rest random
        {"s":numPlayers//2, "d":0, "r":numPlayers-numPlayers//2, "games":intelligenceStudyGames}, # half smart, half random
        {"s":0, "d":1, "r":numPlayers-1, "games":intelligenceStudyGames}, # 1 dumb, rest random
        {"s":0, "d":numPlayers-1, "r":1, "games":intelligenceStudyGames}, # 1 random, rest dumb
        {"s":0, "d":numPlayers//2, "r":numPlayers-numPlayers//2, "games":intelligenceStudyGames}, # half dumb, half random
    ]
    for i, permutation in enumerate(permutations): # times is number of games played per number of players
        for times in range(permutation["games"]):
            players = []
            for s in range(permutation["s"]):
                newBot = Bot(name = str(s), kind = "smart")
                players.append(newBot)
            for d in range(permutation["d"]):
                newBot = Bot(name = str(permutation["s"]+d), kind = "dumb")
                players.append(newBot)
            for r in range(permutation["r"]):
                newBot = Bot(name = str(permutation["s"]+permutation["d"]+r), kind = "random")
                players.append(newBot)
            # initialize game with bots:
            g = Game(
                players = players,
                numSuits = numSuits,
                cardsPerSuit = cardsPerSuit
            )
            blockPrint()
            gamedata = g.ruter_sju() # play the game
            enablePrint()
            centerNumber = (gamedata["cardsPerSuit"]+1)//2
            gameDict = {gamedata["players"][i].name:{} for i in range(numPlayers)}
            for playerIndex in range(gamedata["numPlayers"]):
                playerName = gamedata["players"][playerIndex].name
                gameDict[playerName]["game"] = times
                gameDict[playerName]["numPlayers"] = numPlayers
                gameDict[playerName]["numSmart"] = permutation["s"]
                gameDict[playerName]["numDumb"] = permutation["d"]
                gameDict[playerName]["numRandom"] = permutation["r"]
                gameDict[playerName]["combinationID"] = i+1
                gameDict[playerName]["turns"] = gamedata["turns"]
                gameDict[playerName]["rounds"] = gamedata["rounds"]
                gameDict[playerName]["playerName"] = playerName
                gameDict[playerName]["kind"] = gamedata["players"][playerIndex].kind
                gameDict[playerName]["cardsDealt"] = len(gamedata["handsPerRound"][playerName][0])
                gameDict[playerName]["roundsPlayer"] = len(gamedata["allMoves"][playerName])
                gameDict[playerName]["finalPosition"] = gamedata["winOrder"].index(playerName)
                gameDict[playerName]["startingPosition"] = gamedata["playOrder"].index(playerName)
                # find times the block is taken, total rounds with block, most consecutive rounds with block:
                timesBlockTaken = 0
                totalRoundsWithBlock = 0
                mostRoundsWithBlock = 0
                turnWithFirstBlock = -1 # -1 if block never taken

                current_block_index = 0
                current_rounds_with_block = 0
                for i in gamedata["allMoves"][playerName]:
                    turn = gamedata["allMoves"][playerName][i]
                    if "takes block" in turn:
                        if turnWithFirstBlock == -1:
                            turnWithFirstBlock = i
                        current_block_index = i
                        timesBlockTaken += 1
                    if "blocked" in turn or "takes block" in turn:
                        current_rounds_with_block += 1
                        totalRoundsWithBlock += 1
                    else:
                        current_rounds_with_block = 0
                    if current_rounds_with_block > mostRoundsWithBlock:
                        mostRoundsWithBlock = current_rounds_with_block

                gameDict[playerName]["timesBlockTaken"] = timesBlockTaken
                gameDict[playerName]["turnWithFirstBlock"] = turnWithFirstBlock
                gameDict[playerName]["turnWithFirstBlockProp"] = turnWithFirstBlock/gamedata["rounds"]
                gameDict[playerName]["mostRoundsWithBlock"] = mostRoundsWithBlock
                gameDict[playerName]["mostRoundsWithBlockProp"] = mostRoundsWithBlock/gamedata["rounds"]
                gameDict[playerName]["totalRoundsWithBlock"] = totalRoundsWithBlock
                gameDict[playerName]["totalRoundsWithBlockProp"] = totalRoundsWithBlock/gamedata["rounds"]

                # find number of extreme cards, suit 0 (ace) extreme cards, number of center cards, number of lower/upper openers
                numExtremes = 0
                suitExtremes = {suit:0 for suit in range(numSuits)}
                numCenter = 0
                numOpener = 0

                playerCards = gamedata["handsPerRound"][playerName][0].cards
                cards_list = []
                for suit_list in playerCards.values():
                    cards_list += suit_list
                for card in cards_list:
                    if card.number == 1 or card.number == gamedata["cardsPerSuit"]:
                        numExtremes += 1
                        if card.suit in suitExtremes:
                            suitExtremes[card.suit] += 1
                        else:
                            suitExtremes[card.suit] = 1
                    elif card.number == centerNumber:
                        numCenter += 1
                    elif card.number == centerNumber+1 or card.number == centerNumber-1:
                        numOpener += 1

                gameDict[playerName]["numCenter"] = numCenter
                gameDict[playerName]["numOpener"] = numOpener
                gameDict[playerName]["numExtremes"] = numExtremes
                for suit in suitExtremes:
                    gameDict[playerName][f"suit{suit}Extremes"] = suitExtremes[suit]

            for player, playerData in gameDict.items():
                row = ""
                for category in header.strip().split(","):
                    row += str(playerData[category]) + ","
                row += "\n"
                file.write(row)
            clearConsole()
            progress += 1
            displayProgress(progress)
file.close()