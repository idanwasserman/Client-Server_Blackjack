from PIL import Image, ImageTk

SUITS = ['diamonds', 'clubs', 'hearts', 'spades']
VALUES = range(2, 15)  # 11 = J, 12 = Q, 13 = K, 14 = A
CARDS_IMAGES_PATH = r'C:\seminar_client_server\Client-Server_Blackjack\images\cards'


class Card(dict):

    def __init__(self, suit, value):
        text = f'{value}_of_{suit}'
        img_path = CARDS_IMAGES_PATH + f'\\{text}.png'
        real_value = _compute_blackjack_value(value)
        dict.__init__(self, suit=suit, value=value, text=text, real_value=real_value, path=img_path)


def create_deck(num_of_decks):
    deck = []
    for i in range(num_of_decks):
        for suit in SUITS:
            for value in VALUES:
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
    if value <= 0 or value > 14:
        raise Exception(f"Illegal card value: {value}")

    # if the card is between 2-10
    if value <= 10:
        return value
    # if the card is 'Ace'
    if value == 14:
        return 11
    # if the card is royal card
    else:
        return 10
