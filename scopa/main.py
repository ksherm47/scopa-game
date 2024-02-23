from scopa.game.gui import ScopaBoardGui
from scopa.game.textgame import TextBasedScopaGame
from scopa.game.guigame import GuiBasedScopaGame
from player import ScopaPlayer
import argparse


def main(args):
    kenny = ScopaPlayer('Kenny', human=True)
    brenna = ScopaPlayer('Brenna', show_hand=False)
    andreas = ScopaPlayer('Andreas', show_hand=False)
    players = [kenny, brenna, andreas]

    game = TextBasedScopaGame(players=players) if args.text else GuiBasedScopaGame(ScopaBoardGui(players), players=players)

    game.start_game()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', action='store_true')
    main(parser.parse_args())
