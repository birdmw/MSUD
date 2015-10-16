from deck import Deck
import sys

class BlackJack(object):
    def __init__(self, player_count=1):
        self.players = [Player() for i in range(player_count+1)]
        self.dealer = self.players[0]
        self.D = Deck()

    def deal_cards(self):
        self.D = Deck()
        self.D.shuffle()
        for p in self.players:
            p.clear()
        for i in range(2):
            for p in self.players:
                p.hand.append(self.D.draw_card())
                p.calculate_total()
        self.dealer.print_hand()

    def take_turn(self):
        ordered_of_play_player_list = self.players[1:] + [self.dealer]
        self.dealer.print_hand()
        for p in ordered_of_play_player_list:
            p.print_hand()
            stay_flag = 0
            while stay_flag == 0:
                if p == self.dealer:
                    if p.total <= 16:
                        p.hit(self.D.draw_card)
                    elif  p.total > 16:
                        stay_flag = 1
                        print "Dealer Stays"
                    elif p.total > 21:
                        stay_flag = 1
                        print "Dealer Bust!"

                else:  # players (not dealer)
                    if not(p.bust):
                        hit_or_stay = input("0 to stay, 1 to hit")
                        if hit_or_stay == 0:
                            stay_flag = 1
                        else:  # hit
                            p.hit(self.D.draw_card)
                    else:
                        stay_flag = 1
                        print "BUST!"

    def score_player(self, player_to_score):
        '''
        argument(s): player object
        return: int (-1 is loss, 0 is push, 1 is win)
        '''

        # special case for dealer
        if player_to_score == self.dealer:
            if player_to_score.bust == 1:
                return -1
            else:
                return 1
        else: # player ( not dealer )
            if player_to_score.bust:
                return -1
            elif self.dealer.bust:
                return 1
            else: # player and dealer have not busted
                if player_to_score.total < self.dealer.total:
                    return -1
                elif player_to_score.total == self.dealer.total:
                    return 0
                elif player_to_score.total > self.dealer.total:
                    return 1


    def score_game(self):
        '''
        argument(s): None
        return: list( players boolean win/loss )
        dealer win/loss is based on his own bust, not compared to players

        for p in player:
            print self.score_player(p)


        example:
        print score_game()

        [ 1, 1, 0, 1 ]
        Dealer did not bust, player1 beat the dealer, player2 lost to the deal, player 3 beat the dealer

        '''
        for p in self.players:
            if p.total > 21:
                p.bust = 1
                #NOT FINISHED------------------------


    def play_a_game(self):
        quit_flag = raw_input("Would you like to play a hand? y/n: ")
        if quit_flag == 'n':
            sys.exit("Good Game(s)!")
        self.deal_cards()
        self.take_turn()

    def print_winners(self):
        '''
        argument(s): None
        return: None

        prints the winners

        use self.score_game() to find out who the winners are
        '''

class Player(object):
    def __init__(self):
        self.hand = []
        self.total = 0
        self.bust = 0

    def clear(self):
        self.hand = []
        self.total = 0
        self.bust = 0

    def hit(self, card):
        self.hand.append(card)
        self.calculate_total()
        self.print_hand()

    def calculate_total(self):
        '''
        argument(s): None
        return: None
        =========================
        sum all cards of player with aces == 11
        If the total is above 21:
            calculate total with each Ace as a 1 while sum is above 21
        Set self.total to be sum of cards
        '''
        pass

    def print_hand(self):
        '''
        args: NONE
        return: NONE

        just prints the hand

        example1:
        THE DEALER SHOWS: ACE of hearts, 5 of spades

        example2:
        print "player # " + str(self.players.index(p)) + "'s turn" #<===== use this inside the loop
        THE DEALER SHOWS: ACE of hearts, 5 of spades
        PLAYER 2 HAS: 4 of diamonds, 7 of clubs, JACK of hearts

        '''
        print "print_hand"

def main():

    b = BlackJack()
    while True:
        b.play_a_game()

if __name__ == "__main__":
    main()