import pygame
import constants
import utilities
import random
import copy
import math
import numpy as np
from typing import Union, Optional


class Board():
    def __init__(self, board_data: Optional[list[list[Union[int, None]]]] = None, game_start: bool = False,
                 num_of_fields_in_row: int = constants.NUM_OF_FIELDS_IN_ROW):
        self.num_of_fields_in_row = num_of_fields_in_row
        board_data = self._get_empty_list() if not board_data else board_data
        self.board_data = np.array(board_data, dtype=object)
        if game_start:
            self.add_new_random_field()
            self.add_new_random_field()

    def __deepcopy__(self, memo=None):
        new_board = Board(num_of_fields_in_row=self.num_of_fields_in_row)
        new_board.board_data = copy.deepcopy(self.board_data)

        return new_board

    def __str__(self) -> str:
        return str(self.board_data)

    def draw(self, surface: pygame.Surface, initial_y: int) -> None:
        self._draw_board_background(surface, constants.DARK_GREY, initial_y)
        field_width, field_height = self._calc_width_height_of_field(initial_y)
        self._draw_fields(surface, initial_y, field_width, field_height)

    def _draw_board_background(self, surface: pygame.Surface, color: tuple[int, int, int],
                               initial_y: int) -> None:
        pygame.draw.rect(surface, color, pygame.Rect(50, initial_y, constants.SCREEN_WIDTH - 2 * constants.PADDING,
                                                     constants.SCREEN_HEIGHT - initial_y - constants.PADDING))

    def _draw_fields(self, surface: pygame.Surface, initial_y: int,
                     field_width: int, field_height: int) -> None:
        for row_index, row in enumerate(self.board_data):
            # Calculate y coordinate for each row of fields
            field_y = initial_y + (row_index + 1) * constants.BOARD_PADDING + row_index * field_height
            for column_index, num in enumerate(row):
                color = self._get_color_for_field(num)
                field_center = self._draw_field(surface, color, field_width, field_height,
                                                column_index, field_y)
                self._draw_number_on_field(surface, num, field_center)

    def _calc_width_height_of_field(self, initial_y: int) -> tuple[int, int]:
        board_width = constants.SCREEN_WIDTH - 2 * constants.PADDING
        width_for_fields = board_width - (self.num_of_fields_in_row + 1) * constants.BOARD_PADDING

        board_height = constants.SCREEN_HEIGHT - initial_y - constants.PADDING
        height_for_fields = board_height - (self.num_of_fields_in_row + 1) * constants.BOARD_PADDING

        return (width_for_fields // self.num_of_fields_in_row,
                height_for_fields // self.num_of_fields_in_row)

    def _get_empty_list(self) -> list[list[None]]:
        """
        Returns two dimensional list filled with None values according
        to number of fields in a row
        """
        temp_board_data = []
        for _ in range(self.num_of_fields_in_row):
            temp_board_data.append([None] * self.num_of_fields_in_row)
        return temp_board_data

    def add_new_random_field(self) -> bool:
        empty_fields = self.get_empty_fields()
        if empty_fields:
            random_field = random.choice(empty_fields)

            possible_numbers = [2, 4]
            probabilities = [0.9, 0.1]  # 2 - 90%, 4 - 10%
            random_number = random.choices(possible_numbers, probabilities, k=1)[0]

            self.board_data[random_field[0]][random_field[1]] = random_number
            return True
        return False

    def get_empty_fields(self) -> list[tuple[int, int]]:
        empty_fields = []
        for i, row in enumerate(self.board_data):
            for j, num in enumerate(row):
                if not num:
                    empty_fields.append((i, j))
        return empty_fields

    def _get_color_for_field(self, num: int) -> tuple[int, int, int]:
        if num is None:
            color = constants.LIGHT_GREY
        else:
            color = constants.COLORS_FOR_NUMBERS.get(num, constants.YELLOW)
        return color

    def _draw_number_on_field(self, surface: pygame.Surface, num: int,
                              field_center: tuple[int, int]) -> None:
        if num:
            color = constants.DARK_GREY if num in [2, 4] else constants.WHITE
            field_num_width, field_num_height = utilities.get_size_of_text(str(num),
                                                                           constants.MEDIUM_FONT)
            utilities.draw_text(surface, str(num), constants.MEDIUM_FONT, color,
                                field_center[0] - field_num_width // 2,
                                field_center[1] - field_num_height // 2)

    def _draw_field(self, surface: pygame.Surface, color: tuple[int, int, int], field_width: int,
                    field_height: int, column_index: int, field_y: int) -> tuple[int, int]:
        field_x = constants.PADDING + (column_index + 1) * constants.BOARD_PADDING + column_index * field_width
        field_rect = pygame.Rect(field_x, field_y, field_width, field_height)
        pygame.draw.rect(surface, color, field_rect)
        field_center = field_rect.center

        return field_center

    def evaluate(self) -> float:
        _, if_best_in_left_top_corner = self._get_max_value()
        _, if_second_largest_in_first_row, if_second_largest_in_fist_column = self._get_second_largest_value()

        corner_boost = 370 if if_best_in_left_top_corner else 0

        second_largest_value_penalty = 0 if if_second_largest_in_first_row or\
            if_second_largest_in_fist_column else 180
        penalty_for_blocked_fields = self._count_blocked_fields() * 75
        penalty_blocked_top_right_corner = 175 if self._check_if_field_in_top_right_corner_is_blocked() else 0
        penalties = second_largest_value_penalty + penalty_for_blocked_fields + penalty_blocked_top_right_corner

        empty_fields_score = self._get_num_of_empty_fields() * 60
        spreading_score = self._evaluate_spreading() * 7
        smoothness_score = self._evaluate_smoothness() * 4

        return empty_fields_score + spreading_score + corner_boost - penalties - smoothness_score

    def _get_max_value(self) -> tuple[int, bool]:
        values = [num for row in self.board_data for num in row if num]
        max_value = max(values)
        if_in_left_top_corner = self.board_data[0][0] == max_value
        return max(values), if_in_left_top_corner

    def _get_second_largest_value(self) -> tuple[int, bool, bool]:
        values = self.board_data.flatten()
        values = [num for num in values if num]
        indexes_of_sorted = np.argsort(values)[-2:]
        second_largest = values[indexes_of_sorted[0]]
        if_in_first_row = second_largest in self.board_data[0]
        if_in_first_column = second_largest in self.board_data[:, 0]

        return second_largest, if_in_first_row, if_in_first_column

    def _get_sum_of_values(self) -> int:
        return sum([num for row in self.board_data for num in row if num])

    def _get_num_of_empty_fields(self) -> int:
        return len([field for row in self.board_data for field in row if not field])

    def _increase_eval_if_sorted_reversedly(self, values: np.array, eval_value: int) -> int:
        # used for 1 dimensional arrays
        if not np.any(values == None):
            if np.array_equal(values, np.sort(values)[::-1]):
                eval_value += np.size(values)
        return eval_value

    def _evaluate_spreading(self) -> float:
        evaluation_value = 0

        evaluation_value += self._evaluate_spreading_rows()
        evaluation_value += self._evaluate_spreading_columns()
        # reducing the value of diagonal evaluation
        evaluation_value += self._evaluate_spreading_diagonal() / 2

        return evaluation_value

    def _evaluate_spreading_rows(self):
        evaluation_value = 0

        for i in range(self.num_of_fields_in_row):
            eval_booster = 1 if i != 0 else 9
            row = self.board_data[i, :]
            copied_row_without_nones_at_end = utilities.remove_none_values_from_the_end_of_numpy_list(row)
            evaluation_value = self._increase_eval_if_sorted_reversedly(copied_row_without_nones_at_end,
                                                                        evaluation_value)
            evaluation_value *= eval_booster

        return evaluation_value

    def _evaluate_spreading_columns(self):
        evaluation_value = 0

        for j in range(self.num_of_fields_in_row):
            column = self.board_data[:, j]
            copied_column_without_nones_at_end = utilities.remove_none_values_from_the_end_of_numpy_list(column)
            evaluation_value = self._increase_eval_if_sorted_reversedly(copied_column_without_nones_at_end,
                                                                        evaluation_value)

        return evaluation_value

    def _evaluate_spreading_diagonal(self):
        evaluation_value = 0

        # signle diagonal NW - SE
        diagonal_nw_se = np.diagonal(self.board_data)
        copied_diagonal_without_nones_at_end = utilities.remove_none_values_from_the_end_of_numpy_list(
            diagonal_nw_se)
        evaluation_value = self._increase_eval_if_sorted_reversedly(copied_diagonal_without_nones_at_end,
                                                                    evaluation_value)

        return evaluation_value

    def _count_blocked_fields(self):
        blocked_fields = 0

        blocked_fields += self._count_blocked_fields_along_borders_without_corners()
        blocked_fields += self._count_blocked_fields_in_corners()
        blocked_fields += self._count_blocked_fields_inside()

        return blocked_fields

    def _count_blocked_fields_in_corners(self):
        num_of_blocked_fields = 0
        max_index = self.num_of_fields_in_row - 1

        # check left top corner
        if self.board_data[0][0] and self.board_data[0][1] and self.board_data[1][0] and \
                2 * self.board_data[0][0] <= self.board_data[0][1] and \
                2 * self.board_data[0][0] <= self.board_data[1][0]:
            num_of_blocked_fields += 1

        # check right top corner
        if self.board_data[0][max_index] and self.board_data[0][max_index - 1] and \
                self.board_data[1][max_index] and \
                2 * self.board_data[0][max_index] <= self.board_data[0][max_index - 1] and \
                2 * self.board_data[0][max_index] <= self.board_data[1][max_index]:
            num_of_blocked_fields += 1

        # check left down corner
        if self.board_data[max_index][0] and self.board_data[max_index][1] and \
                self.board_data[max_index - 1][0] and \
                2 * self.board_data[max_index][0] <= self.board_data[max_index - 1][0] and \
                2 * self.board_data[max_index][0] <= self.board_data[max_index][1]:
            num_of_blocked_fields += 1

        # check right down corner
        if self.board_data[max_index][max_index] and self.board_data[max_index][max_index - 1] and \
                self.board_data[max_index - 1][max_index] and \
                2 * self.board_data[max_index][max_index] <= self.board_data[max_index][max_index - 1] and \
                2 * self.board_data[max_index][max_index] <= self.board_data[max_index - 1][max_index]:
            num_of_blocked_fields += 1

        return num_of_blocked_fields

    def _count_blocked_fields_along_borders_without_corners(self):
        num_of_blocked_fields = 0
        max_index = self.num_of_fields_in_row - 1

        for i in range(1, max_index):
            # top border
            if self.board_data[0][i] and self.board_data[0][i - 1] and self.board_data[0][i + 1] and \
                    self.board_data[1][i] and 2 * self.board_data[0][i] <= self.board_data[0][i - 1] and \
                    2 * self.board_data[0][i] <= self.board_data[0][i + 1] and \
                    2 * self.board_data[0][i] <= self.board_data[1][i]:
                num_of_blocked_fields += 1

            # bottom border
            if self.board_data[max_index][i] and self.board_data[max_index][i - 1] and \
                    self.board_data[max_index][i + 1] and self.board_data[max_index - 1][i] and \
                    2 * self.board_data[max_index][i] <= self.board_data[max_index][i - 1] and \
                    2 * self.board_data[max_index][i] <= self.board_data[max_index][i + 1] and \
                    2 * self.board_data[max_index][i] <= self.board_data[max_index - 1][i]:
                num_of_blocked_fields += 1

            # right border
            if self.board_data[i][max_index] and self.board_data[i - 1][max_index] and \
                    self.board_data[i + 1][max_index] and self.board_data[i][max_index - 1] and \
                    2 * self.board_data[i][max_index] <= self.board_data[i - 1][max_index] and \
                    2 * self.board_data[i][max_index] <= self.board_data[i + 1][max_index] and \
                    2 * self.board_data[i][max_index] <= self.board_data[i][max_index - 1]:
                num_of_blocked_fields += 1

            # left border
            if self.board_data[i][0] and self.board_data[i - 1][0] and self.board_data[i + 1][0] and \
                    self.board_data[i][1] and \
                    2 * self.board_data[i][0] <= self.board_data[i - 1][0] and \
                    2 * self.board_data[i][0] <= self.board_data[i + 1][0] and \
                    2 * self.board_data[i][0] <= self.board_data[i][1]:
                num_of_blocked_fields += 1

        return num_of_blocked_fields

    def _count_blocked_fields_inside(self):
        num_of_blocked_fields = 0
        max_index = self.num_of_fields_in_row - 1

        def is_blocked_around(row: int, col: int) -> None:
            if self.board_data[row][col] and self.board_data[row - 1][col] and \
                    self.board_data[row + 1][col] and self.board_data[row][col - 1] and \
                    self.board_data[row][col + 1] and \
                    2 * self.board_data[row][col] <= self.board_data[row - 1][col] and \
                    2 * self.board_data[row][col] <= self.board_data[row + 1][col] and \
                    2 * self.board_data[row][col] <= self.board_data[row][col - 1] and \
                    2 * self.board_data[row][col] <= self.board_data[row][col + 1]:
                return True
            return False

        for row_index in range(1, max_index):
            for col_index in range(1, max_index):
                if is_blocked_around(row_index, col_index):
                    num_of_blocked_fields += 1

        return num_of_blocked_fields

    def _check_if_field_in_top_right_corner_is_blocked(self) -> bool:
        max_index = self.num_of_fields_in_row - 1

        # check right top corner
        if self.board_data[0][max_index] and self.board_data[0][max_index - 1] and \
                self.board_data[1][max_index] and \
                2 * self.board_data[0][max_index] <= self.board_data[0][max_index - 1] and \
                2 * self.board_data[0][max_index] <= self.board_data[1][max_index]:
            return True
        return False

    def _evaluate_smoothness(self) -> int:
        # The less, the better smoothness of the board
        return 2 * self._evaluate_smoothness_in_rows() + self._evalute_smoothness_in_columns()

    def _evaluate_smoothness_in_rows(self) -> int:
        overall_difference = 0

        for row in range(self.num_of_fields_in_row):
            for column in range(self.num_of_fields_in_row - 1):
                value = self.board_data[row][column]
                value_on_right = self.board_data[row][column + 1]
                if value and value_on_right:
                    differnce = math.log(max(value, value_on_right) // min(value, value_on_right), 2)
                    overall_difference += differnce

        return overall_difference

    def _evalute_smoothness_in_columns(self) -> int:
        overall_difference = 0

        for column in range(self.num_of_fields_in_row):
            for row in range(self.num_of_fields_in_row - 1):
                value = self.board_data[row][column]
                value_below = self.board_data[row + 1][column]

                if value and value_below:
                    differnce = math.log(max(value, value_below) // min(value, value_below), 2)
                    overall_difference += differnce

        return overall_difference
