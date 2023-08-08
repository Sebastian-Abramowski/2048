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
        self._num_of_fields_in_row = num_of_fields_in_row
        self._last_board_data = None
        self._last_score = None

    def move_horiziontally(self, direction, score_rect_center=None):
        self._last_board_data = copy.deepcopy(self.board.board_data)
        self._last_score = self.score
        self.if_undo_move = False

        if_board_changed = False
        board_before_changing = copy.deepcopy(self.board.board_data)
        for i in range(self._num_of_fields_in_row):
            skip_counter = 0

            if direction == "left":
                col_range = range(self._num_of_fields_in_row)
                merge_cond = lambda j_index: j_index < self._num_of_fields_in_row
                next_index = lambda j_index: j_index + 1
                not_out_of_range = lambda j_index: j_index < self._num_of_fields_in_row
            elif direction == "right":
                col_range = range(self._num_of_fields_in_row - 1, -1, -1)
                merge_cond = lambda j_index: j_index >= 0
                next_index = lambda j_index: j_index - 1
                not_out_of_range = lambda j_index: j_index >= 0

            for j in col_range:
                if skip_counter > 0:
                    skip_counter -= 1
                    continue

                num = self.board.board_data[i][j]

                temp_j_index = next_index(j)

                if num:
                    while merge_cond(temp_j_index) and self.board.board_data[
                            i][temp_j_index] is None:
                        temp_j_index = next_index(temp_j_index)
                        skip_counter += 1

                    if not_out_of_range(temp_j_index):
                        if self.board.board_data[i][temp_j_index] == num:
                            self.board.board_data[i][j] = None
                            self.board.board_data[i][temp_j_index] = 2 * num
                            self.score += 2 * num

                            if score_rect_center:
                                damage = '+' + str(2 * num)
                                self._update_score_text_group(damage, score_rect_center)

                            skip_counter += 1
            # if you are done changing the row,
            # you need to move fields to the right/left if it's possible
            row = self.board.board_data[i]
            filter_none_values = [num for num in row if num is not None]
            fill_none_values = [None] * (self._num_of_fields_in_row - len(filter_none_values))

            if direction == "right":
                self.board.board_data[i] = fill_none_values + filter_none_values
            elif direction == "left":
                self.board.board_data[i] = filter_none_values + fill_none_values

            if board_before_changing != self.board.board_data:
                if_board_changed = True

        return if_board_changed

    def move_vertically(self, direction, score_rect_center=None):
        self._last_board_data = copy.deepcopy(self.board.board_data)
        self._last_score = self.score
        self.if_undo_move = False

        if_board_changed = False
        board_before_changing = copy.deepcopy(self.board.board_data)
        for i in range(self._num_of_fields_in_row):
            skip_counter = 0

            if direction == "up":
                row_range = range(self._num_of_fields_in_row)
                merge_cond = lambda j_index: j_index < self._num_of_fields_in_row
                next_index = lambda j_index: j_index + 1
                not_out_of_range = lambda j_index: j_index < self._num_of_fields_in_row
            elif direction == "down":
                row_range = range(self._num_of_fields_in_row - 1, -1, -1)
                merge_cond = lambda j_index: j_index >= 0
                next_index = lambda j_index: j_index - 1
                not_out_of_range = lambda j_index: j_index >= 0

            for j in row_range:
                if skip_counter > 0:
                    skip_counter -= 1
                    continue

                num = self.board.board_data[j][i]

                temp_j_index = next_index(j)

                if num:
                    while merge_cond(temp_j_index) and self.board.board_data[
                            temp_j_index][i] is None:
                        temp_j_index = next_index(temp_j_index)
                        skip_counter += 1

                    if not_out_of_range(temp_j_index):
                        if self.board.board_data[temp_j_index][i] == num:
                            self.board.board_data[j][i] = None
                            self.board.board_data[temp_j_index][i] = 2 * num
                            self.score += 2 * num

                            if score_rect_center:
                                damage = '+' + str(2 * num)
                                self._update_score_text_group(damage, score_rect_center)

                            skip_counter += 1
            # if you are done changing the column,
            # you need to move fields up/down if it's possible
            column = []
            for index_col in range(self._num_of_fields_in_row):
                column.append(self.board.board_data[index_col][i])

            filter_none_values = [num for num in column if num is not None]
            fill_none_values = [None] * (self._num_of_fields_in_row - len(filter_none_values))

            if direction == "down":
                new_column = fill_none_values + filter_none_values
                for index_col in range(self._num_of_fields_in_row):
                    self.board.board_data[index_col][i] = new_column[index_col]
            elif direction == "up":
                new_column = filter_none_values + fill_none_values
                for index_col in range(self._num_of_fields_in_row):
                    self.board.board_data[index_col][i] = new_column[index_col]

            if board_before_changing != self.board.board_data:
                if_board_changed = True

        return if_board_changed

    def undo_last_move(self):
        self.if_undo_move = True
        if self._last_board_data:
            self.board.board_data = self._last_board_data
            self.score = self._last_score

    def updates_scores(self, file_path):
        player_or_ai = None
        if self.if_ai_play:
            player_or_ai = "ai"
        else:
            player_or_ai = "player"

        if self.score > utilities.read_best_player_or_ai_score_from_file(file_path, player_or_ai):
            utilities.update_best_score_in_file(
                file_path, self.score, self.if_ai_play)

    def _update_score_text_group(self, damage: str, score_rect_center):
        score_text = ScoreText(*score_rect_center, damage, constants.GREY, constants.NORMAL_FONT)
        if self.score_text_group:
            last_sprite_creation_time = self.score_text_group.sprites()[-1].creation_time
            if score_text.creation_time - last_sprite_creation_time > score_text.cooldown:
                self.score_text_group.add(score_text)
        else:
            self.score_text_group.add(score_text)
