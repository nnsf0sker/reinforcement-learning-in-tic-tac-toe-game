from abc import ABCMeta
from typing import Dict
from typing import Optional

from referee import Field


class PlayerAdapter(metaclass=ABCMeta):
    side: Optional[int]
    last_game_steps: Dict[Field, int]

    def next_step(self, field: Field) -> int:
        pass

    def game_train(self, player_result: float) -> None:
        pass
