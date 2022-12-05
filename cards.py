from enum import IntEnum, Enum
import random


class ScopaSuit(Enum):
    COINS = 0,
    CUPS = 1,
    SWORDS = 2,
    CLUBS = 3


class ScopaRank(IntEnum):
    ACE = 1,
    TWO = 2,
    THREE = 3,
    FOUR = 4,
    FIVE = 5,
    SIX = 6,
    SEVEN = 7,
    JACK = 8,
    QUEEN = 9,
    KING = 10


def get_prime_points(rank: ScopaRank) -> int:
    if rank == ScopaRank.ACE:
        return 16
    if rank == ScopaRank.TWO:
        return 12
    if rank == ScopaRank.THREE:
        return 13
    if rank == ScopaRank.FOUR:
        return 14
    if rank == ScopaRank.FIVE:
        return 15
    if rank == ScopaRank.SIX:
        return 18
    if rank == ScopaRank.SEVEN:
        return 21
    if rank == ScopaRank.JACK or rank == ScopaRank.QUEEN or rank == ScopaRank.KING:
        return 10


class ScopaCard:

    def __init__(self, rank: ScopaRank, suit: ScopaSuit):
        self.__rank = rank
        self.__suit = suit

    def rank(self) -> ScopaRank:
        return self.__rank

    def suit(self) -> ScopaSuit:
        return self.__suit

    def __rank_str(self):
        if self.__rank == ScopaRank.ACE:
            return 'A'
        if self.__rank == ScopaRank.TWO:
            return '2'
        if self.__rank == ScopaRank.THREE:
            return '3'
        if self.__rank == ScopaRank.FOUR:
            return '4'
        if self.__rank == ScopaRank.FIVE:
            return '5'
        if self.__rank == ScopaRank.SIX:
            return '6'
        if self.__rank == ScopaRank.SEVEN:
            return '7'
        if self.__rank == ScopaRank.JACK:
            return 'J'
        if self.__rank == ScopaRank.QUEEN:
            return 'Q'
        if self.__rank == ScopaRank.KING:
            return 'K'

    def __suit_str(self):
        if self.__suit == ScopaSuit.COINS:
            return '\u25ef'
        if self.__suit == ScopaSuit.CUPS:
            return '\U0001F377'
        if self.__suit == ScopaSuit.CLUBS:
            return '\u2663'
        if self.__suit == ScopaSuit.SWORDS:
            return '\u2694'

    def __str__(self):
        return f'{self.__rank_str()}{self.__suit_str()}'

    def __eq__(self, other_card):
        return self.__suit == other_card.__suit and self.__rank == other_card.__rank

    def __hash__(self):
        return hash((self.__rank, self.__suit))


class ScopaDeck:

    def __init__(self):
        self.__cards = self.__get_new_deck()

    def __get_new_deck(self) -> list[ScopaCard]:
        deck = [ScopaCard(rank, suit) for rank in ScopaRank for suit in ScopaSuit]
        return deck

    def shuffle(self):
        random.shuffle(self.__cards)

    def draw_card(self) -> ScopaCard:
        if self.__cards:
            return self.__cards.pop(0)

    def cards_left(self) -> bool:
        return len(self.__cards) > 0

    def refresh_deck(self):
        self.__cards = self.__get_new_deck()



