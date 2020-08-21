from enum import Enum
from enum import IntEnum
from random import sample
import numpy as np
import functools
import operator
import tkinter as tk
from PIL import ImageTk,Image
from functools import partial
import random 


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
    DIAMONDS = 'Diamond'
    SPADES = 'Spades'
    CLUBS = 'Clubs'
    HEARTS = 'Hearts'
    

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
    def __init__(self, hand, name, type):
        self.name = name
        self.pile = np.empty(0)
        self.hand = hand
        self.points = 0
        self.matchpoints = 0
        self.passinghand = np.empty(0)
        self.type = type
    def __str__(self):
       return self.name 
       #return "pile:" + str(self.pile) + ", hand:" + str(self.hand) + ", points: " + str(self.points)

    def __repr__(self):
       return self.name
       #return "pile:" + str(self.pile) + ", hand:" + str(self.hand) + ", points: " + str(self.points)


#makes deck for 4 player game
def make_deck4():
    global inverse_deck
    full_deck = []
    for suit in Suit:
        for card in Card:
            full_deck.append(PlayingCard(Card(card), Suit(suit)))
    inverse_deck = np.asarray(full_deck)
    return np.asarray(full_deck)

#makes deck for 3 player game
def make_deck3():
    global inverse_deck
    full_deck = []
    for suit in Suit:
        for card in Card:
            full_deck.append(PlayingCard(Card(card), Suit(suit)))
    full_deck.pop(0)
    inverse_deck = np.asarray(full_deck)
    return np.asarray(full_deck)

#shuffles deck
def shuffle_deck(deck, num_player):
    if num_player == 4:
         deck = sample(list(deck), 52)
    else:
         deck = sample(list(deck), 51)
    return deck

#find which player has the two of clubs in their hand
def twoc (players_list):
    lista = []
    twocs = PlayingCard(Card(2), Suit('Clubs'))
    for player in players_list:
        if twocs in player.hand:
            lista.append(True)
        else:
            lista.append(False)
    return lista

#sorts hands by suit and value
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
def players_init(ai_num):
    players_dict = dict()
    players_list = []
    hand = np.empty(0)
    print('num players: ', numplayers)
    print('ai player: ', ai_num)
    for i in range(ai_num):
        players_dict['ai' + str(i+1)] = Player(hand, 'ai' + str(i+1), 'ai')
        players_list.append(players_dict['ai' + str(i+1)])
    for j in range(numplayers-ai_num):
        players_dict['human' + str(j+1)] = Player(hand, 'human' + str(j+1), 'human')
        players_list.append(players_dict['human' + str(j+1)])
    random.shuffle(players_list)
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

#keeps track of status of each match
def matchStatus(players_list):
    global win_points
    ongoing = 1
    for player in players_list:
        if player.matchpoints >= win_points:
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

#determines which indices of the hand are valid moves
def legalMoves(hand):
    legal_moves = np.empty(0)
    global first_game
    global first_trick
    global lead_suit
    if (first_game == 0):
        index = np.where(hand == PlayingCard(Card(2),Suit('Clubs')))[0][0]
        legal_moves = np.append(legal_moves, index)
        return legal_moves
    #if it is the first play of the trick
    if (first_trick == 0):
        #if hearts are broken play whatever
        if hearts_broken == True:
            return np.arange(0,hand.shape[0])
        #if hearts are not brokne but that's all you have play whatever
        if suitNotInHand(hand, 'Hearts').shape[0] == 0:
            return np.arange(0,hand.shape[0])
        #if hearts are not broken and you have other suits, play those
        else:
            return suitNotInHand(hand, 'Hearts')
    #if it is not the first play of the trick
    legal_moves = suitInHand(hand, lead_suit)
    #if you have cards in the lead suit play that
    if legal_moves.shape[0] > 0:
        return legal_moves
    #if you don't have cards in the lead suit play whatever
    return np.arange(0, hand.shape[0])


#used at the end of passing, adds all passing hands to hands
def passingResolve(old_frame, new_frame):
    global players_list_wrap
    global players_list
    global option
    global players_list_index
    players_list = np.empty(0)
    for i in range(0, numplayers):
        player = players_list_wrap[i]
        player.hand = np.concatenate((player.hand, player.passinghand))
        player.hand = handSort(player.hand)
        players_list = np.append(players_list, player)
    players_list_wrap = np.concatenate((players_list, players_list))
    first = goesFirst(players_list)
    players_list_index = np.where(players_list == first)[0][0]
    option = 'play'
    aiOrHuman(old_frame, new_frame)


#cycles through players three times to ask for which cards they would like to pass
#and handles removing and adding those cards accordingly
def passing(index, old_frame, new_frame):
    global card_passing_index
    global player_passing_index
    global option
    global players_list_wrap
    print('player passing index ', player_passing_index)
    print('card passing index ', card_passing_index)
    playergive = players_list_wrap[player_passing_index]
    playertake = players_list_wrap[player_passing_index+1]
    print('playergive', playergive.name)
    print('playertake', playertake.name)
    playertake.passinghand = np.append(playertake.passinghand, playergive.hand[index])
    print('deleted card ', playergive.hand[index])
    playergive.hand = np.delete(playergive.hand, index)
    players_list_wrap[player_passing_index] = playergive
    option = 'passing'
    card_passing_index += 1
    if card_passing_index == 3:
        card_passing_index = 0
        player_passing_index+= 1
    if player_passing_index == numplayers:
        passingResolve(old_frame, new_frame)
        return 1
    old_frame.switch_frame(new_frame)
    
#determines who has won the trick
def pileWin(player_pile, lead_suit, option):
    player_pile_filtered = filter(lambda x: x[1].suit.value == lead_suit, list(player_pile))
    player_pile = list(player_pile_filtered)
    player_pile = list(player_pile)
    player_pile.sort(reverse = True, key = lambda x: x[1].value.value)
    return list(player_pile)[0][option]

#counts the points a player gains based on their pile
def pileCount(pile):
    count = 0
    if PlayingCard(Card(12), Suit('Spades')) in pile:
        count = count + 13
    pile_filtered = filter(lambda x: x.suit.value == 'Hearts', pile)
    return count + len(list(pile_filtered))

#handles scoring each player at the end of each game
def scoreCount(players_list):
    global message
    for player in players_list:
            if player.points == 26:
                player.matchpoints -= 26
                message += player.name + ', you shot the moon! You now have ' + str(player.matchpoints) + ' point!\n'
            else:
                player.matchpoints += player.points
                message += player.name + ', you now have ' + str(player.matchpoints) + ' points!\n'
                print(player.name + ', you now have ' + str(player.matchpoints) + ' points!\n')
            player.points = 0


def cardPlay(player, ind, old_frame):
    global trick_pile
    global hearts_broken
    global first_trick
    global first_game 
    global lead_suit
    global players_list
    global players_list_wrap
    global players_list_index
    global lastwinner
    global message
    global option
    global inverse_deck
    #checks if chosen card is a legal move
    legal_moves = legalMoves(player.hand)
    print('legal moves: ', legal_moves)
    if ind not in legal_moves:
        message = message + 'That is not a valid move!\n'
        old_frame.switch_frame(PagePlay)
        return 1
    thecard = player.hand[ind]
    #if it is legal adds the card to the trick pile
    tpile = np.append(trick_pile, thecard)
    trick_pile = tpile
    #changes game state variables accordingly
    if first_game == 0:
        first_game = 1
    if first_trick == 0:
        lead_suit = thecard.suit.value
        first_trick = 1
    if hearts_broken == 0 and thecard.suit.value == 'Hearts':
        hearts_broken = 1
    if hearts_broken == 0 and thecard == PlayingCard(Card(12), Suit('Spades')):
        hearts_broken = 1
    #removes played card from players hand
    inverse_deck = np.delete(inverse_deck, np.where(inverse_deck == player.hand[ind])[0][0])
    player.hand = np.delete(player.hand, ind)
    #print(inverse_deck)
    #shifts player list index, so the next time pageTwo is displayed it displays a different players hand
    players_list_index += 1
    #at the end of each trick, find the player than won the trick, changes their pile, and point total
    if trick_pile.shape[0] == numplayers:
        zip_piles = zip(players_list_wrap[players_list_index-numplayers:players_list_index], trick_pile)
        player_piles = list(zip_piles)
        winner = pileWin(player_piles, lead_suit, 0)
        message = message + winner.name + ', you took the pile'
        winner.pile = np.concatenate((np.asarray(winner.pile), trick_pile), axis = None) 
        winner.points = winner.points + pileCount(trick_pile)
        lastwinner = winner
        trick_pile = np.empty(0)
        lead_suit = ''
        first_trick = 0
        players_list_index = np.where(players_list == winner)[0][0]
    #at the end of the game, count the score, and deal cards again, and reset to passing mode
    if gameStatus(players_list) == False:
        first = goesFirst(players_list)
        players_list_index = np.where(players_list == first)[0][0]
        scoreCount(players_list)
        players_list = init(players_list, numplayers)
        hearts_broken = 0
        first_game = 0
        players_list_index = np.where(players_list == first)[0][0]
        option = 'passing'
        print('players_list_index 1: ', players_list_index)
    if matchStatus(players_list) == False:
        exit()
    aiOrHuman(old_frame, PagePlay)
    

def aiOrHuman(old_frame, new_frame):
    player = players_list_wrap[players_list_index]
    if player.type == 'human':
        old_frame.switch_frame(new_frame)
    else:
        aiPlay(player, old_frame)

def cardOpen(card):
    #opens card image based on string
    card_value = card.value.value
    card_suit_str = card.suit.value[0]
    if card_value > 10:
        img = Image.open('PNG/' + str(card.value)[5] + card_suit_str +'.png')
        img = img.resize((98,150), Image.ANTIALIAS)
        cardimg = ImageTk.PhotoImage(img)
    else:
        img = Image.open('PNG/' + str(card_value) + card_suit_str +'.png')
        img = img.resize((98,150), Image.ANTIALIAS)
        cardimg = ImageTk.PhotoImage(img)
    return cardimg

#function for displaying hand in tkinter canvas
def playerPlay(player, choice, frame_canvas, master):
    hand = player.hand
    row_counter = 4
    column_counter = 0
    for j in range(trick_pile.shape[0]):
        frame = tk.Frame(
            master=frame_canvas,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row = 1, column = 5+j)
        cardimg = cardOpen(trick_pile[j])
        lab = tk.Label(master=frame, image = cardimg, width = 98)
        lab.image = cardimg
        lab.pack()

    for i in range(hand.shape[0]):
        frame = tk.Frame(
            master=frame_canvas,
            relief=tk.RAISED,
            borderwidth=1
        )
        callback_with_args = partial(cardPlay, player, i, master)
        passing_with_args = partial(passing, i, master, PagePlay)
        column_counter+=1
        if i == 9:
            column_counter = 1
            row_counter = 5
        frame.grid(row = row_counter, column = column_counter)
        cardimg = cardOpen(hand[i])
        if choice == 'play':
            but = tk.Button(master=frame, image = cardimg, command = callback_with_args, width = 98)
        else:
            but = tk.Button(master=frame, image = cardimg, command = passing_with_args, width = 98)
        but.image = cardimg
        but.pack()
    return


def setNumPlayers(num, frame_old, frame_new):
    global numplayers
    numplayers = num
    frame_old.switch_frame(frame_new)

#sets point total and calls player play to start game
def setPointTotal(num, frame_old, frame_new):
    global win_points
    win_points = int(num)
    
    # players_list = passing(players_list_wrap)
    #frame_old.switch_frame(frame_new)
    aiOrHuman(frame_old, frame_new)
    # playerPlay(players_list_wrap[index], 'play', frame_new)

def setAiNum(ai_num, frame_old, frame_new):
    global players_list_wrap
    global players_list
    global players_list_index
    print('ai_num', ai_num)
    players_list = players_init(ai_num)
    print(players_list)
    players_list = init(players_list, numplayers)
    players_list_wrap = np.concatenate((players_list, players_list))
    first = goesFirst(players_list)
    players_list_index = np.where(players_list == first)[0][0]
    frame_old.switch_frame(frame_new)
    
def aiPlay(player, old_frame):
    #random player
    #dims = np.maximum(player.hand.max(0),inverse_deck.max(0))+1
    #local_inverse_deck = inverse_deck[~np.in1d(np.ravel_multi_index(inverse_deck.T,1),np.ravel_multi_index(player.hand.T,1))]
    # local_inverse_deck = inverse_deck[np.all(np.any((inverse_deck-player.hand[:, None]), axis=2), axis=0)]
   # local_inverse_deck = inverse_deck[~((inverse_deck[None] == player.hand).all(-1)).any(1)]
    local_inverse_deck = np.asarray([i for i in list(inverse_deck) if i not in list(player.hand)])
    random.shuffle(local_inverse_deck)
    local_players_list_wrap = players_list_wrap
    local_trick_pile = trick_pile
    local_player_index = players_list_index
    local_hand = player.hand
    best_total = 26
    local_lead_suit = lead_suit
    player_index_list = np.asarray(range(numplayers))
    player_index_list_wrap = np.concatenate((player_index_list, player_index_list))
    legal_moves = legalMoves(player.hand)
    #play_index = legal_moves[0]
    counter = 0
    #loop for each inital card
    for i in range(legal_moves.shape[0]):
        per_hand_total = 0
        #loop for tricks
        while local_hand.shape[0] != 0:
            #loop for each card played
            counter+=1
            while local_trick_pile.shape[0] != numplayers:
                if local_players_list_wrap[local_player_index] == player:
                    ai_card = local_hand[0]
                    thecard = local_hand[0]
                    local_trick_pile = np.append(local_trick_pile, local_hand[0])
                    local_hand = np.delete(local_hand, 0)
                else: 
                    thecard = local_inverse_deck[0]
                    local_trick_pile = np.append(local_trick_pile, local_inverse_deck[0])
                    local_inverse_deck = np.delete(local_inverse_deck, 0)
                if local_trick_pile.shape[0] == 1:
                    local_lead_suit = thecard.suit.value
                local_player_index+=1
            zip_piles = zip(player_index_list_wrap[local_player_index-numplayers:local_player_index], local_trick_pile)
            player_piles = list(zip_piles)
            winner = pileWin(player_piles, local_lead_suit, 1)
            print('trick pile', trick_pile)
            if winner == ai_card:
                per_hand_total += pileCount(trick_pile)
                print('perhand total', per_hand_total)   
            local_lead_suit = ''
            local_player_index = [i for i, v in enumerate(player_piles) if v[1] == winner].pop() 
            local_trick_pile = np.empty(0)
        if per_hand_total < best_total:
            best_total = per_hand_total
            play_index = int(legal_moves[i])
            
    print('play index', play_index)
    print('best_total', best_total)
    cardPlay(player, play_index, old_frame)
    # #np.random.shuffle(legal_moves)
    # index = legal_moves[0]
    # print('index: ', index)
    # cardPlay(player, int(index), old_frame)


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome to Hearts!").pack(side="top", pady=20)
        tk.Label(self, text="How many total players would you like in the game?").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="3 Players",
                  command=lambda: setNumPlayers(3, master, AiPage)).pack()
        tk.Button(self, text="4 players",
                  command=lambda: setNumPlayers(4, master, AiPage)).pack()

class AiPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome to Hearts!").pack(side="top", pady=20)
        tk.Label(self, text="How many human players would you like in the game?").pack(side="top", fill="x", pady=10)
        for i in range(numplayers):
            ai_num = numplayers-i-1
            callback_with_args = partial(setAiNum, ai_num, master, PageOne)
            print('ainum: ',ai_num)
            print('i: ', i)
            tk.Button(self, text = str(i+1)  + ' human(s)', command=callback_with_args).pack(pady = 2)
        tk.Button(self, text="Back", command=lambda: master.switch_frame(StartPage)).pack()


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text='How many points would you like to play to?').pack()
        pointtotal_entry = tk.Entry(self)
        pointtotal_entry.pack()
        tk.Button(self, text='Submit', command=lambda:setPointTotal(pointtotal_entry.get(), master, PagePlay)).pack()
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(AiPage)).pack()

class handShow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()    

class PagePlay(tk.Frame):
    def __init__(self, master):
        global message
        tk.Frame.__init__(self, master)
        if option == 'passing':
            curr_player = players_list_wrap[player_passing_index]
            tk.Label(self, text=curr_player.name + ', choose the card(s) you would like to pass?' + ' (' + 
            str(3-card_passing_index) + ' left)', relief = tk.RAISED, border = 1, height = 7, width = 135).grid(row = 0, column = 1, columnspan = 9)
        else:
            curr_player = players_list_wrap[players_list_index]
            tk.Label(self, text="This is your hand " + curr_player.name, relief = tk.RAISED, border = 1, height = 7, width = 135).grid(row = 0, column = 1, columnspan = 9)
        playerPlay(curr_player, option, self, master)
        tk.Label(self, text="Trick Pile:", width = 32, height = 10, relief = tk.RAISED).grid(row = 1, column = 0)
        img = Image.open('heart_strip_cut.png')
        img = img.resize((230, 105), Image.ANTIALIAS)
        bannerimg = ImageTk.PhotoImage(img)
        banner = tk.Label(self, image = bannerimg, width = 230, relief = tk.RAISED)
        banner.image = bannerimg
        banner.grid(row = 0, column = 0)
        if first_trick == 0:
            firstp = 'True'
        else:
            firstp = 'False'
        if hearts_broken:
            heartsb = 'True'
        else:
            heartsb = 'False'
        tk.Label(self, width = 32, height = 9, relief = tk.RAISED, border = 3, text='Hearts Broken: ' + heartsb + '\n New Trick: '+ firstp + '\nLead Suit: ' + lead_suit).grid(row = 4, column = 0)
        tk.Label(self, relief = tk.RAISED, border = 3, text= message, width = 32, height = 9).grid(row = 5, column = 0)
        message = 'Message: ' 

class Passing(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        

def main():
    global inverse_deck
    global player_passing_index
    player_passing_index = 0 
    global card_passing_index
    card_passing_index = 0
    global option
    option = 'play'
    global message
    message = 'Message: '
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
    # Set-up the window
    app = SampleApp()
    app.mainloop()

                    
            
if __name__ == "__main__":
    main()