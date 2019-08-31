import json
import random
from typing import Tuple
from typing import List
from typing import Dict
from typing import Any
from referee import Referee
from referee import Field

from players import PlayerAdapter


def free_cells(field: Field) -> Tuple[float, ...]:
    return tuple(-1.0 if cell else 0.5 for cell in field)


class ReinforcementLearningPlayer(PlayerAdapter):
    def __init__(self, config: Dict[str, Any], referee: Referee):
        self._player_name: str = config["PLAYER_NAME"]
        self._random_step_chance: float = config["RANDOM_STEP_CHANCE"]
        self._studying_coef: float = config["STUDYING_COEF"]
        self._db_path = config["DB_PATH"]  # TODO: Добавить hint
        self._referee: Referee = referee
        self.mode: str
        self.side: int
        self.last_game_steps: Dict[Field, int] = {}
        self._weight_db: Dict[Field, List[float]]
        try:
            with open(self._db_path, "r") as db_file:
                self._weight_db = {}
                for key, value in json.load(db_file).items():
                    self._weight_db[tuple(key)] = value
                self._mode = "play"
        except Exception:  # TODO: Бесит ошибка: разобраться!
            self._weight_db = {}
            self._mode = "train"
            for possible_position in referee.all_possible_fields():
                self._weight_db[possible_position] = list(free_cells(possible_position))

    def next_step(self, field: Field) -> int:
        possible_steps = self._weight_db[field]
        field_size = self._referee.rows_n * self._referee.cols_n
        if self._mode == "train":
            if random.random() < self._random_step_chance:
                while True:
                    step = random.randrange(field_size)
                    if possible_steps[step] > 0:
                        return step
        return possible_steps.index(max(possible_steps))

    def game_train(self, player_result: float) -> None:
        for prev_field, step in self.last_game_steps.items():
            self._step_train(player_result, prev_field, step)
        self.last_game_steps = {}

    def _step_train(self, result: float, prev_field: Field, step: int) -> None:
        rows_n = self._referee.rows_n
        cols_n = self._referee.cols_n
        for field_, step_ in (
            (prev_field, step),
            (self._referee.horizontal_revert(prev_field), (rows_n - step // cols_n - 1) * cols_n + step % cols_n),
            (self._referee.vertical_revert(prev_field), (step // cols_n + 1) * cols_n - step % cols_n - 1),
            (self._referee.horizontal_revert(self._referee.vertical_revert(prev_field)), cols_n * rows_n - step - 1),
        ):
            step_weight = self._weight_db[field_][step_]
            self._weight_db[field_][step_] = step_weight + self._studying_coef * (result - step_weight)

    def save_weight_db(self) -> None:
        with open(self._db_path, "w") as db_file:
            obj = [{"key": key, "value": value} for key, value in self._weight_db.items()]
            json.dump(obj=obj, fp=db_file, indent=1)
