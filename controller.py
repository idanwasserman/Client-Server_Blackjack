from view import View
from constants import *
import sys
from client import MyClient
import card
import json


class Controller:

    def __init__(self, num_of_players, num_of_decks, username, user_money):
        self.view = View(self, num_of_players, username, user_money)
        self.client = MyClient()
        self.game_on = False
        self.username = username
        self.user_money = user_money

        info_dict = {
            NUM_PLAYERS: num_of_players,
            NUM_DECKS: num_of_decks,
            USERNAME: username,
            USER_MONEY: user_money
        }
        self.client.send_recv_data(json.dumps(info_dict))

    def main(self):
        self.view.main()

    def on_button_click(self, caption):
        """
        User clicked a button. This function is called by the View.\n
        if game has started -> cannot start again or quit.\n
        if game hasn't started -> can only start or quit.\n

        Parameters
        ----------
        caption : string
            the button's caption which user has clicked
        """
        b1 = bool(caption == START or caption == QUIT)
        b2 = self.game_on
        if b1 == b2:
            return

        server_answer = dict(self.client.send_recv_data(caption))
        self._update_view(server_answer)

    def _update_view(self, dictionary):
        """
        Updates view

        Parameters
        ----------
        dictionary : dict
            a dictionary with relevant objects and data to update view
        """
        switcher = dictionary[SWITCHER]

        if switcher == NEW_GAME:
            self.user_bet = self.view.get_player_bet()
            player_bet_text = f'{BET}={self.user_bet}'
            server_answer = self.client.send_recv_data(player_bet_text)
            if server_answer[ERROR]:
                self.view.show_message(server_answer[MSG])
                return
            else:
                self.view.change_buttons_state()
                self._new_game_started(dictionary)
                return

        elif switcher == STAND:
            self._curr_player_turn_over(dictionary)

        elif switcher == QUIT:
            self.client.send_recv_data(DISCONNECT_MSG)
            self.view.destroy_all()
            self.view.destroy()

        if HIT_CARD in switcher:
            card_img = card.get_resized_image(dictionary[CARD][PATH])
            spot = dictionary[SPOT]
            player_num = dictionary[PLAYER_NUM]
            self.view.players_cards_labels[player_num][spot].config(image=card_img)
            self.view.players_cards_labels[player_num][spot].image = card_img

        if SHOW_MSG in switcher:
            self.view.show_message(dictionary[MSG])
            server_answer = dict(self.client.send_recv_data(STAND))
            self._curr_player_turn_over(server_answer)

    def _curr_player_turn_over(self, dictionary):
        """
        Current player turn is over.
        If all the players have played -> It's dealer's turn.

        Parameters
        ----------
        dictionary : dict
            a dictionary with relevant objects and data
        """

        self.view.show_message(dictionary[MSG])

        if dictionary[IS_OVER]:
            self._dealer_turn()

    def _dealer_turn(self):
        """
        Dealer's turn starts with revealing his 2nd card.
        After that dealer hits cards till his score is at least 17.
        """
        self.view.reveal_hidden_card()
        while True:
            server_answer = self.client.send_recv_data(DEALER_TURN)
            if not server_answer[BOOL]:
                break

            self.view.show_card(-1, server_answer[CARD], server_answer[SPOT])

        # Dealer's turn is over -> Show results
        server_answer = self.client.send_recv_data(GET_RESULTS)
        self.view.change_buttons_state()
        self.view.show_message(server_answer[RESULTS])
        # Update money
        self.user_money = server_answer[USER_MONEY]
        self.view.update_money_label(self.user_money)

        self.game_on = False

    def _new_game_started(self, dictionary):
        """
        New game has been started.

        Parameters
        ----------
        dictionary : dict
            a dictionary with relevant objects and data
        """
        self.game_on = True
        # Clear old cards
        self.view.clear_cards()
        # Show message
        server_answer = self.client.send_recv_data(NEW_GAME_MSG)
        self.view.show_message(server_answer[NEW_GAME_MSG])
        # Update money
        self.user_money -= self.user_bet
        self.view.update_money_label(self.user_money)

        # Update dealer's cards
        dealer_cards = dictionary[DEALER_CARDS]
        for dealer_spot in dictionary[DEALER_SPOTS]:
            curr_img = card.get_resized_image(dealer_cards[dealer_spot][PATH])
            self.view.dealer_cards_labels[dealer_spot].config(image=curr_img)
            self.view.dealer_cards_labels[dealer_spot].image = curr_img

        # Hide 2nd dealer's card
        self.view.hide_card(dealer_cards[1][PATH])

        # Update players' cards
        players_cards = dictionary[PLAYERS_CARDS]
        for player_num in dictionary[PLAYERS]:
            for player_spot in dictionary[PLAYERS_SPOTS]:
                curr_img = card.get_resized_image(players_cards[player_num][player_spot][PATH])
                self.view.players_cards_labels[player_num][player_spot].config(image=curr_img)
                self.view.players_cards_labels[player_num][player_spot].image = curr_img


if __name__ == '__main__':
    try:
        nop = int(sys.argv[1])   # number of players
        nod = int(sys.argv[2])   # number of decks
        un = sys.argv[3]         # username
        um = float(sys.argv[4])  # user money
        blackjack = Controller(nop, nod, un, um)
        blackjack.main()
    except ValueError as e:
        print(e)
