from cards import *
from player import ScopaPlayer


class ScopaGame:

    def __init__(self, players: list[ScopaPlayer] = None, winning_score: int = 11):

        self.__deck = ScopaDeck()
        self.__deck.shuffle()
        self.__players = [] if players is None else players
        self.__winning_score = winning_score

    def add_player(self, player: ScopaPlayer):
        self.__players.append(player)

    def __winner_exists(self, scores: dict[ScopaPlayer, int]) -> bool:
        for player, score in scores.items():
            if score >= self.


    def start_game(self):
        if len(self.__players) < 2:
            raise ValueError('Number of players must be greater than or equal to 2')

        scores = {player: 0 for player in self.__players}
        while
