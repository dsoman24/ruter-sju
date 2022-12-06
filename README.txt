Ruter Sju Bot
by Daniel Öman

Created a bot to play the Swedish card game Ruter Sju (Seven of Diamonds). 

Given a hand and a gamestate, the bot will perform the best move on the gamestate with its hand. 

A gamestate is an attribute of the Game class. It is a dictionary in the form:

{
    suit0:{"under":[], "center":[], "over":[]}
    ...
}

Cards over or equal to the center card (in a normal deck this is 7) of a given suit are 
placed in the "over" array and cards below the center card are placed in the "under" array. 

There are three bot algorithms available - "smart", "dumb", and "random"

The "smart" bot algorithm works as follows:
    1. Do nothing if it has the block. 
    2. If the starting card (7 of diamonds) hasn't been played and it is in the bot's hand, play it.
    3. Find all cards from the hand that can be possibly placed into the game. 
       This can either be a new center card, a card with 1 over the "over" pile (if it exists for the suit), 
       or 1 under the "under" pile (if it exists for the suit). If there are no possible moves it takes the block and its turn ends.
    4. Find the card that matches the suit and over-under direction that has the card in the hand farthest 
       from the center of that suit, and play it. For example, if a player has a 10 of diamonds and a possible card of 8 of diamonds,
       as well as a 13 (king) of hearts and a possible card of 8 of hearts, it would pick the 8 of hearts because 13 is 
       farther from the center than 10. 
    5. If an extreme card (ace or king) was placed, repeat steps 3-5 (place another card until chosen not to place an extreme)
     
The "dumb" bot algorithm does the opposite. On step 4, it chooses the card from the possible suit that has a card in the 
hand closest to the center.
The "random" bot chooses a random card out of its possible cards. 

Also done data analysis on thousands of games played by bots to answer many questions about the card game. 
The purpose of the data analysis is to let a player look at their cards and be able to roughly estimate if they will win.

TO DO:
- Save last several gamestates, undo feature
- what cards to winners have?
- average number of rounds per game
- bot intelligence analysis

This project was started on Dec 23, 2021.