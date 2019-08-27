from abc import ABCMeta
from referee import Field


class PlayerAdapter(metaclass=ABCMeta):
    def next_step(self, field: Field) -> int:
        pass

    def game_train(self, player_result: float) -> None:
        pass
