from cards import *
from player import ScopaPlayer
from strategy import ScopaMove, ScopaMoveType
import sys


class ScopaGame:

    def __init__(self, players: list[ScopaPlayer] = None,
                 winning_score: int = 11,
                 hand_size: int = 3,
                 board_size: int = 4):
        self.__deck = ScopaDeck()
        self.__deck.shuffle()
        self.__board = []
        self.__players = [] if players is None else players
        self.__winning_score = winning_score
        self.__hand_size = hand_size
        self.__board_size = board_size

    def add_player(self, player: ScopaPlayer):
        self.__players.append(player)

    def start_game(self):
        if len(self.__players) < 2:
            raise ValueError('Number of players must be greater than or equal to 2')

        scores = {player: 0 for player in self.__players}
        winner = None

        while not winner:
            print('No winner yet')
            print([f'{player}: {score}' for player, score in scores.items()])
            self.__deck.refresh_deck()
            self.__deck.shuffle()
            self.__deal_board()
            while self.__deck.cards_left():
                self.__deal_players()
                print()
                for _ in range(self.__hand_size):
                    for player in self.__players:
                        print()
                        print(f'Board: {[str(card) for card in self.__board]}')
                        print(f'Player {player} hand: {[str(card) for card in  player.get_hand()]}')
                        move = player.make_move(self.__board)
                        print(f'Move made: {move}')
                        self.__evaluate_move(move, player, scores)
                        print(f'New hand: {[str(card) for card in  player.get_hand()]}')

            self.__update_scores(scores)
            winner = self.__winning_player(scores)

        print(f'{winner} wins! Final scores: {[f"{player}: {score}" for player, score in scores.items()]}')

    def __winning_player(self, scores: dict[ScopaPlayer, int]):
        for player, score in scores.items():
            if score >= self.__winning_score:
                return player
        return None

    def __deal_board(self):
        for _ in range(self.__board_size):
            self.__board.append(self.__deck.draw_card())

    def __deal_players(self):
        for _ in range(self.__hand_size):
            for player in self.__players:
                player.deal_card(self.__deck.draw_card())

    def __evaluate_move(self, move: ScopaMove, player: ScopaPlayer, scores: dict[ScopaPlayer, int]):
        if move.move_type() == ScopaMoveType.TAKE:
            player.capture_card(move.hand_card())
            player.capture_cards(move.board_cards())

            player.remove_hand_card(move.hand_card())
            for board_card in move.board_cards():
                self.__board.remove(board_card)

            if not self.__board:
                scores[player] += 1
            return

        if move.move_type() == ScopaMoveType.DISCARD:
            self.__board.append(move.hand_card())
            player.remove_hand_card(move.hand_card())
            return

        raise ValueError(f'Invalid move type f{move.move_type()}')

    def __update_scores(self, scores: dict[ScopaPlayer, int]):
        # Card Count
        most_cards, most_cards_player = -sys.maxsize, None
        for player in self.__players:
            num_captured = len(player.get_captured_cards())
            most_cards, most_cards_player = max((most_cards, most_cards_player), (num_captured, player),
                                                key=lambda x: x[0])
        scores[most_cards_player] += 1

        # Coin Count
        most_coins, most_coins_player = -sys.maxsize, None
        for player in self.__players:
            num_coins = player.get_num_coins_captured()
            most_coins, most_coins_player = max((most_coins, most_coins_player), (num_coins, player),
                                                key=lambda x: x[0])
        scores[most_coins_player] += 1

        # Seven of Coins
        for player in self.__players:
            if ScopaCard(ScopaRank.SEVEN, ScopaSuit.COINS) in player.get_captured_cards():
                scores[player] += 1
                break

        # Primes
        highest_prime_sum, highest_prime_sum_player = -sys.maxsize, None
        for player in self.__players:
            prime_sum = 0
            for suit in ScopaSuit:
                prime_sum += max([get_prime_points(card.rank()) for card in player.get_captured_cards()
                                  if card.suit() == suit])
            highest_prime_sum, highest_prime_sum_player = max((highest_prime_sum, highest_prime_sum_player),
                                                              (prime_sum, player), key=lambda x: x[0])
        scores[highest_prime_sum_player] += 1
