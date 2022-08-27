"""
This file contains constants used by other scripts
"""

# Buttons captions
START = 'Start'
HIT = 'Hit'
STAND = 'Stand'
QUIT = 'Quit'
CREATE_TABLE = 'Create table'

# Keys of data passing between modules
HIT_CARD = 'hit_card'
IMAGE = 'image'
SWITCHER = 'switcher'
CARD = 'card'
SPOT = 'spot'
PLAYER_NUM = 'player_num'
SHOW_MSG = 'show_message'
MSG = 'message'
IS_OVER = 'is_over'
DEALER_CARDS = 'dealer_cards'
DEALER_SPOTS = 'dealer_spots'
PLAYERS_CARDS = 'players_cards'
PLAYERS_SPOTS = 'players_spots'
PLAYERS = 'players'
NEW_GAME = 'new_game'
NEW_GAME_MSG = 'new_game_message'
BOOL = 'boolean'
NUM_PLAYERS = 'num_of_players'
NUM_DECKS = 'num_of_decks'
ERROR = 'error'

# View
SERVER_TITLE = 'Blackjack Server'
TITLE = 'Blackjack-1.0'
DEALER = 'Dealer'
PLAYER = 'Player'
GREEN = 'green'
BLUE = 'blue'
RED = 'red'
BLACK = 'black'
LOST = 'Lost'
TIE = 'Tie'
WON = 'Won'
SCORES = 'Scores'
STATE = 'state'
NOTIFICATIONS = 'Notifications'
ICN_PLUS_PATH = r'images\icons\icn_plus.png'
ICN_MINUS_PATH = r'images\icons\icn_minus.png'

# Client/Server
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = '!DISCONNECT!'
DISCONNECTING = 'disconnecting'
MIN_PLAYERS = 1
MAX_PLAYERS = 3
MAX_CLIENTS = 3
MIN_USERNAME_LEN = 4

MAX_CARDS = 5
MIN_BET = 5.0
MAX_BET = 100.0
DEALER_TURN = 'dealer_turn'
GET_RESULTS = 'get_results'
RESULTS = 'results'
PRIZE = 'prize'
BET = 'bet'

# Card's attributes
SUIT = 'suit'
VALUE = 'value'
TEXT = 'text'
REAL_VALUE = 'real_value'
PATH = 'path'
HIGH_VALUE = 'high_value'

# card suits
DIAMONDS = 'diamonds'
CLUBS = 'clubs'
HEARTS = 'hearts'
SPADES = 'spades'

# User
USERNAME = 'username'
USER_MONEY = 'user_money'
STARTER_MONEY_AMOUNT = 1000.0

# guides
GUIDE = 'guide'
SERVER_GUIDE_TEXT = """This is a blackjack server.
Please enter your username,
and select how many players and decks are in the game.
If this is your first time playing,
just choose any username and start to play."""
CLIENT_GUIDE_TEXT = f"""This is a blackjack client.
Press [{START}] * - To start a new game.
Press [{HIT}] ** - To get another card from the dealer (You can get up to {MAX_CARDS} cards).
Press [{STAND}] ** - To finish current player's turn.
Press [{QUIT}] * - To exit from the game.

*   Cannot be clicked during a game!
**  Can be clicked (only) during a game!"""
