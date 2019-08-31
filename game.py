from referee import Referee
from players import PlayerAdapter
from typing import Optional
from typing import List


class Game:
    def __init__(self, referee: Referee):
        self._referee: Referee = referee

    def several_games(
            self,
            games_number: int,
            start_position: str,
            first_player: PlayerAdapter,
            second_player: PlayerAdapter
    ) -> None:
        for game_no in range(games_number):
            self.one_game(start_position, first_player, second_player)

    # TODO: Функцию one_game нужно декомпозировать, она очень сложная. Прям ОЧЕНЬ! 50 строчек кода!
    def one_game(self, start_position: str, first_player: PlayerAdapter, second_player: PlayerAdapter) -> None:
        game_result: Optional[int] = None
        field: List[int]
        next_player: PlayerAdapter
        prev_player: PlayerAdapter
        first_player.side = 1
        second_player.side = 2
        if start_position == 'random':
            field = list(self._referee.get_random_field())
            x_cells: int = field.count(1)
            o_cells: int = field.count(2)
            if x_cells == o_cells:
                next_player = first_player
                prev_player = second_player
            elif x_cells > o_cells:
                next_player = second_player
                prev_player = first_player
        elif start_position == 'clear':
            field = list(self._referee.get_clear_field())
            next_player = first_player
            prev_player = second_player
        else:
            assert False, "ERROR! Starting position does not stated."
            # TODO:
            #  1) ERROR -> WARNING;
            #  2) Продумать логику выбора типа стартового поля;
            #  3) Может использовать логи в .txt
        steps_counter: int = 1
        while not game_result:
            step: int = next_player.next_step(tuple(field))
            next_player.last_game_steps[tuple(field)] = step
            field[step] = next_player.side
            game_result = self._referee.check_field(
                field=tuple(field),
                last_step_row=step // self._referee.cols_n,
                last_step_col=step % self._referee.cols_n,
            )
            next_player, prev_player = prev_player, next_player
            steps_counter += 1
        if game_result == 1:
            first_player.game_train(player_result=1)
            second_player.game_train(player_result=0)
        elif game_result == 2:
            first_player.game_train(player_result=0)
            second_player.game_train(player_result=1)
        else:
            first_player.game_train(player_result=0.5)
            second_player.game_train(player_result=0.5)
        # first_player.save_weight_db()
