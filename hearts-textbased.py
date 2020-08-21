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

#sets up game and empty players
def players_init(num_player):
    players_list = []
    hand = np.empty(0)
    player1 = Player(hand, 'player1')
    players_list.append(player1)
    player2 = Player(hand, 'player2')
    players_list.append(player2)
    player3 = Player(hand, 'player3')
    players_list.append(player3)
    if num_player == 4:
        player4 = Player(hand, 'player4')
        players_list.append(player4)
    
    return np.asarray(players_list)

#deals out new hands
def init(players_list, num_player):
    deck = np.empty(4)
    if num_player == 3:
        deck = make_deck3()
    if num_player == 4:
        deck = make_deck4() 
    deck = shuffle_deck(deck, num_player)
    hands = {}  
    hand_size = int(52/num_player)
    for i in range(1, num_player + 1):
        hands['player'+ str(i)] = handSort(deck[0:hand_size])
        deck = np.delete(deck, range(hand_size))
    #print(hands)
    players_list[0].hand = np.asarray(hands['player1'])
    players_list[1].hand = np.asarray(hands['player2'])
    players_list[2].hand = np.asarray(hands['player3'])
    if num_player == 4:
        players_list[3].hand = np.asarray(hands['player4'])
    return players_list

#keeps track of status of each match, needs to be upgrades probably
def matchStatus(points, players_list):
    ongoing = 1
    for player in players_list:
        if player.matchpoints >= points:
            ongoing = 0
            print(str(player) + " loses!")
    if ongoing == 1:
        return True
    return False
    

#keeps track of status for each game
def gameStatus(players_list):
    for player in players_list:
        if player.hand.shape[0] > 0:
            return True
    return False

#returns indices of B that equal objects in A
def isMember(A, B):
    return [ np.sum(a == B) for a in A ]



#returns all indices of cards with correct suit
def suitInHand(hand, suit):
    legal_moves = []
    for i in range(hand.shape[0]):
        if (hand[i].suit.value == suit):
            legal_moves.append(i)
    return np.asarray(legal_moves)


#returns all indices of cards not in suit suit
def suitNotInHand(hand, suit):
    legal_moves = []
    for i in range(hand.shape[0]):
        if (hand[i].suit.value != suit):
            legal_moves.append(i)
    return np.asarray(legal_moves)

#decides who goes first for each round
def goesFirst(players_list):
    if lastwinner == 0:
        boolarr = twoc(players_list)
        return players_list[boolarr]
    else:
        return lastwinner

def legalMoves(hand):
    legal_moves = np.empty(0)
    global first_game
    global first_trick
    global lead_suit
    if (first_game == 0):
        index = np.where(hand == PlayingCard(Card(2),Suit('clubs')))[0][0]
        legal_moves = np.append(legal_moves, index)
        return legal_moves
    #if it is the first play of the trick
    if (first_trick == 0):
        #if hearts are broken play whatever
        if hearts_broken == True:
            return np.arange(0,hand.shape[0])
        #if hearts are not brokne but that's all you have play whatever
        if suitNotInHand(hand, 'hearts').shape[0] == 0:
            return np.arange(0,hand.shape[0])
        #if hearts are not broken and you have other suits, play those
        else:
            return suitNotInHand(hand, 'hearts')
    #if it is not the first play of the trick
    legalMoves = suitInHand(hand, lead_suit)
    #if you have cards in the lead suit play that
    if legalMoves.shape[0] > 0:
        return legalMoves
    #if you don't have cards in the lead suit play whatever
    return np.arange(0, hand.shape[0])

#still need to error proof
def passingHelp(playergive, playertake):
    handPrint(playergive.hand)
    while True:
        try:
            index1 = int(input(playergive.name +' what is the first card you would like to pass to ' + playertake.name + '? '))
            index2 = int(input(playergive.name +', what is the second card you would like to pass to ' + playertake.name + '? '))
            index3 = int(input(playergive.name +', what is the third card you would like to pass to ' + playertake.name + '? '))
            index_list = [index1, index2, index3]
            if (len(set(index_list)) != len(index_list)):
                print('You cannot choose duplicate cards, please try again')
                continue
            card1 = playergive.hand[index1]
            card2 = playergive.hand[index2]
            card3 = playergive.hand[index3]
            break
        except ValueError:
            print("Oops!  That was not a valid number.  Try again... ")
        except IndexError:
            print("Oops!  That was not a valid number.  Try again... ")
    return [card1, card2, card3]

#change passing order
def passing(players_list_wrap):
    all_passed_cards = []
    for i in range(3):
        playergive = players_list_wrap[i]
        playertake = players_list_wrap[i+1]
        print('playergive', playergive.name)
        print('playertake', playertake.name)
        givecards = passingHelp(playergive, playertake)
        all_passed_cards.append((givecards, playergive, playertake))
    print('\nall_passed_card: ', all_passed_cards)
    for transac in all_passed_cards:
        #removes passed cards from giveplayer's hand
        transac[1].hand = list(transac[1].hand)
        transac[1].hand = np.asarray([x for x in transac[1].hand if x not in transac[0]])
        print('\nafter hand removed', transac[1].hand)
        #adds cards to take players hand
        transac[2].hand = np.concatenate((transac[2].hand, np.asarray(transac[0])))
        print('\nafter hand added', transac[2].hand)
        #resorting hand after changes
        transac[2].hand = handSort(transac[2].hand)
    return np.array([all_passed_cards[0][1], all_passed_cards[1][1], all_passed_cards[2][1]])


#handles each players turn
def playerPlay(player):
    global first_trick
    global hearts_broken
    global lead_suit
    global trick_pile
    global first_game
    print('\n'+ player.name + ', It is your turn!')
    print('This is you hand:')
    handPrint(player.hand)
    legal_moves = legalMoves(player.hand)
    print('Legal Moves:', legal_moves)
    while True:
        try:
            play_card = int(input('Which card would you like to play: '))
            break
        except ValueError:
            print("Oops!  That was not a valid number.  Try again...")
    if play_card not in legal_moves:
        print('That is not a valid move!')
        playerPlay(player)
    else:
        thecard = player.hand[play_card]
        print('You played a', thecard, '!')
        tpile = np.append(trick_pile, thecard)
        trick_pile = tpile
        if first_game == 0:
            first_game = 1
        if first_trick == 0:
            lead_suit = thecard.suit.value
            print(lead_suit)
            first_trick = 1
        if hearts_broken == 0 and thecard.suit.value == 'hearts':
            hearts_broken = 1
        if hearts_broken == 0 and thecard == PlayingCard(Card(12), Suit('spades')):
            hearts_broken = 1
        player.hand = np.delete(player.hand, play_card)

def pileWin(player_pile):
    # print('player pile:', list(player_pile))
    player_pile_filtered = filter(lambda x: x[1].suit.value == lead_suit, list(player_pile))
    player_pile = list(player_pile_filtered)
    # print('player pile after filter:', list(player_pile))
    player_pile = list(player_pile)
    player_pile.sort(reverse = True, key = lambda x: x[1].value.value)
    return list(player_pile)[0][0]

def pileCount(pile):
    count = 0
    if PlayingCard(Card(12), Suit('spades')) in pile:
        count = count + 13
    pile_filtered = filter(lambda x: x.suit.value == 'hearts', pile)
    return count + len(list(pile_filtered))

def scoreCount(players_list):
    for player in players_list:
            if player.points == 26:
                moon = int(input('You shot the moon! Would you like to: [1] subtract 26 points from your score or [2] add 26 to your opponents'))
                if moon == 1:
                    player.matchpoints -= 26
                    print('You now have '+ str(player.matchpoints) + ' points.')
                    player.points = 0
                if moon == 2:
                    print('This option is not available yet, Try Again')
                    scoreCount(players_list)
                else:
                    print('Invalid choice, choose [1], [2]')
            else:
                player.matchpoints += player.points
                print(player.name + ', you now have ' + str(player.matchpoints) + ' points')
                player.points = 0

def main():
    #player who won last trick
    global lastwinner 
    lastwinner = 0
    #is it the first play of the game
    global first_game 
    first_game = 0
    #boolean first card played in the trick
    global first_trick
    first_trick = 0
    #boolean for whether or not hearts have been broken
    global hearts_broken
    hearts_broken = 0
    #the suit leading the trick
    global lead_suit
    lead_suit = ''
    #pile representing the current trick
    global trick_pile
    trick_pile = np.empty(0)
    print("Welcome to Hearts!")
    num_player = input("How many are in your game?:")
    win_points = input("How many points would you like to play to?:")
    num_player = int(num_player)
    win_points = int(win_points)
    players_list = players_init(num_player)
    #processes each match
    while(matchStatus(win_points, players_list)):
        players_list = init(players_list, num_player)
        players_list_wrap = np.concatenate((players_list, players_list))
        #processes each game
        players_list = passing(players_list_wrap)
        print(players_list)
        players_list_wrap = np.concatenate((players_list, players_list))
        while(gameStatus(players_list)):
            first = goesFirst(players_list)
            index = np.where(players_list == first)
            #processes each trick
            for i in range(index[0][0], index[0][0]+num_player):
                playerPlay(players_list_wrap[i])
            zip_piles = zip(players_list_wrap[index[0][0]:index[0][0]+num_player], trick_pile)
            player_piles = list(zip_piles)
            winner = pileWin(player_piles)
            winner.pile = np.concatenate((np.asarray(winner.pile), trick_pile), axis = None) 
            winner.points = winner.points + pileCount(trick_pile)
            print(winner.name + ', you took the pile')
            #print('You now have '+ str(winner.points) + ' points.')
            lastwinner = winner
            lead_suit = ''
            first_trick = 0
            trick_pile = np.empty(0)
            #construct piles and give the winner piles
        scoreCount(players_list)
        hearts_broken = 0
        first_game = 0
        

                    
            
               



            
            
            



    
   

if __name__ == "__main__":
    main()