from scopa.cards import *
from scopa.player import ScopaPlayer
from scopa.strategy import ScopaMove, ScopaMoveType
import sys
from abc import ABC, abstractmethod


class ScopaGame(ABC):

    def __init__(self, players: list[ScopaPlayer] = None,
                 winning_score: int = 11,
                 hand_size: int = 3,
                 board_size: int = 4):
        self.deck = ScopaDeck()
        self.deck.shuffle()
        self.board = []
        self.players = [] if players is None else players
        self.winning_score = winning_score
        self.hand_size = hand_size
        self.board_size = board_size

    @abstractmethod
    def new_deck_event(self, scores: dict[ScopaPlayer, int]):
        ...

    @abstractmethod
    def dealing_players_event(self, dealer: ScopaPlayer):
        ...

    @abstractmethod
    def begin_player_turn_event(self, player: ScopaPlayer):
        ...

    @abstractmethod
    def invalid_move_event(self, error: ValueError):
        ...

    @abstractmethod
    def move_made_event(self, move: ScopaMove):
        ...

    @abstractmethod
    def scopa_event(self):
        ...

    @abstractmethod
    def post_move_event(self, player: ScopaPlayer):
        ...

    @abstractmethod
    def ending_event(self, winners: list[ScopaPlayer], scores: dict[ScopaPlayer, int]):
        ...

    def add_player(self, player: ScopaPlayer):
        self.players.append(player)

    def start_game(self):
        if len(self.players) < 2:
            raise ValueError('Number of players must be greater than or equal to 2')

        scores = {player: 0 for player in self.players}
        winners = []

        while not winners:
            self.new_deck_event(scores)
            self.__reset_players()
            self.deck.refresh_deck()
            self.deck.shuffle()
            self.__deal_board()

            while self.deck.cards_left():
                self.dealing_players_event(self.players[0])
                self.__deal_players()
                for _ in range(self.hand_size):
                    for player in self.players:
                        self.begin_player_turn_event(player)
                        while True:
                            try:
                                move = player.make_move(self.board)
                                self.__evaluate_move(move, player)
                                break
                            except ValueError as ve:
                                self.invalid_move_event(ve)

                        self.move_made_event(move)
                        if not self.board:
                            self.scopa_event()
                            player.add_scopa()
                        self.post_move_event(player)

                # Change dealer
                self.players.append(self.players.pop(0))
                print()

            self.__update_scores(scores)
            winners = self.__winning_players(scores)

        self.ending_event(winners, scores)

    def __winning_players(self, scores: dict[ScopaPlayer, int]):
        best_score = max(scores.values())
        if best_score >= self.winning_score:
            return [player for player, score in scores.items() if score == best_score]
        return None

    def __deal_board(self):
        self.board = []
        for _ in range(self.board_size):
            self.board.append(self.deck.draw_card())

    def __deal_players(self):
        for _ in range(self.hand_size):
            for player in self.players:
                player.deal_card(self.deck.draw_card())

    def __reset_players(self):
        for player in self.players:
            player.reset()

    def __evaluate_move(self, move: ScopaMove, player: ScopaPlayer):
        mt = move.move_type()
        if move.move_type() == ScopaMoveType.TAKE:
            self.__validate_take_move(move, player)

            player.capture_card(move.hand_card())
            player.capture_cards(move.board_cards())

            player.remove_hand_card(move.hand_card())
            for board_card in move.board_cards():
                self.board.remove(board_card)

            return

        if move.move_type() == ScopaMoveType.DISCARD:
            self.__validate_discard_move(move, player)
            self.board.append(move.hand_card())
            player.remove_hand_card(move.hand_card())
            return

        raise ValueError(f'Invalid move type {move.move_type()}')

    def __validate_take_move(self, move: ScopaMove, player: ScopaPlayer):
        if move.hand_card() not in player.get_hand():
            raise ValueError(f'{move.hand_card()} not in {player}\'s hand')

        for board_card in move.board_cards():
            if board_card not in self.board:
                raise ValueError(f'{board_card} is not on the board')

        if sum([board_card.rank() for board_card in move.board_cards()]) != move.hand_card().rank():
            raise ValueError('Board card ranks do not add up to hand card rank')

    @staticmethod
    def __validate_discard_move(move: ScopaMove, player: ScopaPlayer):
        if move.hand_card() not in player.get_hand():
            raise ValueError(f'{move.hand_card()} not in {player}\'s hand')

    def __update_scores(self, scores: dict[ScopaPlayer, int]):
        # Scopas
        for player in self.players:
            scores[player] += player.get_scopa_count()
            print(f'{player} got {player.get_scopa_count()} scopas ({scores[player]})')

        # Card Count
        most_cards, most_cards_player = -sys.maxsize, None
        for player in self.players:
            num_captured = len(player.get_captured_cards())
            most_cards, most_cards_player = max((most_cards, most_cards_player), (num_captured, player),
                                                key=lambda x: x[0])
        scores[most_cards_player] += 1
        print(f'{most_cards_player} has most cards ({scores[most_cards_player]})')

        # Coin Count
        most_coins, most_coins_player = -sys.maxsize, None
        for player in self.players:
            num_coins = player.get_num_coins_captured()
            most_coins, most_coins_player = max((most_coins, most_coins_player), (num_coins, player),
                                                key=lambda x: x[0])
        scores[most_coins_player] += 1
        print(f'{most_coins_player} has most coins ({scores[most_coins_player]})')

        # Seven of Coins
        for player in self.players:
            if ScopaCard(ScopaCardRank.SEVEN, ScopaCardSuit.COINS) in player.get_captured_cards():
                scores[player] += 1
                print(f'{player} got the 7 of Coins ({scores[player]})')
                break

        # Primes
        highest_prime_sum, highest_prime_sum_player = -sys.maxsize, None
        for player in self.players:
            prime_sum = 0
            for suit in ScopaCardSuit:
                suit_cards = [card for card in player.get_captured_cards() if card.suit() == suit]
                prime_sum += max([get_prime_points(card.rank()) for card in suit_cards]) if suit_cards else 0
            highest_prime_sum, highest_prime_sum_player = max((highest_prime_sum, highest_prime_sum_player),
                                                              (prime_sum, player), key=lambda x: x[0])
        scores[highest_prime_sum_player] += 1
        print(f'{highest_prime_sum_player} has highest prime score ({scores[highest_prime_sum_player]})')

