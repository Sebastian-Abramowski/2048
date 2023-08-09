import constants
import copy
import utilities
import pygame
from board import Board
from score_text import ScoreText


class Game():
    def __init__(self, board: Board, num_of_fields_in_row=constants.NUM_OF_FIELDS_IN_ROW):
        self.board = board
        self.score = 0
        self.if_undo_move = False
        self.if_ai_play = False
        self.score_text_group = pygame.sprite.Group()
        self.if_skip_win = False
        self.if_blocked_moving = False
        self._num_of_fields_in_row = num_of_fields_in_row
        self._last_board_data = None
        self._last_score = None

    def move_horiziontally(self, direction, score_rect_center=None):
        self._save_current_state()

        if_board_changed = False
        board_before_changing = copy.deepcopy(self.board.board_data)

        for row_index in range(self._num_of_fields_in_row):
            skip_counter = 0

            col_range, merge_cond, next_index, not_out_of_range = self._get_direction_logic(direction)

            for column_index in col_range:
                if skip_counter > 0:
                    skip_counter -= 1
                    continue

                num = self.board.board_data[row_index][column_index]

                temp_col_index = next_index(column_index)

                if num:
                    while merge_cond(temp_col_index) and self.board.board_data[
                            row_index][temp_col_index] is None:
                        temp_col_index = next_index(temp_col_index)
                        skip_counter += 1

                    if not_out_of_range(temp_col_index):
                        if self.board.board_data[row_index][temp_col_index] == num:
                            self.board.board_data[row_index][column_index] = None
                            self.board.board_data[row_index][temp_col_index] = 2 * num
                            self.score += 2 * num

                            if score_rect_center:
                                damage = '+' + str(2 * num)
                                self._add_to_score_text_group(damage, score_rect_center)

                            skip_counter += 1
            # move fields to the right/left if it's possible
            self.move_everything_horizontally(row_index, direction)

        if board_before_changing != self.board.board_data:
            if_board_changed = True

        return if_board_changed

    def move_everything_horizontally(self, row_index, direction):
        # Moves everything to the right or left as much as it can
        row = self.board.board_data[row_index]
        filter_none_values = [num for num in row if num is not None]
        fill_none_values = [None] * (self._num_of_fields_in_row - len(filter_none_values))

        if direction == "right":
            self.board.board_data[row_index] = fill_none_values + filter_none_values
        elif direction == "left":
            self.board.board_data[row_index] = filter_none_values + fill_none_values

    def move_vertically(self, direction, score_rect_center=None):
        self._save_current_state()

        if_board_changed = False
        board_before_changing = copy.deepcopy(self.board.board_data)

        for column_index in range(self._num_of_fields_in_row):
            skip_counter = 0

            row_range, merge_cond, next_index, not_out_of_range = self._get_direction_logic(direction)

            for row_index in row_range:
                if skip_counter > 0:
                    skip_counter -= 1
                    continue

                num = self.board.board_data[row_index][column_index]

                temp_row_index = next_index(row_index)

                if num:
                    while merge_cond(temp_row_index) and self.board.board_data[
                            temp_row_index][column_index] is None:
                        temp_row_index = next_index(temp_row_index)
                        skip_counter += 1

                    if not_out_of_range(temp_row_index):
                        if self.board.board_data[temp_row_index][column_index] == num:
                            self.board.board_data[row_index][column_index] = None
                            self.board.board_data[temp_row_index][column_index] = 2 * num
                            self.score += 2 * num

                            if score_rect_center:
                                damage = '+' + str(2 * num)
                                self._add_to_score_text_group(damage, score_rect_center)

                            skip_counter += 1
            # move fields up/down if it's possible
            self.move_everything_vertically(column_index, direction)

        if board_before_changing != self.board.board_data:
            if_board_changed = True

        return if_board_changed

    def move_everything_vertically(self, column_index, direction):
        column = []
        for row_index in range(self._num_of_fields_in_row):
            column.append(self.board.board_data[row_index][column_index])

        filter_none_values = [num for num in column if num is not None]
        fill_none_values = [None] * (self._num_of_fields_in_row - len(filter_none_values))

        if direction == "down":
            new_column = fill_none_values + filter_none_values
            for row_index in range(self._num_of_fields_in_row):
                self.board.board_data[row_index][column_index] = new_column[row_index]
        elif direction == "up":
            new_column = filter_none_values + fill_none_values
            for row_index in range(self._num_of_fields_in_row):
                self.board.board_data[row_index][column_index] = new_column[row_index]

    def _get_direction_logic(self, direction):
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

    def undo_last_move(self):
        self.if_undo_move = True
        if self._last_board_data:
            self.board.board_data = self._last_board_data
            self.score = self._last_score

    def update_scores_in_file(self, file_path):
        player_or_ai = None
        if self.if_ai_play:
            player_or_ai = "ai"
        else:
            player_or_ai = "player"

        if self.score > utilities.read_best_player_or_ai_score_from_file(file_path, player_or_ai):
            utilities.update_best_score_in_file(
                file_path, self.score, self.if_ai_play)

    def _add_to_score_text_group(self, damage: str, score_rect_center):
        score_text = ScoreText(*score_rect_center, damage, constants.GREY, constants.NORMAL_FONT)
        if self.score_text_group:
            last_sprite_creation_time = self.score_text_group.sprites()[-1].creation_time
            if score_text.creation_time - last_sprite_creation_time > score_text.cooldown:
                self.score_text_group.add(score_text)
        else:
            self.score_text_group.add(score_text)

    def _save_current_state(self):
        self._last_board_data = copy.deepcopy(self.board.board_data)
        self._last_score = self.score
        self.if_undo_move = False

    def check_for_win(self):
        for row in self.board.board_data:
            for num in row:
                if num == 2048:
                    return True
        return False
