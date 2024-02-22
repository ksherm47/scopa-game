import re

from cards import ScopaCardRank, ScopaCard, ScopaCardSuit
from strategy import ScopaMove, ScopaMoveType

__HAND_CARD = "hand_card"
__BOARD_CARDS = "board_cards"
__MOVE_TYPE = "move_type"

__MOVE_TYPE_FORMAT = fr'(?P<{__MOVE_TYPE}>[TtDd])'
__SCOPA_CARD_FORMAT = '[aA234567JjQqKk](([Cc][Uu])|([Cc][Oo])|([Ss][Ww]?)|([Cc][Ll]))'
__HAND_CARD_FORMAT = fr'(?P<{__HAND_CARD}>{__SCOPA_CARD_FORMAT})'
__BOARD_CARDS_FORMAT = fr'(?P<{__BOARD_CARDS}>{__SCOPA_CARD_FORMAT}(,{__SCOPA_CARD_FORMAT})*)'

__SCOPA_MOVE_FORMAT = fr'{__MOVE_TYPE_FORMAT},{__HAND_CARD_FORMAT}(,{__BOARD_CARDS_FORMAT})?'

__STR_TO_TYPE = {
    't': ScopaMoveType.TAKE,
    'd': ScopaMoveType.DISCARD
}

__STR_TO_RANK = {
    'a': ScopaCardRank.ACE,
    '2': ScopaCardRank.TWO,
    '3': ScopaCardRank.THREE,
    '4': ScopaCardRank.FOUR,
    '5': ScopaCardRank.FIVE,
    '6': ScopaCardRank.SIX,
    '7': ScopaCardRank.SEVEN,
    'j': ScopaCardRank.JACK,
    'q': ScopaCardRank.QUEEN,
    'k': ScopaCardRank.KING
}

__STR_TO_SUIT = {
    'cu': ScopaCardSuit.CUPS,
    'co': ScopaCardSuit.COINS,
    's': ScopaCardSuit.SWORDS,
    'sw': ScopaCardSuit.SWORDS,
    'cl': ScopaCardSuit.CLUBS
}


def parse_move(move_str: str) -> ScopaMove:
    move_str = move_str.strip()
    match = re.match(__SCOPA_MOVE_FORMAT, move_str)
    if not match:
        raise ValueError('Move string is not valid')

    move_type = __STR_TO_TYPE[match.group(__MOVE_TYPE).lower()]
    hand_card = __parse_card_str(match.group(__HAND_CARD).lower())

    board_cards_str = match.group(__BOARD_CARDS)
    board_cards = None
    if board_cards_str:
        board_cards = [__parse_card_str(card) for card in board_cards_str.lower().split(',')]

    return ScopaMove(move_type, hand_card, board_cards=board_cards)


def __parse_card_str(card_str) -> ScopaCard:
    return ScopaCard(__STR_TO_RANK[card_str[0]], __STR_TO_SUIT[card_str[1:]])


