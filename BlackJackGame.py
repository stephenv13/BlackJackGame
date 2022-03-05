'''
Project 2 - Simple BlackJack Game

- You will use Object Oriented Programming.
- We will use a computer dealer and a human player, starting with a normal deck of cards.

1. Start with deck of cards
2. Player places a bet, coming from their 'bankroll'
3. Dealer starts with 1 card face up and 1 card face down. Player starts with 2 cards face up.
4. Player goes first, can either:
    - Hit: receive another card
    - Stay: stop receiving cards

    If player sum > 21, player busts and dealer collects money.

5. If player stays and sum is under 21, dealer then hits until they either beat the player by hitting 21
   or the dealer busts > 21
6. If player wins, their bet is doubled and added to 'bankroll'

Special Rules:

- Face Cards (Jack, Queen, King) value = 10
- Aces can count as either 1 or 11, players choice

Classes >> Card, Deck, Hand, Bankroll

'''

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
              'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card():
    '''
    This class creates a single card object
    '''
    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck():
    '''
    This class creates a full deck of cards. It can also shuffle all of the cards and if the cards are dealt,
    it removes them from the deck.
    '''
    def __init__(self) -> None:
        
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                # Create the card object
                
                created_card = Card(suit,rank)
                
                self.all_cards.append(created_card)
                
    def shuffle(self) -> None:
        
        random.shuffle(self.all_cards)
        
    def deal_one(self) -> Card:
        return self.all_cards.pop()

new_deck = Deck()

class Bankroll():

    def __init__(self, balance: int) -> None:
        self.balance = balance
    
    def add(self, num: int) -> None:
        self.balance += num
    
    def subtract(self, num) -> None:
        self.balance -= num
    
    def balance(self) -> int:
        return self.balance

    def __str__(self) -> str:
        return f'Your total bankroll is currently: {self.balance}'

class Hand():

    def __init__(self):
        self.hand = []
        self.value = 0
    
    def add_card(self,card: Card):
        self.hand.append(card)
    
    def get_value(self) -> int:
        self.value = 0

        for card in self.hand:
            self.value += card.value
        return self.value

    def show_hand(self,player: str):
        mycards = []
        self.value = 0

        for card in self.hand:
            mycards.append(card.__str__())
            self.value += card.value
        if player == 'player':
            return f'Player Hand: {mycards}, Total Value: {self.value}'

        return f'Dealer Hand: {mycards}, Total Value: {self.value}'
    def show_one(self):
        lastcard = self.hand[-1]
        mycards = [lastcard.__str__()]
        self.value = lastcard.value
        return f'Dealer Hand: {mycards}, Total Value: {self.value}'

# GAME FUNCTIONS

def setup_game():
    print('Welcome to Black Jack!\n')

    new_deck.shuffle()
    
    player_bankroll = Bankroll(100).balance
    dealer_bankroll = Bankroll(1000).balance

    return player_bankroll, dealer_bankroll

def bet(player_balance: int):
    player_bet = int(input('Place your bet: '))
    print('\n')

    if player_bet > player_balance:
        print('Bet too large!\n')
        not_valid_bet = True
    else:
        not_valid_bet = False

    return player_bet, not_valid_bet

def check_bust(player: str) -> bool:
    if player == 'player':
        if player_hand.get_value() > 21:
            print('BUST! Dealer Wins!\n')
            return True
    else:
        if dealer_hand.get_value() > 21:
            print('BUST! Player Wins!\n')
            return True
    return False

def check_blackjack(player: str) -> bool:
    if player == 'player':
        if player_hand.get_value() == 21:
            print('BLACKJACK! Player Wins!\n')
            return True
    else:
        if dealer_hand.get_value() == 21:
            print('BLACKJACK! Dealer Wins!\n')
            return True
    return False

# MAIN METHOD
if __name__ == '__main__':

    player_balance, dealer_balance = setup_game()
    game_on = True
    
    while game_on:
        print(f'Dealer Bankroll: {dealer_balance}')
        print(f'Player Bankroll: {player_balance}\n')

        not_valid_bet = True

        while not_valid_bet:
            player_bet, not_valid_bet = bet(player_balance)
        
        player_hand = Hand()
        dealer_hand = Hand()
            
        player_hand.add_card(new_deck.deal_one())
        player_hand.add_card(new_deck.deal_one())
        dealer_hand.add_card(new_deck.deal_one())
        dealer_hand.add_card(new_deck.deal_one())

        print(dealer_hand.show_one())
        print(player_hand.show_hand('player') + '\n')

        hit = True

        while hit:
            player_choice = str(input('Would you like to hit? Yes or No: ')).upper()

            if player_choice == 'YES':
                player_hand.add_card(new_deck.deal_one())
                print(player_hand.show_hand('player') + '\n')

                if check_bust('player') == True:
                    player_balance -= player_bet
                    dealer_balance += player_bet
                    hit = False

                if check_blackjack('player') == True:
                    player_balance += (player_bet*1.5) + player_bet
                    dealer_balance -= player_bet*1.5
                    hit = False
            else:
                hit = False
                
                print(dealer_hand.show_hand('dealer') + '\n')

                #check for dealer blackjack
                if check_blackjack('dealer') == True:
                    player_balance -= player_bet
                    dealer_balance += player_bet
                    break

                while dealer_hand.get_value() < 17:
                    dealer_hand.add_card(new_deck.deal_one())
                    print(dealer_hand.show_hand('dealer') + '\n')

                if check_bust('dealer') == True:
                    player_balance += player_bet
                    dealer_balance -= player_bet
                    break

                if check_blackjack('dealer') == True:
                    player_balance -= player_bet
                    dealer_balance += player_bet
                    break
                
                if dealer_hand.get_value() > player_hand.get_value():
                    print('Dealer Wins!')
                    player_balance -= player_bet
                    dealer_balance += player_bet

                elif dealer_hand.get_value() == player_hand.get_value():
                    dealer_hand.add_card(new_deck.deal_one())
                    
                    if check_bust('dealer') == True:
                        player_balance += player_bet
                        dealer_balance -= player_bet
                        break

                    if check_blackjack('dealer') == True:
                        player_balance -= player_bet
                        dealer_balance += player_bet
                        break
                else:
                    print('Player Wins!')
                    player_balance += player_bet
                    dealer_balance -= player_bet

        if player_balance == 0:
            print('You are broke! Game Over.')
            game_on = False

        play_again = str(input('Would you like to play again? Yes or No: ')).upper()
        
        if play_again == 'NO':
            game_on = False
        