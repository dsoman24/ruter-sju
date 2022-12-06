from card import *

class Deck:
    def __init__(self, numSuits = 4, cardsPerSuit = 13): # default 4 suits, 13 numbers per suit, like a normal deck.
        self.deck = []
        self.numSuits = numSuits
        self.cardsPerSuit = cardsPerSuit
        for suit in range(0, self.numSuits):
            for number in range(1, self.cardsPerSuit+1):
                self.deck.append(Card(suit, number))

    def __len__(self):
        return len(self.deck)

    def __str__(self):
        deck_str = ""
        for i in range(len(self)):
            deck_str += self.deck[i].__str__()
            if i != len(self) - 1:
                deck_str += ", "
        return deck_str
