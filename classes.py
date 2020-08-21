from enum import Enum
from enum import IntEnum
from random import sample
import numpy as np
import functools
import operator



class Card(IntEnum):
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

class Suit(Enum):
    DIAMONDS = 'diamond'
    SPADES = 'spades'
    CLUBS = 'clubs'
    HEARTS = 'hearts'
    

class PlayingCard:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return str(self.value.name) + " of " + self.suit.value

    def __repr__(self):
        return str(self.value.name) + " of " + self.suit.value
    
    def __eq__(self, other):
        if self.value == other.value and self.suit == other.suit:
            return True
        else:
            return False


class Player:
    def __init__(self, hand, name):
        self.name = name
        self.pile = np.empty(0)
        self.hand = hand
        self.points = 0
        self.matchpoints = 0
    def __str__(self):
       return self.name 
       #return "pile:" + str(self.pile) + ", hand:" + str(self.hand) + ", points: " + str(self.points)

    def __repr__(self):
       return self.name
       #return "pile:" + str(self.pile) + ", hand:" + str(self.hand) + ", points: " + str(self.points)


#makes deck for 4 player game
def make_deck4():
    full_deck = []
    for suit in Suit:
        for card in Card:
            full_deck.append(PlayingCard(Card(card), Suit(suit)))
    return np.asarray(full_deck)

#makes deck for 3 player game
def make_deck3():
    full_deck = []
    for suit in Suit:
        for card in Card:
            full_deck.append(PlayingCard(Card(card), Suit(suit)))
    full_deck.pop(0)
    return np.asarray(full_deck)

def shuffle_deck(deck, num_player):
    if num_player == 4:
         deck = sample(list(deck), 52)
    else:
         deck = sample(list(deck), 51)
    return deck


def twoc (players_list):
    lista = []
    twocs = PlayingCard(Card(2), Suit('clubs'))
    for player in players_list:
        if twocs in player.hand:
            lista.append(True)
        else:
            lista.append(False)
    return lista

def handPrint(hand):
    for i in range(len(hand)):
        print('['+ str(i) + '], ', hand[i])

def handSort(hand):
    sorted_suit = [[],[],[],[]]
    hand = list(hand)
    hand.sort(key = lambda x: x.suit.value)
    current_suit = ''
    current_index = -1
    for i in range(len(hand)):
        if current_suit != hand[i].suit.value:
            current_suit = hand[i].suit.value
            current_index = current_index + 1
        sorted_suit[current_index].append(hand[i]) 
    for i in range(4):
        sorted_suit[i].sort(key = lambda y: y.value.value)
    hand = functools.reduce(operator.iconcat, sorted_suit, [])
    return np.asarray(hand)




    
    