class Card:
    def __init__(self, suit, number): # suit (int), number (int)
        """
        Suit ranges from 0 to 3 (default), number ranges from 1 to 13 (default). Convention if using 4 suits:
        0 - diamonds
        1 - spades
        2 - hearts
        3 - clubs
        """
        self.suit = suit
        self.number = number

    def __lt__(self, other):
        return self.number < other.number and self.suit == other.suit

    def __eq__(self, other):
        return self.number == other.number and self.suit == other.suit

    def __str__(self):
        normal_suits = ["diamonds", "spades", "hearts", "clubs"]
        if self.suit in range(4):
            suit_str = normal_suits[self.suit]
        else:
            suit_str = self.suit
        return f"{self.number} of {suit_str}"

    def __add__(self, num):
        return Card(self.suit, self.number + num)

    def __sub__(self, num):
        return Card(self.suit, self.number - num)
