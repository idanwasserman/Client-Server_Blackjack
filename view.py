import tkinter as tk
from tkinter.ttk import *
import card
from constants import *


class View(tk.Tk):
    CARD_TOTAL_SPOTS = 5
    PAD = 10

    button_captions = [
        START, HIT, STAND, QUIT
    ]

    def __init__(self, controller, num_of_players, username, user_money):
        super().__init__()
        self.title(TITLE)
        self.geometry(GEOMETRY)
        self.configure(background=GREEN)

        self.controller = controller
        self.hidden_card_path = None

        self.first_msg = 'Hello players'
        self.second_msg = 'Blackjack game'
        self.third_msg = ''

        self._make_main_frame()
        self._make_text_label()
        self._make_dealer_frame()
        self._make_players_frames(num_of_players, username, user_money)
        self._make_bet_frame(username)
        self._make_buttons()

    def main(self):
        self.mainloop()

    def destroy_all(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

    def show_card(self, player_num, card_to_show, spot):
        curr_card_text = f'{card_to_show[VALUE]}_of_{card_to_show[SUIT]}'
        curr_card_img = card.get_resized_image(f'{card.CARDS_IMAGES_PATH}\\{curr_card_text}.png')
        if player_num < 0:
            self.dealer_cards_labels[spot].config(image=curr_card_img)
            self.dealer_cards_labels[spot].image = curr_card_img
        elif player_num < len(self.players_cards_labels):
            self.players_cards_labels[player_num][spot].config(image=curr_card_img)
            self.players_cards_labels[player_num][spot].image = curr_card_img

    def hide_card(self, path):
        question_mark_img = card.get_question_mark_card_image()
        self.hidden_card_path = path
        self.dealer_cards_labels[1].config(image=question_mark_img)
        self.dealer_cards_labels[1].image = question_mark_img

    def reveal_hidden_card(self):
        image = card.get_resized_image(self.hidden_card_path)
        self.dealer_cards_labels[1].config(image=image)
        self.dealer_cards_labels[1].image = image

    def clear_cards(self):
        blank_img = card.get_blank_card_image()
        for label in self.dealer_cards_labels:
            label.config(image=blank_img)
            label.image = blank_img
        for player_num in range(len(self.players_cards_labels)):
            for label in self.players_cards_labels[player_num]:
                label.config(image=blank_img)
                label.image = blank_img

    def show_message(self, message):
        self.first_msg = self.second_msg
        self.second_msg = self.third_msg
        self.third_msg = message
        self.output_text.set(self.first_msg + '\n\n' + self.second_msg + '\n\n' + self.third_msg)

    def update_money_label(self, user_money):
        self.money_label[TEXT] = f'Money: {user_money}'

    def _make_text_label(self):
        self.output_text = tk.StringVar()
        self.label_text = tk.Label(self.main_frame, font=('arial', 14), textvariable=self.output_text)
        self.label_text.pack(side=tk.LEFT, padx=View.PAD)
        self.output_text.set(self.first_msg + '\n\n' + self.second_msg)

    def _make_main_frame(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(padx=self.PAD, pady=self.PAD)

    def _make_buttons(self):
        frame = tk.LabelFrame(self.main_frame)
        frame.pack(side=tk.BOTTOM)

        for caption in self.button_captions:

            if caption == START:
                color = GREEN
            elif caption == QUIT:
                color = RED
            else:
                color = BLACK

            btn = tk.Button(
                frame, text=caption,
                command=(lambda button_caption=caption: self.controller.on_button_click(button_caption)),
                foreground=color, font=('arial', 13, 'bold', 'italic')
            )
            btn.pack(side=tk.LEFT, padx=self.PAD, pady=self.PAD)

    def _make_dealer_frame(self):
        # Dealer's frame
        dealer_frame = tk.LabelFrame(self.main_frame, text=DEALER)
        dealer_frame.pack(pady=self.PAD)

        # Dealer's cards
        blank_img = card.get_blank_card_image()
        self.dealer_cards_labels = []
        for spot in range(self.CARD_TOTAL_SPOTS):
            card_label = tk.Label(dealer_frame, text='', image=blank_img)
            card_label.grid(row=0, column=spot, padx=self.PAD, pady=self.PAD)
            self.dealer_cards_labels.append(card_label)
            # anchor img to object
            self.dealer_cards_labels[spot].image = blank_img

    def _make_players_frames(self, num_of_players, username, user_money):
        self.players_cards_labels = []
        for player_num in range(num_of_players):
            # Player's frame
            if player_num == 0:
                player_name = username
                player_frame = tk.LabelFrame(self.main_frame, text=player_name)
                player_frame.pack(pady=self.PAD)

                self.money_label = tk.Label(player_frame, text=f'Money: {user_money}')
                self.money_label.grid(row=0)
                row = 1

            else:
                player_name = f'{PLAYER} #{player_num + 1}'
                player_frame = tk.LabelFrame(self.main_frame, text=player_name)
                player_frame.pack(pady=self.PAD)
                row = 0

            # Player's cards
            blank_img = card.get_blank_card_image()
            curr_player_cards_labels = []
            for spot in range(self.CARD_TOTAL_SPOTS):
                card_label = tk.Label(player_frame, text='', image=blank_img)
                card_label.grid(row=row, column=spot, padx=self.PAD, pady=self.PAD)
                curr_player_cards_labels.append(card_label)
                # anchor img to object
                curr_player_cards_labels[spot].image = blank_img

            self.players_cards_labels.append(curr_player_cards_labels)

    def _make_bet_frame(self, username):
        frame = tk.LabelFrame(self.main_frame)
        frame.pack(side=tk.LEFT)

        text_label = tk.Label(frame, text=f'{username}\'s bet:', font=('arial', 10, 'bold', 'underline'))
        text_label.pack(padx=self.PAD, pady=self.PAD, side=tk.LEFT)

        self.plus_icn = tk.PhotoImage(file=ICN_PLUS_PATH)
        self.plus_btn = Button(frame, command=self._plus_btn_clicked, image=self.plus_icn)
        self.plus_btn.pack(padx=self.PAD, pady=self.PAD, side=tk.LEFT)

        self.bet_label = tk.Label(frame, text=str(MIN_BET))
        self.bet_label.pack(padx=self.PAD, pady=self.PAD, side=tk.LEFT)

        self.minus_icn = tk.PhotoImage(file=ICN_MINUS_PATH)
        self.minus_btn = Button(frame, command=self._minus_btn_clicked, image=self.minus_icn)
        self.minus_btn.pack(padx=self.PAD, pady=self.PAD, side=tk.LEFT)

    def _plus_btn_clicked(self):
        curr_bet = float(self.bet_label[TEXT])
        if curr_bet >= MAX_BET:
            return
        else:
            curr_bet += 5.0
            self.bet_label[TEXT] = curr_bet

    def _minus_btn_clicked(self):
        curr_bet = float(self.bet_label[TEXT])
        if curr_bet <= MIN_BET:
            return
        else:
            curr_bet -= 5.0
            self.bet_label[TEXT] = curr_bet

    def get_player_bet(self):
        return float(self.bet_label[TEXT])

    def change_buttons_state(self):
        if self.plus_btn[STATE] == tk.DISABLED:
            self.plus_btn[STATE] = tk.DISABLED
            self.minus_btn[STATE] = tk.DISABLED
        else:
            self.plus_btn[STATE] = tk.NORMAL
            self.minus_btn[STATE] = tk.NORMAL
