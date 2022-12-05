from cards import ScopaCard
from strategy import ScopaStrategy, ScopaMove


class ScopaPlayer:

    def __init__(self, name, strategy: str = 'default', human=False):
        self.__hand = []
        self.__strategy = ScopaStrategy(strategy)
        self.__name = name
        self.__human = human

    def hand_is_empty(self) -> bool:
        return not self.__hand

    def make_move(self, scopa_board: list[ScopaCard]) -> ScopaMove:
        if not self.__human:
            move = self.__strategy.make_move(scopa_board, self.__hand)
        else:
            move = None
        return move

    def name(self):
        return self.__name
