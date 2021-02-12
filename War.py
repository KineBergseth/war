"""
How to play: War

The goal is to be the first player to win all 52 cards

The deck is divided evenly, with each player receiving 26 cards
Each player turns up a card at the same time
The player with the higher card takes both cards and puts them on the bottom of his stack
If the cards are the same rank, it is War
Each player turns up two card face down and one card face up
The player with the higher cards takes both piles
If the turned-up cards are again the same rank, there is another war
The player with the higher card takes all cards
*If you don't have enough cards to complete the war, you lose.

The game ends when one player has won all the cards.
"""

import random
import Queue
import sys
from enum import Enum
from typing import NoReturn


class Suit(Enum):
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"

    def __str__(self) -> str:
        return self.value


class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self) -> str:
        if self is Rank.JACK:
            return "J"
        elif self is Rank.QUEEN:
            return "Q"
        elif self is Rank.KING:
            return "K"
        elif self is Rank.ACE:
            return "A"
        else:
            return str(self.value)

    # rich comparisons https://www.python.org/dev/peps/pep-0207/
    # needed in order to compare two instances
    def __gt__(self, other: "Rank") -> bool:
        return self.value > other.value

    def __lt__(self, other: "Rank") -> bool:
        return self.value < other.value


class Card:

    def __init__(self, suit=0, rank=0):
        self.suit = suit
        self.rank = rank

    def show(self) -> NoReturn:
        print(f'{self.rank}{self.suit}')


def create_shuffled_deck():
    """ Creates a shuffled deck of 52 cards """
    deck = [(suit, rank) for suit in Suit for rank in Rank]
    random.shuffle(deck)  # shuffle the deck
    return deck


class War:

    def __init__(self):
        self.deck = create_shuffled_deck()
        self.queues = self.deal_cards()

    def deal_cards(self):
        """
        Split cards between players, give them a card deck containing 26 cards each
        Returns a list of 2 card decks (queues)
        """
        output = []
        player = Queue.Queue('player')  # set owner of queue to player
        computer = Queue.Queue('computer')  # set owner of queue to computer

        # split deck into two queues
        for i in range(0, int(len(self.deck) / 2)):
            player.enqueue(self.deck.pop())
            computer.enqueue(self.deck.pop())

        output.append(player)
        output.append(computer)
        return output

    def get_top_cards(self):
        """
        Gets the top card of both players queue
        :return: top card for both players
        """
        player_card = self.queues[0].dequeue()
        computer_card = self.queues[1].dequeue()
        return player_card, computer_card

    def play_round(self) -> NoReturn:
        """ Gets played cards for both players, call method to print + compare them """
        player_card, computer_card = self.get_top_cards()
        self.print_cards(player_card, computer_card)
        # put the played cards in a pot, and compare them
        card_pot = [player_card, computer_card]
        self.compare_cards(card_pot, computer_card, player_card)

    def war_round(self, pot) -> NoReturn:
        """
        Check if player has at least three cards, then compare cards. Returns the winner and the cards in the pot
        :param pot: the cards on the table/ played by the players from the round leading to the war
        """
        card_pot = pot

        # If you don't have enough cards to complete the war, you lose. See rules defined at top
        if self.queues[0].size() < 3:
            print('\033[91m The player does not have enough cards for the war and loses the game. Congrats to the '
                  'computer! \033[0m')
            sys.exit()
        elif self.queues[1].size() < 3:
            print('\033[91m The computer does not have enough cards for the war and loses the game. Congrats to the '
                  'player! \033[0m')
            sys.exit()
        else:
            # add two secret cards from each player to the pot
            c = 0
            while c < 2:
                c += 1
                player_card, computer_card = self.get_top_cards()
                card_pot.append(player_card)
                card_pot.append(computer_card)

            # Draw a third card from the players card piles, used to determine the war
            player_card, computer_card = self.get_top_cards()

            # add the third card of both the players to the pot as well
            card_pot.append(player_card)
            card_pot.append(computer_card)

            # print cards
            self.print_war_cards(player_card, computer_card)

            # determine out who won the war round
            self.compare_cards(card_pot, computer_card, player_card)

    def compare_cards(self, card_pot, computer_card, player_card):
        """
        Compares the players and the computers cards to determine the round winner
        :param card_pot: a list of the card that are in play on the table
        :param computer_card: the card the computer has played
        :param player_card: the card the player has played
        """
        if player_card[-1] == computer_card[-1]:
            # print text to console in the color yellow
            print('\033[93m Tie! Its time for war \033[0m')
            self.war_round(card_pot)
        elif player_card[1] > computer_card[1]:
            print('The player wins the round!')
            winner = 0
            self.add_cards(card_pot, winner)
        else:
            print('The computer wins the round!')
            winner = 1
            self.add_cards(card_pot, winner)

    def add_cards(self, pot, winner) -> NoReturn:
        """
        Add cards from the pot to the winners personal card deck
        :param pot: a list of the card that are in play on the table
        :param winner: the winner of the round, indicated by the index of that players card pile in self.queues[]
        """
        for card in pot:
            self.queues[winner].enqueue(card)

    # static method is bound to a class rather than the objects for that class
    @staticmethod
    def print_cards(player, computer):
        """
        Prints both of the players card in a round visually
        Looks bad here, but trust the process. (except the card with rank 10, that messes thing up)
        :param player: the card the player has played
        :param computer: the card the computer has played
        """
        card_layout = '''
         PLAYER           COMPUTER
         _____             _____
        |{p_value}    |           |{c_value}    |
        |  {p_suit}  |           |  {c_suit}  |
        |    {p_value}|           |    {c_value}|
         ‾‾‾‾‾             ‾‾‾‾‾
        '''.format(p_suit=player[0], p_value=player[1], c_suit=computer[0], c_value=computer[1])
        print(card_layout)

    # static method is bound to a class rather than the objects for that class
    @staticmethod
    def print_war_cards(player, computer):
        """
        Prints both of the players card for the war round visually, only shows the card that determine the result
        Looks bad here, but trust the process. (except the card with rank 10, that messes thing up)
        :param player: the card the player has played
        :param computer: the card the computer has played
        """
        card_layout = '''
                PLAYER                                  COMPUTER

     _____     _____        _____            _____        _____     _____  
    |?    |   |?    |      |{p_value}    |          |{c_value}    |      |?    |   |?    |
    |  ?  |   |  ?  |      |  {p_suit}  |          |  {c_suit}  |      |  ?  |   |  ?  |
    |    ?|   |    ?|      |    {p_value}|          |    {c_value}|      |    ?|   |    ?| 
     ‾‾‾‾‾     ‾‾‾‾‾        ‾‾‾‾‾            ‾‾‾‾‾        ‾‾‾‾‾     ‾‾‾‾‾ 
        '''.format(p_suit=player[0], p_value=player[1], c_suit=computer[0], c_value=computer[1])
        print(card_layout)

    def empty_queue(self) -> bool:
        """
        Checks if any of the players have an empty queue, if so they lose the game
        :return: return true if any queues are empty, if not return false
        """
        if self.queues[0].is_empty():
            print(f'\033[94m The {self.queues[0].owner} is out of cards, and the {self.queues[1].owner} has won the '
                  f'game! \033[0m')
            return True
        elif self.queues[1].is_empty():
            print(f'\033[94m The {self.queues[1].owner} is out of cards, and the {self.queues[0].owner} has won the '
                  f'game! \033[0m')
            return True
        else:
            return False

    def simulate_game(self) -> NoReturn:
        """ Runs the game automatically without user input and simulates the game continually until it ends """
        print('Lets start a game of War!')
        while not self.empty_queue():
            self.play_round()
            # print the players card count
            for obj in game.queues:
                print(f'{obj.owner}: {obj.size()} cards left')


game = War()
game.simulate_game()

# todo print war cards? show the two secret card?
# todo, play the game with user input? press y/enter for each round? nahhh
