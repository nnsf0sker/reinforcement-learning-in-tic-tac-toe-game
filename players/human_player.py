from typing import Dict

from referee import Field
from referee import Referee
from players import PlayerAdapter


class HumanPlayer(PlayerAdapter):
    def __init__(self, referee: Referee):
        self._referee = referee
        self.side = None
        self.last_game_steps: Dict[Field, int] = {}

    def next_step(self, field: Field) -> int:
        field_size = len(field)
        self._referee.print_field(field)
        step = None
        while not step:
            print("Please, choose cell to make step: ")
            try:
                step = int(input())
                if step < 0:
                    print("Impossible step (< 0), please try again: ")
                elif step >= field_size:
                    print("Impossible step (> field size), please try again: ")
                elif field[step] != 0:
                    print("Impossible step (cell is filled), please try again: ")
                else:
                    return step
                step = None
            except ValueError:
                print("Impossible step, please try again: ")

    def game_train(self, player_result: float) -> None:
        pass
