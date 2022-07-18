from view import View
from model import Model
from constants import *
import sys


class Controller:

    def __init__(self, num_of_players, num_of_decks):
        self.view = View(self, num_of_players)
        self.model = Model(num_of_players, num_of_decks)

    def main(self):
        self.view.main()

    """
    User clicked a button. This function is called by the view.
    input: caption of button which user has clicked
    """
    def on_button_click(self, caption):
        """
        if game has started -> cannot start again or quit
        if game hasn't started -> can only start or quit
        """
        b1 = bool(caption == START or caption == QUIT)
        b2 = self.model.game_on
        if b1 == b2:
            return

        func = self._button_string_to_function(caption)
        ret_dict = func()
        self._update_view(ret_dict)

    """
    input: caption of button which user has clicked
    output: function to perform
    """
    def _button_string_to_function(self, caption):
        buttons_switcher = {
            START: self.model.start_new_game,
            HIT: self.model.hit_card,
            STAND: self.model.stand,
            QUIT: self.model.quit
        }
        return buttons_switcher.get(caption)

    """
    input: dictionary with relevant objects and data to update view
    """
    def _update_view(self, dictionary):
        switcher = dictionary[SWITCHER]

        if switcher == NEW_GAME:
            self._new_game_started(dictionary)
            return
        elif switcher == STAND:
            self._curr_player_turn_over(dictionary)
        elif switcher == QUIT:
            self.view.destroy_all()
            self.view.destroy()

        if HIT_CARD in switcher:
            card_img = dictionary[CARD].image
            spot = dictionary[SPOT]
            player_num = dictionary[PLAYER_NUM]
            self.view.players_cards_labels[player_num][spot].config(image=card_img)
            self.view.players_cards_labels[player_num][spot].image = card_img

        if SHOW_MSG in switcher:
            self.view.show_message(dictionary[MSG])
            ret_val = self.model.stand()
            self._curr_player_turn_over(ret_val)

    """
    Current player has finished his turn.
    If all the players have played -> It's dealer's turn
    """
    def _curr_player_turn_over(self, dictionary):
        self.view.show_message(dictionary[MSG])

        if dictionary[IS_OVER]:
            self._dealer_turn()

    """
    Dealer's turn starts with revealing his 2nd card.
    After that dealer hits cards till his score is at least 17.
    """
    def _dealer_turn(self):
        self.view.reveal_hidden_card()
        while True:
            ret_val = self.model.dealer_turn()
            if ret_val is None:
                break

            card, spot = ret_val
            self.view.show_card(-1, card, spot)

        # Dealer's turn is over -> Show results
        self.view.show_message(self.model.get_results())

    def _new_game_started(self, dictionary):
        # Clear old cards
        self.view.clear_cards()
        # Show message
        self.view.show_message('Started a new game')

        # Update dealer's cards
        dealer_cards = dictionary[DEALER_CARDS]
        for dealer_spot in dictionary[DEALER_SPOTS]:
            curr_img = dealer_cards[dealer_spot].image
            self.view.dealer_cards_labels[dealer_spot].config(image=curr_img)
            self.view.dealer_cards_labels[dealer_spot].image = curr_img

        # Hide 2nd dealer's card
        self.view.hide_card()

        # Update players' cards
        players_cards = dictionary[PLAYERS_CARDS]
        for player_num in dictionary[PLAYERS]:
            for player_spot in dictionary[PLAYERS_SPOTS]:
                curr_img = players_cards[player_num][player_spot].image
                self.view.players_cards_labels[player_num][player_spot].config(image=curr_img)
                self.view.players_cards_labels[player_num][player_spot].image = curr_img


if __name__ == '__main__':
    try:
        nop = int(sys.argv[1])  # number of players
        nod = int(sys.argv[2])  # number of decks
        blackjack = Controller(nop, nod)
        blackjack.main()
    except ValueError as e:
        print(e)
