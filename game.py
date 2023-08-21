import constants
import copy
import utilities
import pygame
import numpy as np
from board import Board
from score_text import ScoreText
from pathlib import Path
from typing import Callable, Optional, Union


class Game():
    def __init__(self, board: Board, num_of_fields_in_row: int = constants.NUM_OF_FIELDS_IN_ROW_AND_COL):
        self.board = board
        self.score = 0
        self.if_undo_move = False
        self.if_ai_play = False
        self.score_text_group = pygame.sprite.Group()
        self.if_skip_win = False
        self.if_moving_is_blocked = False
        self.if_blocked = False
        self.if_started = False
        self.num_of_fields_in_row = num_of_fields_in_row
        self._last_board_data = None
        self._last_score = None

    def move_and_check_if_moved(self, direction: str, curr_score_rect_center: Optional[tuple[int, int]] = None,
                                if_save_last_move: bool = True) -> bool:
        self._validate_function_with_direction(direction)

        if direction in ["right", "left"]:
            return self._move_horiziontally(direction, curr_score_rect_center,
                                            if_save_last_move)
        elif direction in ["up", "down"]:
            return self._move_vertically(direction, curr_score_rect_center,
                                         if_save_last_move)

    def _move_horiziontally(self, direction: str, curr_score_rect_center: Optional[tuple[int, int]] = None,
                            if_save_last_move: bool = True) -> bool:
        if if_save_last_move:
            last_board_data = copy.deepcopy(self.board.board_data)
            last_score = self.score
        board_data_before_changing = copy.deepcopy(self.board.board_data)

        for row_index in range(self.num_of_fields_in_row):
            self._merge_fields_in_row(row_index, direction, curr_score_rect_center)
        # move fields to the right/left if it's possible
        self._move_everything_horizontally(direction)

        is_board_changed = self._check_if_board_changed(board_data_before_changing)
        if is_board_changed and if_save_last_move:
            self._save_previouos_state(last_board_data, last_score)
        return is_board_changed

    def _merge_fields_in_row(self, row_index: int, direction: str,
                             curr_score_rect_center: tuple[int, int]) -> None:
        skip_counter = 0
        col_range, merge_cond, next_index, not_out_of_range = self._get_logic_for_merging(direction)

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
                                                             column_index, temp_col_index, curr_score_rect_center)

    def _skip_none_values_in_row(self, merge_cond: Callable[[int], bool], next_index: Callable[[int], int],
                                 skip_counter: int, row_index: int, temp_col_index: int) -> tuple[int, int]:
        """
        Increases temp_col_index until it spots not None value and keeps track of how many None values it skipped
        """
        while merge_cond(temp_col_index) and self.board.board_data[
                row_index][temp_col_index] is None:
            temp_col_index = next_index(temp_col_index)
            skip_counter += 1
        return skip_counter, temp_col_index

    def _merge_two_fields_in_row(self, not_out_of_range: Callable[[int], bool], skip_counter: int,
                                 num: int, row_index: int, column_index: int, temp_col_index: int,
                                 curr_score_rect_center: int) -> int:
        if not_out_of_range(temp_col_index):
            if self.board.board_data[row_index][temp_col_index] == num:
                self.board.board_data[row_index][column_index] = None
                self.board.board_data[row_index][temp_col_index] = 2 * num
                self.score += 2 * num

                self._add_damage_to_score_text_group(num, curr_score_rect_center)

                skip_counter += 1
        return skip_counter

    def _move_everything_horizontally(self, direction: str) -> None:
        # Moves everything to the right or left as much as it can
        for row_index in range(self.num_of_fields_in_row):
            row = self.board.board_data[row_index]
            fields_values = [num for num in row if num is not None]
            none_values = [None] * (self.num_of_fields_in_row - len(fields_values))

            self._update_row_with_new_values(row_index, none_values, fields_values,
                                             direction)

    def _update_row_with_new_values(self, row_index: int, none_values: list, fields_values: list,
                                    direction: str) -> None:
        if direction == "right":
            self.board.board_data[row_index] = none_values + fields_values
        elif direction == "left":
            self.board.board_data[row_index] = fields_values + none_values

    def _move_vertically(self, direction: str, curr_score_rect_center: tuple[int, int] = None,
                         if_save_last_move: bool = True) -> bool:
        last_board_data, last_score = None, None
        if if_save_last_move:
            last_board_data = copy.deepcopy(self.board.board_data)
            last_score = self.score
        board_data_before_changing = copy.deepcopy(self.board.board_data)

        for column_index in range(self.num_of_fields_in_row):
            self._merge_fields_in_column(column_index, direction, curr_score_rect_center)
        # move fields up/down if it's possible
        self._move_everything_vertically(direction)

        is_board_changed = self._check_if_board_changed(board_data_before_changing)
        if is_board_changed and if_save_last_move:
            self._save_previouos_state(last_board_data, last_score)
        return is_board_changed

    def _merge_fields_in_column(self, column_index: int, direction: str,
                                curr_score_rect_center: tuple[int, int]) -> None:
        skip_counter = 0
        row_range, merge_cond, next_index, not_out_of_range = self._get_logic_for_merging(direction)

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
                                                                curr_score_rect_center)

    def _merge_two_fields_in_column(self, not_out_of_range: Callable[[int], bool], skip_counter: int, num: int,
                                    row_index: int, column_index: int, temp_row_index: int,
                                    curr_score_rect_center: tuple[int, int]) -> int:
        if not_out_of_range(temp_row_index):
            if self.board.board_data[temp_row_index][column_index] == num:
                self.board.board_data[row_index][column_index] = None
                self.board.board_data[temp_row_index][column_index] = 2 * num
                self.score += 2 * num

                self._add_damage_to_score_text_group(num, curr_score_rect_center)

                skip_counter += 1
        return skip_counter

    def _skip_none_values_in_column(self, merge_cond: Callable[[int], bool], next_index: Callable[[int], int],
                                    skip_counter: int, temp_row_index: int, column_index: int) -> tuple[int, int]:
        """
        Increases temp_row_index until it spots not None value and keeps track of how many None values it skipped
        """
        while merge_cond(temp_row_index) and self.board.board_data[
                temp_row_index][column_index] is None:
            temp_row_index = next_index(temp_row_index)
            skip_counter += 1
        return skip_counter, temp_row_index

    def _move_everything_vertically(self, direction: str) -> None:
        for column_index in range(self.num_of_fields_in_row):
            column = []
            for row_index in range(self.num_of_fields_in_row):
                column.append(self.board.board_data[row_index][column_index])

            fields_values = [num for num in column if num is not None]
            none_values = [None] * (self.num_of_fields_in_row - len(fields_values))

            self._update_column_with_new_values(column_index, none_values, fields_values,
                                                direction)

    def _update_column_with_new_values(self, column_index: int, none_values: list, fields_values: list,
                                       direction: str) -> None:
        if direction == "down":
            new_column = none_values + fields_values
            for row_index in range(self.num_of_fields_in_row):
                self.board.board_data[row_index][column_index] = new_column[row_index]
        elif direction == "up":
            new_column = fields_values + none_values
            for row_index in range(self.num_of_fields_in_row):
                self.board.board_data[row_index][column_index] = new_column[row_index]

    def _get_logic_for_merging(self, direction: str) -> tuple[
            int, Callable[[int], bool], Callable[[int], int], Callable[[int], bool]]:
        if direction == "left" or direction == "up":
            row_or_col_range = range(self.num_of_fields_in_row)
            merge_cond = lambda index: index < self.num_of_fields_in_row
            next_index = lambda index: index + 1
            not_out_of_range = lambda index: index < self.num_of_fields_in_row
        elif direction == "right" or direction == "down":
            row_or_col_range = range(self.num_of_fields_in_row - 1, -1, -1)
            merge_cond = lambda index: index >= 0
            next_index = lambda index: index - 1
            not_out_of_range = lambda index: index >= 0

        return row_or_col_range, merge_cond, next_index, not_out_of_range

    def undo_last_move(self) -> None:
        self.if_undo_move = True
        if self._last_board_data is not None:
            self.board.board_data = self._last_board_data
            self.score = self._last_score

    def update_score_in_file(self, file_path: Union[Path, str]) -> None:
        if self.if_ai_play:
            current_score = utilities.read_best_ai_score_from_file(file_path)
        else:
            current_score = utilities.read_best_player_score_from_file(file_path)

        if self.score > current_score:
            if self.if_ai_play:
                utilities.update_best_ai_score_in_file(file_path, self.score)
            else:
                utilities.update_best_player_score_in_file(file_path, self.score)

    def _add_to_score_text_group(self, text: str, curr_score_rect_center: tuple[int, int]) -> None:
        score_text = ScoreText(*curr_score_rect_center, text, constants.GREY, constants.NORMAL_FONT)
        if self.score_text_group:
            last_sprite_creation_time = self.score_text_group.sprites()[-1].creation_time
            if score_text.creation_time - last_sprite_creation_time > score_text.cooldown:
                self.score_text_group.add(score_text)
        else:
            self.score_text_group.add(score_text)

    def _save_previouos_state(self, last_board_data: np.array, last_score: int) -> None:
        self._last_board_data = last_board_data
        self._last_score = last_score
        self.if_undo_move = False

    def _add_damage_to_score_text_group(self, num: int,
                                        curr_score_rect_center: tuple[int, int]) -> None:
        if curr_score_rect_center:
            damage = '+' + str(2 * num)
            self._add_to_score_text_group(damage, curr_score_rect_center)

    def restart_game(self, file_path_to_best_scores: Union[Path, str]) -> None:
        self.update_score_in_file(file_path_to_best_scores)
        self.score = 0
        self.score_text_group.empty()
        board = Board(game_start=True)
        self.board = board
        self.if_blocked = False
        self.if_moving_is_blocked = False
        self.if_ai_play = False
        self.if_started = False
        self.if_skip_win = False
        self._last_board_data = None
        self._last_score = None

    def _check_if_board_changed(self, board_data_before_changing: np.array) -> bool:
        if_board_changed = False
        if not np.array_equal(board_data_before_changing, self.board.board_data):
            if_board_changed = True
        return if_board_changed

    def _validate_function_with_direction(self, direction: str):
        """
        Raises WrongUseOfFunctionError, if passed direction is unknown
        """
        if direction not in ["left", "right", "up", "down"]:
            error_message = (f"The direction can be either left, right, up or down. "
                             f"You passed {direction}")
            raise utilities.WrongUseOfFuncionError(error_message)

    @staticmethod
    def check_for_win(board: Board) -> bool:
        return bool(np.any(board.board_data == 2048))

    @staticmethod
    def check_if_blocked(board: Board,
                         num_of_fields_in_single_row=constants.NUM_OF_FIELDS_IN_ROW_AND_COL) -> bool:
        new_board = copy.deepcopy(board)
        new_game = Game(new_board, num_of_fields_in_row=num_of_fields_in_single_row)

        for direction in ["up", "down", "right", "left"]:
            if new_game.move_and_check_if_moved(direction, if_save_last_move=False):
                return False
        return True

    @staticmethod
    def check_if_able_to_move(board: Board, direction: str,
                              num_of_fields_in_single_row=constants.NUM_OF_FIELDS_IN_ROW_AND_COL) -> tuple[
                                  bool, Board]:
        new_board = copy.deepcopy(board)
        new_game = Game(new_board, num_of_fields_in_row=num_of_fields_in_single_row)

        if_sth_on_board_changed = new_game.move_and_check_if_moved(direction, if_save_last_move=False)
        board_after_movement = new_game.board

        return if_sth_on_board_changed, board_after_movement
