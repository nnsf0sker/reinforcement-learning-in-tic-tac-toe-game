from typing import Any
from typing import List
from typing import Dict
from typing import Tuple
from typing import Optional

from typing import Iterator

import random

Field = Tuple[int, ...]


def obj_without_elem_by_value(obj: Tuple[Any, ...], elem_value: Any) -> Tuple[Any, ...]:
    elem_id = obj.index(elem_value)
    return obj[0:elem_id] + obj[elem_id + 1:]


# TODO: Обобщить int до любого неизменяемого типа данных
def smart_permutations(obj: Tuple[int, ...]) -> Iterator[Tuple[int, ...]]:
    if len(obj) == 1:
        yield (obj[0],)
    else:
        unique_values = set(obj)
        for value in unique_values:
            for perm in smart_permutations(obj_without_elem_by_value(obj, value)):
                yield (value,) + perm


class Referee:
    def __init__(self, config: Dict[str, Any]):
        self.rows_n: int = config["ROWS_N"]
        self.cols_n: int = config["COLS_N"]
        self.len_to_win: int = config["LEN_TO_WIN"]
        assert type(self.rows_n) == int, "[ERROR] Field height (rows_s) is not an integer"
        assert self.rows_n > 0, "[ERROR] Field height (rows_n) is zero or less"
        assert type(self.cols_n) == int, "[ERROR] Field width (cols_n) is not an integer"
        assert self.cols_n > 0, "[ERROR] Field width (cols_n) is zero or less"
        assert type(self.len_to_win) == int, "[ERROR] Len to win-line (len_to_win) is  not an integer"
        assert self.len_to_win > 0, "[ERROR] Len to win-line (len_to_win) is zero or less"
        assert self.rows_n >= self.len_to_win or self.cols_n >= self.len_to_win, "[ERROR] Win-length is unreachable"
        self._field_size: int = self.rows_n * self.cols_n

    def all_possible_fields(self) -> Iterator[Field]:
        for filled_cells_n in range(self._field_size + 1):
            free_cells_n = self._field_size - filled_cells_n
            first_player_cells_n = filled_cells_n // 2 + filled_cells_n % 2
            second_player_cells_n = filled_cells_n // 2
            for possible_position in smart_permutations(
                (0,) * free_cells_n + (1,) * first_player_cells_n + (2,) * second_player_cells_n
            ):
                yield possible_position

    @staticmethod
    def _get_random_free_cell_id_from_tuple(obj: Tuple[int, ...]) -> int:
        if obj.count(0) == 0:
            return -1
        obj_size = len(obj)
        possible_ids = [cell_id for cell_id in range(obj_size) if not obj[cell_id]]
        possible_ids_n = len(possible_ids)
        return possible_ids[random.randrange(possible_ids_n)]

    def get_clear_field(self) -> Tuple[int, ...]:
        return tuple(0 for _ in range(self._field_size))

    def get_random_field(self) -> Tuple[int, ...]:
        while True:
            field = list(self.get_clear_field())
            filled_cells_n = random.randrange(self._field_size)
            for cell_no in range(filled_cells_n):
                cell_side = cell_no % 2 + 1
                cell_id = Referee._get_random_free_cell_id_from_tuple(tuple(field))
                field[cell_id] = cell_side
            if not self.check_field(tuple(field)):
                return tuple(field)

    def check_field(
            self,
            field: Field,
            last_step_row: Optional[int] = None,
            last_step_col: Optional[int] = None
    ) -> int:
        if last_step_row and last_step_col:
            return self._check_field_with_last_step(field=field, row=last_step_row, col=last_step_col)
        else:
            return self._check_field_without_last_step(field=field)

    def print_field(self, field: Field) -> None:
        for row_no in range(self.rows_n):
            for col_no in range(self.cols_n):
                cell = field[row_no * self.cols_n + col_no]
                if cell == 0:
                    print("%2s " % (self.cols_n * row_no + col_no), end="")
                elif cell == 1:
                    print(" x ", end="")
                elif cell == 2:
                    print(" o ", end="")
                else:
                    assert False, "impossible error"
            print()

    def _get_horizontal_line(self, field: Field, row: int, col: int) -> Tuple[int, ...]:
        first_cell_n = row * self.cols_n
        return tuple(field[first_cell_n : first_cell_n + self.cols_n])

    def _get_vertical_line(self, field: Field, row: int, col: int) -> Tuple[int, ...]:
        return tuple(field[row_no * self.cols_n + col] for row_no in range(self.rows_n))

    def _get_left_diagonal_line(self, field: Field, row: int, col: int) -> Tuple[int, ...]:
        row_start = max(row - col, 0)
        col_start = max(col - row, 0)
        first_cell_n = row_start * self.cols_n + col_start
        return tuple(
            field[first_cell_n + step * (self.cols_n + 1)]
            for step in range(min(self.cols_n - col_start, self.rows_n - row_start))
        )

    def _get_right_diagonal_line(self, field: Field, row: int, col: int) -> Tuple[int, ...]:
        first_cell_row = max(0, row + col - self.cols_n + 1)
        first_cell_col = min(row + col, self.cols_n - 1)
        first_cell_n = first_cell_row * self.cols_n + first_cell_col
        return tuple(
            field[first_cell_n + step * (self.cols_n - 1)]
            for step in range(min(self.rows_n - first_cell_row, first_cell_col + 1))
        )

    def _check_line(self, line: Tuple[int, ...]) -> int:
        prev_cell_value = line[0]
        count = 0
        for cell in line:
            if prev_cell_value == cell and cell:
                count += 1
                if count >= self.len_to_win:
                    return cell
            else:
                prev_cell_value = cell
                count = 1
        return 0

    @staticmethod
    def _is_field_full(field: Field) -> bool:
        if field.count(0):
            return False
        return True

    def _check_field_without_last_step(self, field: Field) -> int:
        left_col = tuple({"row": row, "col": 0} for row in range(self.rows_n))
        right_col = tuple({"row": row, "col": self.cols_n - 1} for row in range(self.rows_n))
        upper_col = tuple({"row": 0, "col": col} for col in range(self.cols_n))
        for cells_on_line, get_line_func in (
            (left_col, self._get_horizontal_line),
            (upper_col, self._get_vertical_line),
            (left_col + upper_col, self._get_left_diagonal_line),
            (right_col + upper_col, self._get_right_diagonal_line),
        ):
            for cell in cells_on_line:
                line = get_line_func(field=field, row=cell["row"], col=cell["col"])
                res = self._check_line(line)
                if res:
                    return res
        if Referee._is_field_full(field):
            return -1
        else:
            return 0

    def _check_field_with_last_step(self, field: Field, row: int, col: int) -> int:
        for line in [
            self._get_horizontal_line(field, row, col),
            self._get_vertical_line(field, row, col),
            self._get_left_diagonal_line(field, row, col),
            self._get_right_diagonal_line(field, row, col),
        ]:
            res = self._check_line(line)
            if res:
                return res
        if Referee._is_field_full(field):
            return -1
        else:
            return 0

    def horizontal_revert(self, field: Field) -> Field:
        res: List[int] = []
        for row in range(self.rows_n):
            res = res + list(field[self.cols_n * (self.rows_n - row - 1) : self.cols_n * (self.rows_n - row)])
        return tuple(res)

    def vertical_revert(self, field: Field) -> Field:
        res: List[int] = []
        for row in range(self.rows_n):
            res = res + list(reversed(field[self.cols_n * row : self.cols_n * (row + 1)]))
        return tuple(res)
