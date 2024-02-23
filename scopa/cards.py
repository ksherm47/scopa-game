from enum import IntEnum, Enum
import random


class ScopaCardSuit(Enum):
    COINS = 0,
    CUPS = 1,
    SWORDS = 2,
    CLUBS = 3


class ScopaCardRank(IntEnum):
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


__PRIME_POINTS = {
    ScopaCardRank.ACE: 16,
    ScopaCardRank.TWO: 12,
    ScopaCardRank.THREE: 13,
    ScopaCardRank.FOUR: 14,
    ScopaCardRank.FIVE: 15,
    ScopaCardRank.SIX: 18,
    ScopaCardRank.SEVEN: 21,
    ScopaCardRank.JACK: 10,
    ScopaCardRank.QUEEN: 10,
    ScopaCardRank.KING: 10
}


def get_prime_points(rank: ScopaCardRank) -> int:
    return __PRIME_POINTS[rank]


class ScopaCard:

    __rank_strs = {
        ScopaCardRank.ACE: 'A',
        ScopaCardRank.TWO: '2',
        ScopaCardRank.THREE: '3',
        ScopaCardRank.FOUR: '4',
        ScopaCardRank.FIVE: '5',
        ScopaCardRank.SIX: '6',
        ScopaCardRank.SEVEN: '7',
        ScopaCardRank.JACK: 'J',
        ScopaCardRank.QUEEN: 'Q',
        ScopaCardRank.KING: 'K'
    }

    __suit_strs = {
        ScopaCardSuit.COINS: '\u25ef',
        ScopaCardSuit.CUPS: '\U0001F377',
        ScopaCardSuit.CLUBS: '\u2663',
        ScopaCardSuit.SWORDS: '\u2694'
    }

    def __init__(self, rank: ScopaCardRank, suit: ScopaCardSuit):
        self.__rank = rank
        self.__suit = suit

    def rank(self) -> ScopaCardRank:
        return self.__rank

    def suit(self) -> ScopaCardSuit:
        return self.__suit

    def __str__(self):
        return f'{ScopaCard.__rank_strs[self.__rank]}{ScopaCard.__suit_strs[self.__suit]}'

    def __eq__(self, other_card):
        return self.__suit == other_card.__suit and self.__rank == other_card.__rank

    def __hash__(self):
        return hash((self.__rank, self.__suit))


class ScopaDeck:

    def __init__(self):
        self.__cards = [ScopaCard(rank, suit) for rank in ScopaCardRank for suit in ScopaCardSuit]

    def shuffle(self):
        random.shuffle(self.__cards)

    def draw_card(self) -> ScopaCard:
        if self.__cards:
            return self.__cards.pop(0)

    def cards_left(self) -> bool:
        return len(self.__cards) > 0

    def refresh_deck(self):
        self.__cards = [ScopaCard(rank, suit) for rank in ScopaCardRank for suit in ScopaCardSuit]



