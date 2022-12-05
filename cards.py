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
    elif rank == ScopaRank.TWO:
        return 12
    elif rank == ScopaRank.THREE:
        return 13
    elif rank == ScopaRank.FOUR:
        return 14
    elif rank == ScopaRank.FIVE:
        return 15
    elif rank == ScopaRank.SIX:
        return 18
    elif rank == ScopaRank.SEVEN:
        return 21
    elif rank == ScopaRank.JACK or rank == ScopaRank.QUEEN or rank == ScopaRank.KING:
        return 10


class ScopaCard:

    def __init__(self, rank: ScopaRank, suit: ScopaSuit):
        self.__rank = rank
        self.__suit = suit

    def rank(self) -> ScopaRank:
        return self.__rank

    def suit(self) -> ScopaSuit:
        return self.__suit

    def __str__(self):
        return f'{self.__rank.name} of {self.__suit.name}'


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



