from PIL import Image, ImageTk
from constants import *

SUITS = [DIAMONDS, CLUBS, HEARTS, SPADES]
VALUES = range(2, 15)  # 11 = J, 12 = Q, 13 = K, 14 = A
CARDS_IMAGES_PATH = r'C:\seminar_client_server\Client-Server_Blackjack\images\cards'


class Card(dict):

    def __init__(self, suit, value):
        text = f'{value}_of_{suit}'
        img_path = CARDS_IMAGES_PATH + f'\\{text}.png'
        real_value = _compute_blackjack_value(value)
        dict.__init__(self, suit=suit, value=value, text=text, real_value=real_value, path=img_path)


class Ace_Card(Card):

    ACE_VALUE = 14

    def __init__(self, suit):
        super().__init__(suit, Ace_Card.ACE_VALUE)
        self[HIGH_VALUE] = True


def create_deck(num_of_decks):
    deck = []
    for i in range(num_of_decks):
        for suit in SUITS:
            for value in VALUES:
                if value == Ace_Card.ACE_VALUE:
                    new_card = Ace_Card(suit=suit)
                else:
                    new_card = Card(value=value, suit=suit)
                deck.append(new_card)
    return deck


def get_resized_image(path):
    # Open image
    card_image = Image.open(path)
    # Resize image
    resized_card_img = card_image.resize((70, 100))
    return ImageTk.PhotoImage(resized_card_img)


def get_blank_card_image():
    return get_resized_image(CARDS_IMAGES_PATH + '\\blank.png')


def get_question_mark_card_image():
    return get_resized_image(CARDS_IMAGES_PATH + '\\question_mark.png')


def _compute_blackjack_value(value):
    if value <= 0 or value > Ace_Card.ACE_VALUE:
        raise Exception(f"Illegal card value: {value}")

    # if the card is between 2-10
    if value <= 10:
        return value
    # if the card is 'Ace'
    if value == Ace_Card.ACE_VALUE:
        return 11
    # if the card is royal card
    else:
        return 10
