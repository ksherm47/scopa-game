from game import ScopaGame
from player import ScopaPlayer


def main():
    kenny = ScopaPlayer('Kenny', human=True)
    brenna = ScopaPlayer('Brenna', show_hand=False)
    andreas = ScopaPlayer('Andreas', show_hand=False)

    game = ScopaGame(players=[brenna, kenny, andreas], winning_score=11, board_size=8)
    game.start_game()


if __name__ == '__main__':
    main()
