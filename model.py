import card
import random
from constants import *
import datetime
import user


def _add_timestamp_to_msg(msg):
    return f'[{datetime.datetime.now()}]\n{msg}'


class Model:

    BLACKJACK = 21
    MAX_CARDS = 5

    def __init__(self, num_of_players, num_of_decks, username, user_money):
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
        self.deck = card.create_deck(num_of_decks)
        # Current player playing
        self.curr_player = 0
        # User
        self.user = user.User(username=username, money=user_money)

    @staticmethod
    def new_game_message():
        return {
            NEW_GAME_MSG: _add_timestamp_to_msg('Starting a new game')
        }

    def quit(self):
        self._save_game()
        return {
            SWITCHER: QUIT
        }

    def _save_game(self):
        # TODO: save game stats
        pass

    def hit_card(self):
        # Check player can hit more cards
        if not self.players_spots[self.curr_player] < Model.MAX_CARDS:
            return {
                SWITCHER: SHOW_MSG,
                MSG: f'You cannot have more than {Model.MAX_CARDS} cards!\nYour turn is over'
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
                ret_dict[MSG] = _add_timestamp_to_msg(f'{PLAYER} #{self.curr_player + 1} got BLACKJACK!')
            else:
                ret_dict[MSG] = _add_timestamp_to_msg(f'{PLAYER} #{self.curr_player + 1} got OVER BLACKJACK!')

        return ret_dict

    def _hit_player(self):
        rand_card = self._grab_random_card_from_deck()
        if rand_card is None:
            raise Exception('card is None')

        self.players_cards[self.curr_player].append(rand_card)
        self.players_scores[self.curr_player] += rand_card[REAL_VALUE]
        self.players_spots[self.curr_player] += 1

        if self.players_scores[self.curr_player] > Model.BLACKJACK:
            for card_num in range(len(self.players_cards[self.curr_player])):
                if self.players_cards[self.curr_player][card_num][VALUE] == card.Ace_Card.ACE_VALUE:
                    if self.players_cards[self.curr_player][card_num][HIGH_VALUE]:
                        self.players_cards[self.curr_player][card_num][HIGH_VALUE] = False
                        self.players_scores[self.curr_player] -= 10
                        break

    def _hit_dealer(self):
        rand_card = self._grab_random_card_from_deck()
        if rand_card is None:
            raise Exception('card is None')
        self.dealer_cards.append(rand_card)
        self.dealer_score += rand_card[REAL_VALUE]
        self.dealer_spot += 1

    def stand(self):
        self.curr_player += 1
        if self.curr_player >= self.num_of_players:
            return {
                SWITCHER: STAND,
                MSG: _add_timestamp_to_msg("All players finished their turns\nDealer's turn"),
                IS_OVER: True
            }
        else:
            msg = f"{PLAYER} #{self.curr_player} finished his turn!\nIt's player #{self.curr_player+1} turn"
            return {
                SWITCHER: STAND,
                MSG: _add_timestamp_to_msg(msg),
                IS_OVER: False
            }

    def start_new_game(self):
        self.__init__(self.num_of_players, self.num_of_decks, self.user.username, self.user.money)
        # print('Model - started a new game')
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
            rand_card = random.choice(self.deck)
        except ValueError as e:
            print(e)
            return None
        self.deck.remove(rand_card)
        return rand_card

    def dealer_turn(self):
        if self.dealer_score < 17 and self.dealer_spot < Model.MAX_CARDS:
            self._hit_dealer()
            spot = self.dealer_spot - 1
            return {
                CARD: self.dealer_cards[spot],
                SPOT: spot,
                BOOL: True
            }
        else:
            self.game_on = False
            return {
                BOOL: False
            }

    def get_results(self):
        msg = f'{SCORES}:\n'
        msg += f'{DEALER}: {self.dealer_score}\n'
        for player_num in range(self.num_of_players):
            curr_player_score = self.players_scores[player_num]
            lower_than_dealer = curr_player_score < self.dealer_score <= Model.BLACKJACK
            if curr_player_score > Model.BLACKJACK or lower_than_dealer:
                curr_result = LOST
            else:
                if curr_player_score == self.dealer_score:
                    curr_result = TIE
                else:
                    curr_result = WON
            msg += f'{PLAYER} #{player_num + 1}: {self.players_scores[player_num]} ({curr_result})\n'

        msg += f'Game Over!\nPress [{START}] to start a new game'
        return {
            RESULTS: _add_timestamp_to_msg(msg)
        }

    def process_data(self, data):
        func_dict = {
            START: self.start_new_game,
            HIT: self.hit_card,
            STAND: self.stand,
            QUIT: self.quit,
            NEW_GAME_MSG: self.new_game_message,
            DEALER_TURN: self.dealer_turn,
            GET_RESULTS: self.get_results
        }
        ret_val = func_dict[data]()
        return ret_val
