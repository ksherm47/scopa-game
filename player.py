from cards import ScopaCard, ScopaCardSuit
from strategy import ScopaStrategy, ScopaMove
import moveparser


class ScopaPlayer:

    __supported_move_inputs = {'text', 'list'}

    def __init__(self, name, strategy: str = 'default', human: bool = False, show_hand: bool = True,
                 move_input: str = 'list'):
        self.__hand = []
        self.__captures = set()
        self.__strategy = ScopaStrategy(strategy)
        self.__name = name
        self.__human = human
        self.__show_hand = show_hand
        self.__coins_captured = 0
        self.__scopas = 0

        if move_input.lower() not in ScopaPlayer.__supported_move_inputs:
            raise ValueError(f'Unsupported move input selected for player. Must be one of {ScopaPlayer.__supported_move_inputs}')
        self.__move_input = move_input.lower()

    def hand_is_empty(self) -> bool:
        return not self.__hand

    def show_hand(self) -> bool:
        return self.__show_hand

    def make_move(self, scopa_board: list[ScopaCard]) -> ScopaMove:
        if not self.__human:
            return self.__strategy.make_move(scopa_board, self.__hand)

        if self.__move_input == 'text':
            move_input = input('Enter move: ')
            move = None
            while not move:
                try:
                    move = moveparser.parse_move(move_input)
                except ValueError as ve:
                    print(ve)
                    move_input = input('Enter move: ')
            return move

        if self.__move_input == 'list':
            moves = ScopaStrategy.get_potential_moves(scopa_board, self.__hand)
            potential_moves = {str(index): move for index, move in zip(range(1, len(moves) + 1), moves)}
            for index, move in potential_moves.items():
                print(f'{index}: {move}')

            selected_index = None
            while selected_index not in potential_moves:
                selected_index = input('Select move to make: ')

            return potential_moves[selected_index]

    def name(self) -> str:
        return self.__name

    def deal_card(self, card: ScopaCard):
        self.__hand.append(card)

    def remove_hand_card(self, card: ScopaCard):
        self.__hand.remove(card)

    def capture_card(self, card: ScopaCard):
        if card.suit() == ScopaCardSuit.COINS:
            self.__coins_captured += 1
        self.__captures.add(card)

    def capture_cards(self, cards: list[ScopaCard]):
        for card in cards:
            self.capture_card(card)

    def get_captured_cards(self) -> set[ScopaCard]:
        return self.__captures

    def add_scopa(self):
        self.__scopas += 1

    def get_scopa_count(self) -> int:
        return self.__scopas

    def get_num_coins_captured(self) -> int:
        return self.__coins_captured

    def reset(self):
        self.__hand = []
        self.__captures = set()
        self.__coins_captured = 0
        self.__scopas = 0

    def get_hand(self) -> list[ScopaCard]:
        return list(self.__hand)

    def __str__(self):
        return self.__name
