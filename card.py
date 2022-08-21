from PIL import Image, ImageTk
from constants import *

SUITS = [DIAMONDS, CLUBS, HEARTS, SPADES]
VALUES = range(2, 15)  # 11 = J, 12 = Q, 13 = K, 14 = A
CARDS_IMAGES_PATH = r'C:\seminar_client_server\Client-Server_Blackjack\images\cards'
CARD_SIZE = (70, 100)


class Card(dict):
    """
    A class (that inherits dict class) used to represent a Game Card

    ...

    Attributes
    ----------
    suit : str
        the card's suit (DIAMONDS, CLUBS, HEARTS or SPADES)
    value : str
        the card's value (a number in the range 2-14)
    """

    def __init__(self, suit, value):
        # text = a formatted string to represent the specific card in a deck
        text = f'{value}_of_{suit}'

        # img_path = the path to the card's image
        img_path = CARDS_IMAGES_PATH + f'\\{text}.png'

        # real_value = the real card's value in a Blackjack game
        real_value = _compute_blackjack_value(value)

        dict.__init__(self, suit=suit, value=value, text=text, real_value=real_value, path=img_path)


class Ace_Card(Card):
    """
    A class (that inherits dict class) used to represent the Ace Game Card

    ...

    Attributes
    ----------
    suit : str
        the card's suit (DIAMONDS, CLUBS, HEARTS or SPADES)
    """
    ACE_VALUE = 14

    def __init__(self, suit):
        super().__init__(suit, Ace_Card.ACE_VALUE)

        # high_value = a boolean indicated if the card's real value is high (11) or low (1)
        self[HIGH_VALUE] = True


def create_deck(num_of_decks=1):
    """
    A simple function that creates some 52-cards regular decks

    Parameters
    ----------
    num_of_decks : int
        The number of decks to create (default is 1)

    Returns
    -------
    list
        a list contains at least one deck

    Raises
    -------
    Exception
        if num_of_decks is lower than 1
    """

    if num_of_decks < 1:
        raise Exception(f'Cannot create {num_of_decks} decks')

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
    """
    A function that returns a resized image from a specific path for tkinter GUI

    Parameters
    ----------
    path : str
        The path to the image

    Returns
    -------
    PhotoImage
        the resized photo image
    """

    # Open image
    card_image = Image.open(path)
    # Resize image
    resized_card_img = card_image.resize(CARD_SIZE)
    return ImageTk.PhotoImage(resized_card_img)


def get_blank_card_image():
    """Returns an image of a blank card"""
    return get_resized_image(CARDS_IMAGES_PATH + '\\blank.png')


def get_question_mark_card_image():
    """Returns an image of a question mark card"""
    return get_resized_image(CARDS_IMAGES_PATH + '\\question_mark.png')


def _compute_blackjack_value(value):
    """
    A function that computes the real card's value in a Blackjack game

    Parameters
    ----------
    value : int
        The card's value

    Returns
    -------
    int
        the real card's value in a Blackjack game
    """

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
