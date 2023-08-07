import constants
from board import Board


class Game():
    def __init__(self, board: Board, num_of_fields_in_row=constants.NUM_OF_FIELDS_IN_ROW):
        self.board = board
        self.score = 0
        self._num_of_fields_in_row = num_of_fields_in_row

    def move_right(self):
        for i in range(self._num_of_fields_in_row):
            skip_counter = 0
            for j in range(self._num_of_fields_in_row):
                if skip_counter > 0:
                    skip_counter -= 1
                    continue

                num = self.board.board_data[i][j]
                temp_j_index = j + 1
                if num:
                    while temp_j_index < self._num_of_fields_in_row and self.board.board_data[
                            i][temp_j_index] is None:
                        temp_j_index += 1
                        skip_counter += 1
                    if temp_j_index < self._num_of_fields_in_row:
                        if self.board.board_data[i][temp_j_index] == num:
                            self.board.board_data[i][j] = None
                            self.board.board_data[i][temp_j_index] = 2*num
                            skip_counter += 1
            # if you are done changing the row,
            # you need to move fields to the right if it's possible
            row = self.board.board_data[i]
            filter_none_values = [num for num in row if num is not None]
            fill_none_values = [None]*(self._num_of_fields_in_row - len(filter_none_values))
            self.board.board_data[i] = fill_none_values + filter_none_values
