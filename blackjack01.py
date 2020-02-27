#!/usr/bin/python -tt

import sys
import os
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
playing = True

class Cards:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank +' of '+ self.suit
 
class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Cards(suit,rank))
        
    def __str__(self):
        deck_row = ''
        for card in self.deck:
            deck_row += '\n' + card.str()
        return 'The deck holds these cards:\n' + deck_row

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:

    def __init__(self):
        self.cards  = []
        self.value = 0
        self.aces   = 0

    def adjustForAce(self,card):
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def addCard(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Aces':
            self.aces += 1

class Chips:

    def __init__(self):
        self.amount = 100
        self.bet = 0

    def win_bet(self):
        self.amount += self.bet

    def lose_bet(self):
        self.amount -= self.bet

def take_bet(chips):
    while True:
        try:
            bet = int(input('Player please enter your bet:\n'))
        except TypeError:
            print('Please enter a real number\n')
            continue
        else:
            if bet > chips.amount:
                print(f'You are low on funds !!! Bet below: {chips.amount}')
                continue
            chips.bet = bet
            break

def hit(deck, hand):
    card = deck.deal()
    hand.addCard(card)
    if card.rank == 'Ace':
        hand.adjustForAce(card)

def hit_or_stand(deck, hand):
    global playing
    while True:
        option = input('Player choose wisely: You Want to "h" or "s"\n')
        if option.lower() == 'h':
            hit(deck, hand)
        elif option.lower() == 's':
            playing = False
        else:
            print('Sorry! please try again\n')
            continue
        break
    

def show_some(player,dealer):
    print(f'\nDealer\'s cards: {dealer.cards[0].rank} of {dealer.cards[0].suit}')
    print(f'\nPlayer\'s cards:')
    for card in player.cards:
        print(f'{card.rank} of {card.suit}')

def show_all(player,dealer):
    print(f'\nPlayer\'s cards:')
    for card in player.cards:
        print(f'{card.rank} of {card.suit}')
    print(f'\nPlayer\'s Total: {player.value}')
    print(f'\nDealer\'s cards:')
    for card in dealer.cards:
        print(f'{card.rank} of {card.suit}')
    print(f'\nDealer\'s Total: {dealer.value}')
    

def player_bust(chips):
    print('Player Busted!!!')
    chips.lose_bet()

def player_win(chips):
    print('Player Won!!!')
    chips.win_bet()

def dealer_bust(chips):
    print('Dealer Busted!!!')
    chips.win_bet()

def dealer_win(chips):
    print('Dealer Won!!!')
    chips.lose_bet()

def push():
    print('Dealer and Player tie! its a push\n')

def main():
    # Set up the Player's chips
    player_chips = Chips()

    while True:
        # Print an opening statement
        print('Welcome To The Game Of BlackJack !!!\n')

        # Create & shuffle the deck, deal two cards to each player
        deck = Deck()
        deck.shuffle()
        player = Hand()
        hit(deck, player)
        hit(deck, player)
        dealer = Hand()
        hit(deck, dealer)
        hit(deck, dealer)

        # Prompt the Player for their bet
        take_bet(player_chips)

        # Show cards (but keep one dealer card hidden)
        show_some(player,dealer)
        global playing

        while playing:  # recall this variable from our hit_or_stand function

            # Prompt for Player to Hit or Stand
            hit_or_stand(deck, player)

            # Show cards (but keep one dealer card hidden)
            show_some(player, dealer)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player.value > 21:
                player_bust(player_chips)      
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        while dealer.value < 17 and player.value < 21:
            hit(deck, dealer) 

        # Show all cards
        show_all(player,dealer)

        # Run different winning scenarios
        if player.value > 21:
            pass
        elif player.value == 21:
            player_win(player_chips)
        elif dealer.value == 21:
            dealer_win(player_chips)
        elif dealer.value > 21:
            dealer_bust(player_chips)
        elif player.value > dealer.value:
            player_win(player_chips)
        elif dealer.value > player.value:
            dealer_win(player_chips)
        else:
            push()

        # Inform Player of their chips total
        print(f'Player\'s Chip Total is: {player_chips.amount}\n')

        # Ask to play again
        option = input('Would you like to play another hand: Enter "y" or "n"\n')
        if option.lower() == 'y':
            if player_chips.amount == 0:
                print('Hard Luck!!! Looks like you are out of chips,\n 100 coins are credited to your account\n')
                player_chips.amount += 100
            playing = True
            continue
        else:
            print('\nThankyou For Playing With Us!!!')
            break


if __name__ == '__main__':
    main()
