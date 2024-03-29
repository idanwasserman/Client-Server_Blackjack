import card
import random
from constants import *
import datetime
import user
import threading
import file_utils


def _add_timestamp_to_msg(msg):
    return f'[{datetime.datetime.now()}]\n{msg}'


class Model:
    """
    A model class part of MVC design pattern for a blackjack game

    ...

    Attributes
    ----------
    num_of_players : int
        number of players that are in the table
    num_of_decks : int
        number of decks in a single deck
    username : str
        the user's name which started the game
    user_money : float
        the user's amount of money
    """

    BLACKJACK = 21  # Blackjack value
    MAX_CARDS = MAX_CARDS   # max number of cards for each player

    def __init__(self, num_of_players, num_of_decks, username, user_money):
        self.num_of_players = num_of_players
        self.num_of_decks = num_of_decks
        self.user = user.User(username=username, money=user_money)
        self.deck = []
        self.game_on = False
        self.curr_player = 0

        self._reset()

    def _reset(self):
        self.game_on = False

        # Scores
        self.dealer_score = 0
        self.players_scores = [0] * self.num_of_players

        # Cards
        self.dealer_cards = []
        self.players_cards = []
        for player_num in range(self.num_of_players):
            self.players_cards.append([])

        # Cards' spots
        self.dealer_spot = 0
        self.players_spots = [0] * self.num_of_players

        # Deck - check there are enough cards
        if len(self.deck) < Model.MAX_CARDS * (self.num_of_players + 1):
            self.deck = card.create_deck(self.num_of_decks)

        # Current player playing
        self.curr_player = 0

    @staticmethod
    def new_game_message():
        return {
            NEW_GAME_MSG: _add_timestamp_to_msg('Starting a new game')
        }

    def quit(self):
        saving_thread = threading.Thread(target=self._save_game)
        saving_thread.start()
        return {
            SWITCHER: QUIT
        }

    def _save_game(self):
        """
        saves the user's information
        """
        users = file_utils.load_users_from_file()
        users[self.user.username] = self.user.get_money()
        file_utils.save_users_to_file(users)

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
        """
        Hits current player with a card from the deck.

        Raises
        -------
        Exception
            if deck is empty
        """
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
        """
        Hits the dealer with a card from the deck.

        Raises
        -------
        Exception
            if deck is empty
        """
        rand_card = self._grab_random_card_from_deck()
        if rand_card is None:
            raise Exception('card is None')
        self.dealer_cards.append(rand_card)
        self.dealer_score += rand_card[REAL_VALUE]
        self.dealer_spot += 1

    def stand(self):
        """
        Current player chose to finish his turn.
        The function checks if all players have played.
        """
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
        """
        Hits current player with a card from the deck.

        Raises
        -------
        Exception
            if deck is empty
        """
        # self.__init__(self.num_of_players, self.num_of_decks, self.user.username, self.user.get_money())
        self._reset()
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
        """
        This function writes a message contains the last game's results.
        :return: a message represent the results of the last game
        """
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

        prize = self._get_player_prize()
        self.user.add_money(prize)
        msg += f'{self.user.username} won {prize}\n'

        msg += f'Game Over!\nPress [{START}] to start a new game'
        return {
            RESULTS: _add_timestamp_to_msg(msg),
            PRIZE: prize,
            USER_MONEY: self.user.get_money()
        }

    def _get_player_prize(self):
        """
        This function calculates how much the user won depends on his and dealer's scores
        :return: user's calculated prize
        """
        main_player_score = self.players_scores[0]
        lower_than_dealer = main_player_score < self.dealer_score <= Model.BLACKJACK
        if main_player_score > Model.BLACKJACK or lower_than_dealer:
            # lost - player gets nothing
            return 0
        else:
            if main_player_score == self.dealer_score:
                # a tie - player gets his bet back
                return self.bet
            else:
                if main_player_score == Model.BLACKJACK:
                    # win with BLACKJACK - player gets 2.5 * bet
                    return self.bet * 2.5
                else:
                    # win - player get 2.0 * bet
                    return self.bet * 2.0

    def process_data(self, data):
        """
        Model's main function which called each time user is using the system.\n
        :param data: data got from the Controller which needs to be processed
        :return: relevant updates for the View
        """
        if BET in data:
            return self._handle_player_bet(data)

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

    def _handle_player_bet(self, data):
        """
        Checks that user has got enough money to gamble on
        """
        self.bet = float(data.split('=')[1])
        try:
            self.user.take_money(self.bet)
            return {
                ERROR: False,
                BET: self.bet
            }
        except Exception as e:
            print(e)
            return {
                ERROR: True,
                MSG: _add_timestamp_to_msg("You don't have enough money")
            }
