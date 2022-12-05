from game import ScopaGame
from player import ScopaPlayer


def main():
    kenny = ScopaPlayer('Kenny')
    brenna = ScopaPlayer('Brenna')

    game = ScopaGame(players=[kenny, brenna])
    game.start_game()


if __name__ == '__main__':
    main()
