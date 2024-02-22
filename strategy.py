from cards import ScopaCard, ScopaCardSuit, ScopaCardRank, get_prime_points
from itertools import combinations
from enum import Enum


class ScopaMoveType(Enum):
    TAKE = 0,
    DISCARD = 1


class ScopaMove:

    def __init__(self, move_type: ScopaMoveType, hand_card: ScopaCard, board_cards: list[ScopaCard] = None):
        if not hand_card:
            raise ValueError('Hand card cannot be None when making a move')
        if move_type == ScopaMoveType.TAKE and not board_cards:
            raise ValueError('Board cards cannot be None or empty if move type is TAKE')
        if move_type == ScopaMoveType.DISCARD and board_cards:
            raise ValueError('Board cards cannot be specified if move type is DISCARD')
        self.__move_type = move_type
        self.__hand_card = hand_card
        self.__board_cards = list(board_cards) if board_cards else None

    def move_type(self) -> ScopaMoveType:
        return self.__move_type

    def hand_card(self) -> ScopaCard:
        return self.__hand_card

    def board_cards(self) -> list[ScopaCard]:
        return self.__board_cards

    def __str__(self):
        move_str = f'{self.__move_type.name}: {self.__hand_card}'
        if self.__move_type == ScopaMoveType.TAKE:
            move_str += ' -> ' + ', '.join([str(bc) for bc in self.__board_cards])
        return move_str


class ScopaStrategy:

    __possible_strategies = {'default'}

    def __init__(self, strategy: str = 'default'):
        if strategy not in ScopaStrategy.__possible_strategies:
            raise ValueError(f'Strategy {strategy} not implemented')

        if strategy == 'default':
            self.__scopa_weight = 2
            self.__cards_weight = 1
            self.__coins_weight = 1
            self.__seven_of_coins_weight = 2
            self.__highest_primes_weight = 2
            self.__discard_highest_weight = 0
            self.__discard_lowest_weight = 0

    @staticmethod
    def get_potential_moves(scopa_board: list[ScopaCard], hand: list[ScopaCard]) -> list[ScopaMove]:
        potential_moves = []
        single_take = set()

        for hc in hand:
            for bc in scopa_board:
                if bc.rank() == hc.rank():
                    move = ScopaMove(ScopaMoveType.TAKE, hc, [bc])
                    potential_moves.append(move)
                    single_take.add(hc)

        board_card_combos = []
        for combo_num in range(2, 5):
            board_card_combos.extend(tuple(combinations(scopa_board, combo_num)))

        for hc in hand:
            if hc not in single_take:
                for combo in board_card_combos:
                    combo_ranks = [int(bc.rank()) for bc in combo]
                    if sum(combo_ranks) == hc.rank():
                        move = ScopaMove(ScopaMoveType.TAKE, hc, list(combo))
                        potential_moves.append(move)

        if not potential_moves:
            potential_moves = [ScopaMove(ScopaMoveType.DISCARD, hc) for hc in hand]

        return potential_moves

    def __get_move_scores(self, potential_moves: list[ScopaMove], board: list[ScopaCard]) -> list[int]:
        scores = [0] * len(potential_moves)
        move_type = potential_moves[0].move_type()

        if move_type == ScopaMoveType.TAKE:
            most_cards = 1
            most_coins = 0
            highest_prime = 0

            for i, pm in enumerate(potential_moves):

                cards_to_take = list(pm.board_cards())
                cards_to_take.append(pm.hand_card())

                if len(pm.board_cards()) == len(board):
                    scores[i] += self.__scopa_weight

                for c in cards_to_take:
                    if c.rank() == ScopaCardRank.SEVEN and c.suit() == ScopaCardSuit.COINS:
                        scores[i] += self.__seven_of_coins_weight
                        break

                if len(pm.board_cards()) > most_cards:
                    most_cards = len(pm.board_cards())

                coin_cards = [c for c in cards_to_take if c.suit() == ScopaCardSuit.COINS]
                if len(coin_cards) > most_coins:
                    most_coins = len(coin_cards)

                move_highest_prime = max([get_prime_points(c.rank()) for c in cards_to_take])
                if move_highest_prime > highest_prime:
                    highest_prime = move_highest_prime

            for i, pm in enumerate(potential_moves):
                cards_to_take = list(pm.board_cards())
                cards_to_take.append(pm.hand_card())

                if 1 < most_cards == len(pm.board_cards()):
                    scores[i] += self.__cards_weight

                coin_cards = [c for c in cards_to_take if c.suit() == ScopaCardSuit.COINS]
                if 0 < most_coins == len(coin_cards):
                    scores[i] += self.__coins_weight

                if highest_prime == max([get_prime_points(c.rank()) for c in cards_to_take]):
                    scores[i] += self.__highest_primes_weight

        elif move_type == ScopaMoveType.DISCARD:

            lowest_rank = potential_moves[0].hand_card().rank()
            lowest_rank_idx = 0
            highest_rank = potential_moves[0].hand_card().rank()
            highest_rank_idx = 0
            for i, pm in enumerate(potential_moves):
                if pm.hand_card().rank() < lowest_rank:
                    lowest_rank = pm.hand_card().rank()
                    lowest_rank_idx = i

                if pm.hand_card().rank() > highest_rank:
                    highest_rank = pm.hand_card().rank()
                    highest_rank_idx = i

            scores[lowest_rank_idx] += self.__discard_lowest_weight
            scores[highest_rank_idx] += self.__discard_highest_weight

        else:
            raise ValueError(f'Move type {move_type} not supported')

        return scores

    def make_move(self, scopa_board: list[ScopaCard], hand: list[ScopaCard]) -> ScopaMove:
        if not hand:
            raise ValueError('Cannot make move with empty hand')

        potential_moves = ScopaStrategy.get_potential_moves(scopa_board, hand)

        if len(potential_moves) == 1:
            return potential_moves[0]

        scores = self.__get_move_scores(potential_moves, scopa_board)
        best_move, _ = max(list(zip(potential_moves, scores)), key=lambda x: x[1])

        return best_move
