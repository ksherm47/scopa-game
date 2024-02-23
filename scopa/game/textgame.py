from scopa.game.basegame import ScopaGame
from scopa.player import ScopaPlayer
from scopa.strategy import ScopaMove


class TextBasedScopaGame(ScopaGame):

    def new_deck_event(self, scores: dict[ScopaPlayer, int]):
        print('No winner yet')
        print([f'{player}: {score}' for player, score in scores.items()])
        print()

    def dealing_players_event(self, dealer: ScopaPlayer):
        print(f'-----DEALING CARDS ({dealer} is the Dealer)-----')

    def begin_player_turn_event(self, player: ScopaPlayer):
        print()
        print(f'Player Turn: {player}')
        print(f'Board: {[str(card) for card in self.board]}')
        if player.show_hand():
            print(f'Player {player} hand: {[str(card) for card in player.get_hand()]}')

    def invalid_move_event(self, error: ValueError):
        print(f'Invalid move: {error}')

    def move_made_event(self, move: ScopaMove):
        print(f'Move made: {move}')

    def scopa_event(self):
        print('SCOPA!!!!!!!!!!!!!!')

    def post_move_event(self, player: ScopaPlayer):
        if player.show_hand():
            print(f'New hand: {[str(card) for card in player.get_hand()]}')

    def ending_event(self, winners: list[ScopaPlayer], scores: dict[ScopaPlayer, int]):
        final_scores = [f'{player}: {score}' for player, score in scores.items()]
        if len(winners) > 1:
            print(' and '.join(str(w) for w in winners) + f' tie! Final scores: {final_scores}')
            return

        print(f'{winners[0]} wins! Final scores: {final_scores}')