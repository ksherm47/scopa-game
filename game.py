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
        winners = []

        while not winners:
            print('No winner yet')
            print([f'{player}: {score}' for player, score in scores.items()])
            print()
            self.__reset_players()
            self.__deck.refresh_deck()
            self.__deck.shuffle()
            self.__deal_board()
            while self.__deck.cards_left():
                print(f'-----DEALING CARDS ({self.__players[0]} is the Dealer)-----')
                self.__deal_players()
                for _ in range(self.__hand_size):
                    for player in self.__players:
                        print()
                        print(f'Player Turn: {player}')
                        print(f'Board: {[str(card) for card in self.__board]}')
                        if player.show_hand():
                            print(f'Player {player} hand: {[str(card) for card in player.get_hand()]}')

                        move = None
                        valid_move = False
                        while not valid_move:
                            try:
                                move = player.make_move(self.__board)
                                self.__evaluate_move(move, player)
                                valid_move = True
                            except ValueError as ve:
                                print(f'Invalid move: {ve}')

                        print(f'Move made: {move}')
                        if player.show_hand():
                            print(f'New hand: {[str(card) for card in player.get_hand()]}')

                # Change dealer
                self.__players.append(self.__players.pop(0))
                print()

            self.__update_scores(scores)
            winners = self.__winning_players(scores)

        final_scores = [f'{player}: {score}' for player, score in scores.items()]
        if len(winners) == 1:
            print(f'{winners[0]} wins! Final scores: {final_scores}')
            return

        print(' and '.join(winners) + f' tie! Final scores: {final_scores}')

    def __winning_players(self, scores: dict[ScopaPlayer, int]):
        best_score = max(scores.values())
        if best_score >= self.__winning_score:
            return [player for player, score in scores.items() if score == best_score]
        return None

    def __deal_board(self):
        self.__board = []
        for _ in range(self.__board_size):
            self.__board.append(self.__deck.draw_card())

    def __deal_players(self):
        for _ in range(self.__hand_size):
            for player in self.__players:
                player.deal_card(self.__deck.draw_card())

    def __reset_players(self):
        for player in self.__players:
            player.reset()

    def __evaluate_move(self, move: ScopaMove, player: ScopaPlayer):
        if move.move_type() == ScopaMoveType.TAKE:
            self.__validate_take_move(move, player)

            player.capture_card(move.hand_card())
            player.capture_cards(move.board_cards())

            player.remove_hand_card(move.hand_card())
            for board_card in move.board_cards():
                self.__board.remove(board_card)

            if not self.__board:
                print('SCOPA!!!!!!!!!!!!!!')
                player.add_scopa()
            return

        if move.move_type() == ScopaMoveType.DISCARD:
            self.__validate_discard_move(move, player)
            self.__board.append(move.hand_card())
            player.remove_hand_card(move.hand_card())
            return

        raise ValueError(f'Invalid move type f{move.move_type()}')

    def __validate_take_move(self, move: ScopaMove, player: ScopaPlayer):
        if move.hand_card() not in player.get_hand():
            raise ValueError(f'{move.hand_card()} not in {player}\'s hand')

        for board_card in move.board_cards():
            if board_card not in self.__board:
                raise ValueError(f'{board_card} is not on the board')

        if sum([board_card.rank() for board_card in move.board_cards()]) != move.hand_card().rank():
            raise ValueError('Board card ranks do not add up to hand card rank')

    @staticmethod
    def __validate_discard_move(move: ScopaMove, player: ScopaPlayer):
        if move.hand_card() not in player.get_hand():
            raise ValueError(f'{move.hand_card()} not in {player}\'s hand')

    def __update_scores(self, scores: dict[ScopaPlayer, int]):
        # Scopas
        for player in self.__players:
            scores[player] += player.get_scopa_count()
            print(f'{player} got {player.get_scopa_count()} scopas ({scores[player]})')

        # Card Count
        most_cards, most_cards_player = -sys.maxsize, None
        for player in self.__players:
            num_captured = len(player.get_captured_cards())
            most_cards, most_cards_player = max((most_cards, most_cards_player), (num_captured, player),
                                                key=lambda x: x[0])
        scores[most_cards_player] += 1
        print(f'{most_cards_player} has most cards ({scores[most_cards_player]})')

        # Coin Count
        most_coins, most_coins_player = -sys.maxsize, None
        for player in self.__players:
            num_coins = player.get_num_coins_captured()
            most_coins, most_coins_player = max((most_coins, most_coins_player), (num_coins, player),
                                                key=lambda x: x[0])
        scores[most_coins_player] += 1
        print(f'{most_coins_player} has most coins ({scores[most_coins_player]})')

        # Seven of Coins
        for player in self.__players:
            if ScopaCard(ScopaCardRank.SEVEN, ScopaCardSuit.COINS) in player.get_captured_cards():
                scores[player] += 1
                print(f'{player} got the 7 of Coins ({scores[player]})')
                break

        # Primes
        highest_prime_sum, highest_prime_sum_player = -sys.maxsize, None
        for player in self.__players:
            prime_sum = 0
            for suit in ScopaCardSuit:
                suit_cards = [card for card in player.get_captured_cards() if card.suit() == suit]
                prime_sum += max([get_prime_points(card.rank()) for card in suit_cards]) if suit_cards else 0
            highest_prime_sum, highest_prime_sum_player = max((highest_prime_sum, highest_prime_sum_player),
                                                              (prime_sum, player), key=lambda x: x[0])
        scores[highest_prime_sum_player] += 1
        print(f'{highest_prime_sum_player} has highest prime score ({scores[highest_prime_sum_player]})')
