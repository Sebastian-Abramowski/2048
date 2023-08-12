import constants
import copy
import utilities
import pygame
from board import Board
from score_text import ScoreText
from typing import Callable, Optional


class Game():
    def __init__(self, board: Board, num_of_fields_in_row: int = constants.NUM_OF_FIELDS_IN_ROW):
        self.board = board
        self.score = 0
        self.if_undo_move = False
        self.if_ai_play = False
        self.score_text_group = pygame.sprite.Group()
        self.if_skip_win = False
        self.if_moving_is_blocked = False
        self.if_blocked = False
        self._num_of_fields_in_row = num_of_fields_in_row
        self._last_board_data = None
        self._last_score = None

    def move_horiziontally(self, direction: str, score_rect_center: Optional[tuple[int, int]] = None,
                           if_save_last_move: bool = True) -> bool:
        if if_save_last_move:
            self._save_current_state()

        if_board_changed = False
        board_before_changing = copy.deepcopy(self.board.board_data)

        for row_index in range(self._num_of_fields_in_row):
            self._merge_fields_in_row(row_index, direction, score_rect_center)

        # move fields to the right/left if it's possible
        self.move_everything_horizontally(direction)

        if board_before_changing != self.board.board_data:
            if_board_changed = True

        return if_board_changed

    def _merge_fields_in_row(self, row_index: int, direction: str,
                             score_rect_center: tuple[int, int]) -> None:
        skip_counter = 0
        col_range, merge_cond, next_index, not_out_of_range = self._get_direction_logic(direction)

        for column_index in col_range:
            if skip_counter > 0:
                skip_counter -= 1
                continue

            num = self.board.board_data[row_index][column_index]
            temp_col_index = next_index(column_index)

            if num:
                skip_counter, temp_col_index = self._skip_none_values_in_row(merge_cond, next_index, skip_counter,
                                                                             row_index, temp_col_index)
                skip_counter = self._merge_two_fields_in_row(not_out_of_range, skip_counter, num, row_index,
                                                             column_index, temp_col_index, score_rect_center)

    def _skip_none_values_in_row(self, merge_cond: Callable[[int], bool], next_index: Callable[[int], int],
                                 skip_counter: int, row_index: int, temp_col_index: int) -> tuple[int, int]:
        while merge_cond(temp_col_index) and self.board.board_data[
                row_index][temp_col_index] is None:
            temp_col_index = next_index(temp_col_index)
            skip_counter += 1
        return skip_counter, temp_col_index

    def _merge_two_fields_in_row(self, not_out_of_range: Callable[[int], bool], skip_counter: int,
                                 num: int, row_index: int, column_index: int, temp_col_index: int,
                                 score_rect_center: int) -> int:
        if not_out_of_range(temp_col_index):
            if self.board.board_data[row_index][temp_col_index] == num:
                self.board.board_data[row_index][column_index] = None
                self.board.board_data[row_index][temp_col_index] = 2 * num
                self.score += 2 * num

                self._add_damage_to_score_text_group(num, score_rect_center)

                skip_counter += 1
        return skip_counter

    def move_everything_horizontally(self, direction: str) -> None:
        # Moves everything to the right or left as much as it can
        for row_index in range(self._num_of_fields_in_row):
            row = self.board.board_data[row_index]
            fields_values = [num for num in row if num is not None]
            none_values = [None] * (self._num_of_fields_in_row - len(fields_values))

            self._update_row_with_new_values(row_index, none_values, fields_values,
                                             direction)

    def _update_row_with_new_values(self, row_index: int, none_values: list, fields_values: list,
                                    direction: str) -> None:
        if direction == "right":
            self.board.board_data[row_index] = none_values + fields_values
        elif direction == "left":
            self.board.board_data[row_index] = fields_values + none_values

    def move_vertically(self, direction: str, score_rect_center: tuple[int, int] = None,
                        if_save_last_move: bool = True) -> bool:
        if if_save_last_move:
            self._save_current_state()

        if_board_changed = False
        board_before_changing = copy.deepcopy(self.board.board_data)

        for column_index in range(self._num_of_fields_in_row):
            self._merge_fields_in_column(column_index, direction, score_rect_center)

        # move fields up/down if it's possible
        self.move_everything_vertically(direction)

        if board_before_changing != self.board.board_data:
            if_board_changed = True

        return if_board_changed

    def _merge_fields_in_column(self, column_index: int, direction: str,
                                score_rect_center: tuple[int, int]) -> None:
        skip_counter = 0
        row_range, merge_cond, next_index, not_out_of_range = self._get_direction_logic(direction)

        for row_index in row_range:
            if skip_counter > 0:
                skip_counter -= 1
                continue

            num = self.board.board_data[row_index][column_index]
            temp_row_index = next_index(row_index)

            if num:
                skip_counter, temp_row_index = self._skip_none_values_in_column(merge_cond, next_index,
                                                                                skip_counter, temp_row_index,
                                                                                column_index)
                skip_counter = self._merge_two_fields_in_column(not_out_of_range, skip_counter, num,
                                                                row_index, column_index, temp_row_index,
                                                                score_rect_center)

    def _merge_two_fields_in_column(self, not_out_of_range: Callable[[int], bool], skip_counter: int, num: int,
                                    row_index: int, column_index: int, temp_row_index: int,
                                    score_rect_center: tuple[int, int]) -> int:
        if not_out_of_range(temp_row_index):
            if self.board.board_data[temp_row_index][column_index] == num:
                self.board.board_data[row_index][column_index] = None
                self.board.board_data[temp_row_index][column_index] = 2 * num
                self.score += 2 * num

                self._add_damage_to_score_text_group(num, score_rect_center)

                skip_counter += 1
        return skip_counter

    def _skip_none_values_in_column(self, merge_cond: Callable[[int], bool], next_index: Callable[[int], int],
                                    skip_counter: int, temp_row_index: int, column_index: int) -> tuple[int, int]:
        while merge_cond(temp_row_index) and self.board.board_data[
                temp_row_index][column_index] is None:
            temp_row_index = next_index(temp_row_index)
            skip_counter += 1
        return skip_counter, temp_row_index

    def move_everything_vertically(self, direction: str) -> None:
        for column_index in range(self._num_of_fields_in_row):
            column = []
            for row_index in range(self._num_of_fields_in_row):
                column.append(self.board.board_data[row_index][column_index])

            fields_values = [num for num in column if num is not None]
            none_values = [None] * (self._num_of_fields_in_row - len(fields_values))

            self._update_column_with_new_values(column_index, none_values, fields_values,
                                                direction)

    def _update_column_with_new_values(self, column_index: int, none_values: list, fields_values: list,
                                       direction: str) -> None:
        if direction == "down":
            new_column = none_values + fields_values
            for row_index in range(self._num_of_fields_in_row):
                self.board.board_data[row_index][column_index] = new_column[row_index]
        elif direction == "up":
            new_column = fields_values + none_values
            for row_index in range(self._num_of_fields_in_row):
                self.board.board_data[row_index][column_index] = new_column[row_index]

    def _get_direction_logic(self, direction: str) -> tuple[
            int, Callable[[int], bool], Callable[[int], int], Callable[[int], bool]]:
        if direction == "left" or direction == "up":
            row_or_col_range = range(self._num_of_fields_in_row)
            merge_cond = lambda index: index < self._num_of_fields_in_row
            next_index = lambda index: index + 1
            not_out_of_range = lambda index: index < self._num_of_fields_in_row
        elif direction == "right" or direction == "down":
            row_or_col_range = range(self._num_of_fields_in_row - 1, -1, -1)
            merge_cond = lambda index: index >= 0
            next_index = lambda index: index - 1
            not_out_of_range = lambda index: index >= 0

        return row_or_col_range, merge_cond, next_index, not_out_of_range

    def undo_last_move(self) -> None:
        self.if_undo_move = True
        if self._last_board_data:
            self.board.board_data = self._last_board_data
            self.score = self._last_score

    def update_scores_in_file(self, file_path) -> None:
        player_or_ai = None
        player_or_ai = "ai" if self.if_ai_play else "player"

        if self.score > utilities.read_best_player_or_ai_score_from_file(file_path, player_or_ai):
            utilities.update_best_score_in_file(
                file_path, self.score, self.if_ai_play)

    def _add_to_score_text_group(self, damage: str, score_rect_center: tuple[int, int]) -> None:
        score_text = ScoreText(*score_rect_center, damage, constants.GREY, constants.NORMAL_FONT)
        if self.score_text_group:
            last_sprite_creation_time = self.score_text_group.sprites()[-1].creation_time
            if score_text.creation_time - last_sprite_creation_time > score_text.cooldown:
                self.score_text_group.add(score_text)
        else:
            self.score_text_group.add(score_text)

    def _save_current_state(self) -> None:
        self._last_board_data = copy.deepcopy(self.board.board_data)
        self._last_score = self.score
        self.if_undo_move = False

    def _add_damage_to_score_text_group(self, num: int,
                                        score_rect_center: tuple[int, int]) -> None:
        if score_rect_center:
            damage = '+' + str(2 * num)
            self._add_to_score_text_group(damage, score_rect_center)

    def check_for_win(self) -> bool:
        for row in self.board.board_data:
            for num in row:
                if num == 2048:
                    return True
        return False

    def check_if_blocked(self) -> bool:
        new_board = copy.deepcopy(self.board)
        new_game = Game(new_board, num_of_fields_in_row=self._num_of_fields_in_row)

        if_moved_right = new_game.move_horiziontally("right", if_save_last_move=False)
        if_moved_left = new_game.move_horiziontally("left", if_save_last_move=False)
        if if_moved_right or if_moved_left:
            return False
        if_moved_up = new_game.move_vertically("up", if_save_last_move=False)
        if_moved_down = new_game.move_vertically("down", if_save_last_move=False)
        if if_moved_up or if_moved_down:
            return False
        return True

    def restart_game(self, file_path_to_best_scores) -> None:
        self.update_scores_in_file(file_path_to_best_scores)
        self.score = 0
        self.score_text_group.empty()
        board = Board(game_start=True)
        self.board = board
        self.if_blocked = False
        self.if_moving_is_blocked = False
        self.if_skip_win = True
