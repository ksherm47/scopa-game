from cards import ScopaCard, ScopaSuit
from strategy import ScopaStrategy, ScopaMove


class ScopaPlayer:

    def __init__(self, name, strategy: str = 'default', human: bool = False):
        self.__hand = []
        self.__captures = set()
        self.__strategy = ScopaStrategy(strategy)
        self.__name = name
        self.__human = human
        self.__coins_captured = 0

    def hand_is_empty(self) -> bool:
        return not self.__hand

    def make_move(self, scopa_board: list[ScopaCard]) -> ScopaMove:
        if not self.__human:
            move = self.__strategy.make_move(scopa_board, self.__hand)
        else:
            move = None
        return move

    def name(self) -> str:
        return self.__name

    def deal_card(self, card: ScopaCard):
        self.__hand.append(card)

    def remove_hand_card(self, card: ScopaCard):
        self.__hand.remove(card)

    def capture_card(self, card: ScopaCard):
        if card.suit() == ScopaSuit.COINS:
            self.__coins_captured += 1
        self.__captures.add(card)

    def capture_cards(self, cards: list[ScopaCard]):
        for card in cards:
            self.capture_card(card)

    def get_captured_cards(self) -> set[ScopaCard]:
        return self.__captures

    def get_num_coins_captured(self) -> int:
        return self.__coins_captured

    def get_hand(self) -> list[ScopaCard]:
        return list(self.__hand)

    def __str__(self):
        return self.__name
