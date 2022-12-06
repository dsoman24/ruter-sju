# Ruter Sju Bot

import random
import time
import os
import copy

from card import *
from hand import *
from deck import *
from human import *
from bot import *

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def gamestate_str(gamestate):
    """returns a string representation of a gamestate"""
    normal_suits = ["diamonds", "spades", "hearts", "clubs"]

    rows = ""
    for suit in gamestate:
        if suit in range(4):
            suit_str = normal_suits[suit]
        else:
            suit_str = str(suit)
        row = suit_str + ": "
        if gamestate[suit]["under"]:
            row += str(gamestate[suit]["under"][-1].number) + " "
        if gamestate[suit]["center"]:
            row += str(gamestate[suit]["center"][-1].number) + " "
        if gamestate[suit]["over"]:
            row += str(gamestate[suit]["over"][-1].number)
        rows += row + "\n"
    return rows

def parse_hand(filename):
    """Parses csv file containing the hand. Rows in the form number,suit"""
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    hand = []
    for line in lines:
        line = line.strip().split(",")
        suit = int(line[1])
        number = int(line[0])
        hand.append(Card(suit, number))
    return hand

class Game:
    def __init__(self, players, bothands = [], numSuits = 4, cardsPerSuit = 13, delay = 0, withRealCards = False): # numPlayers (int)
        self.players = players
        self.withRealCards = withRealCards
        for player in self.players:
            if isinstance(player, Human):
                self.withRealCards = True
                break

        self.numPlayers = len(players)
        self.numSuits = numSuits
        self.cardsPerSuit = cardsPerSuit
        self.card_deck = Deck(self.numSuits, self.cardsPerSuit)
        self.numCards = len(self.card_deck)
        self.delay = delay
        self.counts = [0 for j in range(self.numPlayers)] # counts of how many cards are dealt
        self.center = (self.cardsPerSuit+1)//2 # default 7
        self.data = {
            "players":self.players,
            "numPlayers":self.numPlayers,
            "numSuits":self.numSuits,
            "cardsPerSuit":self.cardsPerSuit,
            "numCards":self.numCards,
            "botHands":bothands, # if playing with real players, enter in hands of bots manually here. Can be parsed from csv file
            "winOrder":[],
            "playOrder":[],
            "allMoves":{},
            "turns":0, # if a player is holding a block this counts as a turn. Placing multiple cards in one go due to low/high cards counts as 1 turn.
            "rounds":0,
            "handsPerRound":{}, # hands per round mapped to player name
            "gameStates":[] # all gamestates per turn
            }

        self.game = {} # keeps track of the games.
        for suit in range(self.numSuits):
            self.game[suit] = {"under": [], "center":[], "over": []}

    def __len__(self):
        total = 0
        for cards in self.game.values():
            total += len(cards["under"]) + len(cards["over"])+len(cards["over"])
        return total # how many cards are in play

    def __str__(self):
        return gamestate_str(self.game)

    def shuffle_deck(self):
        random.shuffle(self.card_deck.deck)

    def deal(self, hands = []):
        i = 0
        dealt = self.numCards
        while dealt > 0:
            self.players[i].cards_given += 1
            dealt -= 1
            i = (i+1)%self.numPlayers
        if not self.withRealCards:
            i = 0
            while len(self.card_deck.deck) > 0:
                self.players[i].hand.give(self.card_deck.deck.pop())
                i = (i+1)%self.numPlayers
        else:
            for i in range(len(self.players)):
                if isinstance(self.players[i], Bot):
                    self.players[i].hand.force_hand(cards = hands.pop(0))
                else:
                    self.players[i].hand.force_hand(cards =[Card(-(self.numSuits+1),-(self.cardsPerSuit+1)) for x in range(self.players[i].cards_given)]) # empty hands to unknown real player

    def show(self, which):
        """
        Shows the current game state
        """
        print(f"{self.players[which].name}:")
        if isinstance(self.players[which], Bot):
            print("CARDS")
            print(self.players[which].hand)
        print("GAME")
        print(self)

    def undo(self): # enter -1 -1 human input to undo
        pass # figure out how to "undo"

    def ruter_sju(self):
        """
        Plays ruter-sju. Returns a dictionary of all game data
        """

        self.shuffle_deck()
        self.deal(hands = self.data["botHands"])

        for i in range(len(self.players)):
            if isinstance(self.players[i], Bot):
                if 0 in self.players[i].hand.cards:
                    if Card(0, self.center) in self.players[i].hand.cards[0]:
                        break
        else:
            i = int(input("Which player starts?: ")) # this is done manually, makes sense for now

        starting_player = i
        blocked = None

        turn = 0
        while len(self.data["winOrder"]) < self.numPlayers:
            if self.players[i].name not in self.data["winOrder"]:
                self.data["turns"] += 1
                if self.players[i].name in self.data["handsPerRound"]:
                    self.data["handsPerRound"][self.players[i].name].append(copy.deepcopy(self.players[i].hand))
                else:
                    self.data["handsPerRound"][self.players[i].name] = [copy.deepcopy(self.players[i].hand)]
                if blocked == i and len(self.data["winOrder"]) == self.numPlayers - 1:
                    blocked = None
                if blocked != i:
                    self.show(i)
                    times = 0
                    m = "again" # 3 is place another condition, 0 is block condition, 1 is continue condition, 2 is out condition
                    while m == "again":
                        m = self.players[i].move(gamestate = self)
                        if m == "block":
                            text = f"takes block"
                            if self.data["rounds"] in self.players[i].hand.moves:
                                self.players[i].hand.moves[self.data["rounds"]].append(text)
                            else:
                                self.players[i].hand.moves[self.data["rounds"]] = [text]
                        times += 1
                    if m == "block" and times == 1:
                        blocked = i
                    if m == "out":
                        self.data["winOrder"].append(self.players[i].name)
                else:
                    text = f"{self.players[i].name} is blocked..."
                    print(text+"\n")
                    text = f"blocked"
                    if self.data["rounds"] in self.players[i].hand.moves:
                        self.players[i].hand.moves[self.data["rounds"]].append(text)
                    else:
                        self.players[i].hand.moves[self.data["rounds"]] = [text]
                self.data["gameStates"].append(copy.deepcopy(self.game))
                time.sleep(self.delay)
            turn += 1
            if turn == self.numPlayers-len(self.data["winOrder"]):
                turn = 0
                self.data["rounds"] += 1
            i = (i+1)%self.numPlayers
            # clearConsole()
        print("GAME OVER")
        print(self)
        print("Final Order:")
        for index, name in enumerate(self.data["winOrder"]):
            print(f"{index+1}. {name}")
        for j in range(self.numPlayers):
            if isinstance(self.players[j], Human):
                self.players[j].hand.match_placed(self.numSuits)
            player_index = (starting_player+j)%self.numPlayers
            self.data["allMoves"][self.players[player_index].name] = self.players[player_index].hand.moves
            self.data["playOrder"].append(self.players[player_index].name)
        return self.data
