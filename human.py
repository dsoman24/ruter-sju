from hand import *

class Human:
    def __init__(self, name = ""):
        self.hand = Hand()
        self.cards_given = 0 # when dealing remember to increment this by 1. Create alias in gamestate.data
        self.name = name
    
    def place(self, card, gamestate): # which (int) index of the player will place what card
        """Moves card from hand onto the gamestate"""
        if card.number < gamestate.center:
            gamestate.game[card.suit]["under"].append(card) # under center
        if card.number > gamestate.center:
            gamestate.game[card.suit]["over"].append(card) # equal or over center
        if card.number == gamestate.center:
            gamestate.game[card.suit]["center"].append(card)
        self.hand.cards_placed.append(card)
        condition = len(self.hand.cards_placed) == self.cards_given
        text = f"{self.name} places {card}..."
        print(text+"\n")
        if condition:
            print(f"{self.name} is out!\n")
        text = f"places {self.hand.cards_placed[-1]}"
        if gamestate.data["rounds"] in self.hand.moves:
            self.hand.moves[gamestate.data["rounds"]].append(text)
        else:
            self.hand.moves[gamestate.data["rounds"]] = [text]
        return condition

    def move(self, gamestate):
        while True:
            try:
                response = input("Which card will you place (number, suit separated by space): ").split()
                normal_suits = ["d", "s", "h", "c"]
                if response[1].lower()[0] in normal_suits:
                    suit = normal_suits.index(response[1].lower()[0])
                else:
                    suit = int(response[1])
                number = int(response[0])
            except:
                print("Enter a valid card!")
                continue
            if (suit, number) == (0, 0):
                text = f"{self.name} takes the block..."
                print(text+"\n")
                return "block"
            elif (suit, number) == (-1,-1):
                text = f"Going back to last player input..."
                print(text+"\n")
                return "undo"
            else:
                break
        p = self.place(card = Card(suit, number), gamestate = gamestate)
        if p:
            return "out"
        if number == 1 or number == gamestate.card_deck.cardsPerSuit:
            response = input("Place another? (y/n): ").lower()
            if response == "y":
                return "again"
        return "place"