import tkinter as tk

from scopa.game.basegame import ScopaGame
from scopa.game.gui import ScopaBoardGui
from scopa.player import ScopaPlayer
from scopa.strategy import ScopaMove


class GuiBasedScopaGame(ScopaGame):

    def __init__(self, scopa_gui: ScopaBoardGui, players: list[ScopaPlayer] = None, winning_score: int = 11,
                 hand_size: int = 3, board_size: int = 4):
        super().__init__(players=players, winning_score=winning_score, hand_size=hand_size, board_size=board_size)
        self.scopa_gui = scopa_gui

    def new_deck_event(self, scores: dict[ScopaPlayer, int]):
        ...

    def dealing_players_event(self, dealer: ScopaPlayer):
        ...

    def begin_player_turn_event(self, player: ScopaPlayer):
        ...

    def invalid_move_event(self, error: ValueError):
        ...

    def move_made_event(self, move: ScopaMove):
        ...

    def scopa_event(self):
        ...

    def post_move_event(self, player: ScopaPlayer):
        ...

    def ending_event(self, winners: list[ScopaPlayer], scores: dict[ScopaPlayer, int]):
        ...