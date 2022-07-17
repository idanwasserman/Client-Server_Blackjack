from card import *
import random
from constants import *


class Model:

    BLACKJACK = 21
    MAX_CARDS = 5

    def __init__(self, num_of_players, num_of_decks):
        self.num_of_players = num_of_players
        self.num_of_decks = num_of_decks
        self.game_on = False
        # Scores
        self.dealer_score = 0
        self.players_scores = [0] * self.num_of_players
        # Cards
        self.dealer_cards = []
        self.players_cards = []
        for player_num in range(num_of_players):
            self.players_cards.append([])
        # Cards' spots
        self.dealer_spot = 0
        self.players_spots = [0] * self.num_of_players
        self.deck = Card.create_deck(num_of_decks)
        # Current player playing
        self.curr_player = 0

    def quit(self):
        # TODO: save game stats
        print(self)
        return {
            SWITCHER: QUIT
        }

    def hit_card(self):
        # Check player can hit more cards
        if not self.players_spots[self.curr_player] < Model.MAX_CARDS:
            return {
                SWITCHER: SHOW_MSG,
                MSG: f'You cannot have more than {Model.MAX_CARDS} cards! Your turn is over'
            }

        self._hit_player()
        spot = self.players_spots[self.curr_player] - 1
        ret_dict = {
            SWITCHER: HIT_CARD,
            CARD: self.players_cards[self.curr_player][spot],
            SPOT: spot,
            PLAYER_NUM: self.curr_player
        }

        if self.players_scores[self.curr_player] >= Model.BLACKJACK:
            ret_dict[SWITCHER] = f'{HIT_CARD}_{SHOW_MSG}'
            if self.players_scores[self.curr_player] == Model.BLACKJACK:
                ret_dict[MSG] = 'You got BLACKJACK! Your turn is over'
            else:
                # TODO: check if there are ACES in cards
                ret_dict[MSG] = 'You got OVER BLACKJACK! Your turn is over'

        return ret_dict

    def _hit_player(self):
        card = self._grab_random_card_from_deck()
        if card is None:
            raise Exception('card is None')
        self.players_cards[self.curr_player].append(card)
        self.players_scores[self.curr_player] += card.real_value
        self.players_spots[self.curr_player] += 1

    def _hit_dealer(self):
        card = self._grab_random_card_from_deck()
        if card is None:
            raise Exception('card is None')
        self.dealer_cards.append(card)
        self.dealer_score += card.real_value
        self.dealer_spot += 1

    def stand(self):
        self.curr_player += 1
        if self.curr_player >= self.num_of_players:
            return {
                SWITCHER: STAND,
                MSG: "All players finished their turns. Dealer's turn",
                IS_OVER: True
            }
        else:
            return {
                SWITCHER: STAND,
                MSG: f"It's player #{self.curr_player+1} turn",
                IS_OVER: False
            }

    def start_new_game(self):
        self.__init__(self.num_of_players, self.num_of_decks)
        print('started a new game')
        self.game_on = True

        # Each player (includes dealer) gets 2 cards
        for spot in range(2):
            self._hit_dealer()
            for player_num in range(self.num_of_players):
                self.curr_player = player_num
                self._hit_player()
        self.curr_player = 0

        return {
            SWITCHER: NEW_GAME,
            DEALER_SPOTS: [i for i in range(2)],
            DEALER_CARDS: [self.dealer_cards[i] for i in range(2)],
            PLAYERS: [i for i in range(self.num_of_players)],
            PLAYERS_SPOTS: [i for i in range(2)],
            PLAYERS_CARDS: self.players_cards
        }

    def _grab_random_card_from_deck(self):
        try:
            card = random.choice(self.deck)
        except ValueError as e:
            print(e)
            return None
        self.deck.remove(card)
        return card

    def dealer_turn(self):
        if self.dealer_score < 17 and self.dealer_spot < Model.MAX_CARDS:
            self._hit_dealer()
            spot = self.dealer_spot - 1
            return self.dealer_cards[spot], spot
        else:
            self.game_on = False
            return None

    def get_results(self):
        winners = []
        draws = []
        losers = []
        for i in range(self.num_of_players):
            curr_player_score = self.players_scores[i]
            lower_than_dealer = curr_player_score < self.dealer_score <= Model.BLACKJACK
            if curr_player_score > Model.BLACKJACK or lower_than_dealer:
                losers.append(i + 1)
            else:
                if curr_player_score == self.dealer_score:
                    draws.append(i + 1)
                else:
                    winners.append(i + 1)
        return winners, draws, losers
