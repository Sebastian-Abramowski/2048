import constants
import copy
from board import Board


class Game():
    def __init__(self, board: Board, num_of_fields_in_row=constants.NUM_OF_FIELDS_IN_ROW):
        self.board = board
        self.score = 0
        self._num_of_fields_in_row = num_of_fields_in_row

    def move_horiziontally(self, direction):
        if_board_changed = False
        for i in range(self._num_of_fields_in_row):
            skip_counter = 0
            row_before_changing = copy.copy(self.board.board_data[i])

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
                            skip_counter += 1
            # if you are done changing the row,
            # you need to move fields to the right if it's possible
            row = self.board.board_data[i]
            filter_none_values = [num for num in row if num is not None]
            fill_none_values = [None] * (self._num_of_fields_in_row - len(filter_none_values))

            if direction == "right":
                self.board.board_data[i] = fill_none_values + filter_none_values
            elif direction == "left":
                self.board.board_data[i] = filter_none_values + fill_none_values

            if row_before_changing != self.board.board_data[i]:
                if_board_changed = True

        return if_board_changed

    def move_vertically(self, direction):
        if_board_changed = False
        board_before_changing = copy.deepcopy(self.board.board_data)
        for i in range(self._num_of_fields_in_row):
            skip_counter = 0

            if direction == "up":
                col_range = range(self._num_of_fields_in_row)
                merge_cond = lambda j_index: j_index < self._num_of_fields_in_row
                next_index = lambda j_index: j_index + 1
                not_out_of_range = lambda j_index: j_index < self._num_of_fields_in_row
            elif direction == "down":
                col_range = range(self._num_of_fields_in_row - 1, -1, -1)
                merge_cond = lambda j_index: j_index >= 0
                next_index = lambda j_index: j_index - 1
                not_out_of_range = lambda j_index: j_index >= 0

            for j in col_range:
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
                            skip_counter += 1
            # if you are done changing the row,
            # you need to move fields to the right if it's possible
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
