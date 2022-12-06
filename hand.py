from card import *
import copy
class Hand:
    def __init__(self):
        self.cards = {} # sorted deck by suit {0: [cards], 1:[cards], ...}
        self.cards_placed = []
        self.moves = {}

    def give(self, card): # card (Card). gives card to cards dict
        if card.suit in self.cards:
            self.cards[card.suit].append(card)
        else:
            self.cards[card.suit] = [card]
        self.cards[card.suit].sort()

    def __len__(self):
        length = 0 # how many cards are in a hand
        for suit_list in self.cards.values():
            length += len(suit_list)
        return length

    def __str__(self):
        """string representation of current hand"""
        hand_str = ""
        cards_list = []
        for suit_list in self.cards.values():
            cards_list += suit_list
        for i in range(len(self)):
            hand_str += cards_list[i].__str__()
            if i != len(self) - 1:
                hand_str += ", "
        return hand_str

    def remove_card(self, card): # removes card from hand to be placed in game, takes in Card object
        which_index = self.cards[card.suit].index(card)
        del self.cards[card.suit][which_index]

    def force_hand(self, cards):
        for card in cards:
            self.give(card)
        
    def match_placed(self, numSuits): # call at the end of the game for each real player with unknown hand
        del self.cards[-(numSuits+1)]
        for card in self.cards_placed:
            self.give(card)