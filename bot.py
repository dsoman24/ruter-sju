from hand import *
import random

class Bot:
    def __init__(self, name = "", kind = "smart"):
        self.hand = Hand()
        self.cards_given = 0
        self.name = name
        self.kind = kind # default "smart" bot. Options are smart, random, dumb

    def place(self, card, gamestate): # which (int) index of the player will place what card
        """Moves card from hand onto the gamestate"""
        self.hand.remove_card(card)
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
        if Card(0, gamestate.center) not in gamestate.game[0]["center"]:
            if 0 in self.hand.cards.keys():
                if Card(0, gamestate.center) in self.hand.cards[0]:
                    place_output = self.place(card = Card(0, gamestate.center), gamestate = gamestate)
        else:
            possible_cards = [] # find possible cards before using different algorithms to decide which to play.
            for suit, card_list in self.hand.cards.items(): # iterate through cards in hand
                if Card(suit, gamestate.center) in card_list: # if you have a center the suit is automatically possible
                    possible_cards.append(Card(suit, gamestate.center))
                elif Card(suit, gamestate.center) in gamestate.game[suit]["center"]: # if the center for that suit is in play then check if you can place above or below
                    for card in card_list:
                        if card.number == gamestate.center - 1 or card.number == gamestate.center + 1: # if you have an "opener" card it is possible
                            possible_cards.append(card)
                            # break
                        if gamestate.game[suit]["under"]:
                            if gamestate.game[suit]["under"][-1].number == card.number+1:
                                possible_cards.append(card)
                                # break
                        if gamestate.game[suit]["over"]:
                            if gamestate.game[suit]["over"][-1].number == card.number-1:
                                possible_cards.append(card)
                                # break
            if len(possible_cards) == 0:
                text = f"{self.name} takes the block..."
                print(text+"\n")
                return "block" # get block condition

            # PLAY SMART ALGORITHM BASED ON POSSIBLE CARDS
            if self.kind == "smart":
                max_distance, chosen_card = None, None
                for card in possible_cards:
                    if card.number >= gamestate.center:
                        for hand_card in self.hand.cards[card.suit]:
                            if hand_card.number >= gamestate.center:
                                distance = abs(gamestate.center-hand_card.number)
                                if (max_distance, chosen_card) == (None, None):
                                    max_distance = distance
                                    chosen_card = card
                                elif distance > max_distance:
                                    max_distance = distance
                                    chosen_card = card
                    elif card.number < gamestate.center:
                        for hand_card in self.hand.cards[card.suit]:
                            if hand_card.number < gamestate.center:
                                distance = abs(gamestate.center-hand_card.number)
                                if (max_distance, chosen_card) == (None, None):
                                    max_distance = distance
                                    chosen_card = card
                                elif distance > max_distance:
                                    max_distance = distance
                                    chosen_card = card
                    else:
                        for hand_card in self.hand.cards[card.suit]:
                            distance = abs(gamestate.center-hand_card.number)
                            if (max_distance, chosen_card) == (None, None):
                                max_distance = distance
                                chosen_card = card
                            elif distance > max_distance:
                                max_distance = distance
                                chosen_card = card
                place_output = self.place(card = chosen_card, gamestate = gamestate)

            # PLAY DUMB ALGORITHM BASED ON POSSIBLE CARDS
            elif self.kind == "dumb":
                min_distance, chosen_card = None, None
                for card in possible_cards:
                    if card.number >= gamestate.center:
                        for hand_card in self.hand.cards[card.suit]:
                            if hand_card.number >= gamestate.center:
                                distance = abs(gamestate.center-hand_card.number)
                                if (min_distance, chosen_card) == (None, None):
                                    min_distance = distance
                                    chosen_card = card
                                elif distance < min_distance:
                                    min_distance = distance
                                    chosen_card = card
                    elif card.number < gamestate.center:
                        for hand_card in self.hand.cards[card.suit]:
                            if hand_card.number < gamestate.center:
                                distance = abs(gamestate.center-hand_card.number)
                                if (min_distance, chosen_card) == (None, None):
                                    min_distance = distance
                                    chosen_card = card
                                elif distance < min_distance:
                                    min_distance = distance
                                    chosen_card = card
                    else:
                        for hand_card in self.hand.cards[card.suit]:
                            distance = abs(gamestate.center-hand_card.number)
                            if (min_distance, chosen_card) == (None, None):
                                min_distance = distance
                                chosen_card = card
                            elif distance < min_distance:
                                min_distance = distance
                                chosen_card = card
                place_output = self.place(card = chosen_card, gamestate = gamestate)

            # PLAY RANDOM ALGORITHM BASED ON POSSIBLE CARDS
            elif self.kind == "random":
                card_idx = random.randrange(0,len(possible_cards))
                chosen_card = possible_cards[card_idx]
                place_output = self.place(card = chosen_card, gamestate = gamestate)
            if place_output:
                return "out"
            if chosen_card.number == 1 or chosen_card.number == gamestate.card_deck.cardsPerSuit:
                possible_cards.pop(possible_cards.index(chosen_card))
                if len(possible_cards) > 0:
                    return "again"
            return "place"
