import tkinter as tk

from scopa.player import ScopaPlayer

WINDOW_TITLE = 'SCOPA!'


class ScopaBoardGui:

    def __init__(self, players: list[ScopaPlayer]):
        self.players = players

        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE)
