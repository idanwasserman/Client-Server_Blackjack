from PIL import Image, ImageTk

SUITS = ['diamonds', 'clubs', 'hearts', 'spades']
VALUES = range(2, 15)  # 11 = J, 12 = Q, 13 = K, 14 = A
CARDS_IMAGES_PATH = r'C:\seminar_client_server\Client-Server_Blackjack\images\cards'


def _get_resized_image(path):
    # Open image
    card_img = Image.open(path)
    # Resize image
    resized_card_img = card_img.resize((70, 100))
    return ImageTk.PhotoImage(resized_card_img)


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


class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.text = f'{value}_of_{suit}'
        img_path = CARDS_IMAGES_PATH + f'\\{self.text}.png'
        self.image = _get_resized_image(img_path)
        self.real_value = _compute_blackjack_value(value)

    def __str__(self):
        return f'Card: {self.value} of {self.suit}'

    @staticmethod
    def create_deck(num_of_decks):
        deck = []
        for i in range(num_of_decks):
            for suit in SUITS:
                for value in VALUES:
                    new_card = Card(value=value, suit=suit)
                    deck.append(new_card)
        return deck

    @staticmethod
    def get_blank_card_image():
        return _get_resized_image(CARDS_IMAGES_PATH + '\\blank.png')

    @staticmethod
    def get_question_mark_card_image():
        return _get_resized_image(CARDS_IMAGES_PATH + '\\question_mark.png')
