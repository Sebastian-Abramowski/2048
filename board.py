import pygame
import constants
import utilities
import random


class Board():
    def __init__(self, board_data=None, game_start=False,
                 num_of_fields_in_row=constants.NUM_OF_FIELDS_IN_ROW):
        self.num_of_fields_in_row = num_of_fields_in_row
        board_data = self._get_empty_board() if not board_data else board_data
        self.board_data = board_data
        if game_start:
            self.add_new_random_field()
            self.add_new_random_field()

    def __str__(self):
        result = ""
        for row in self.board_data:
            str_row = [str(item) if item is not None else 'X' for item in row]
            result += ' '.join(str_row)
            result += '\n'
        return result

    def draw(self, surface, initial_y):
        self._draw_board_background(surface, constants.DARK_GREY, initial_y)

        field_width, field_height = self._calc_width_height_of_field(initial_y)

        self._draw_fields(surface, initial_y, field_width, field_height)

    def _draw_board_background(self, surface, color, initial_y):
        pygame.draw.rect(surface, color, pygame.Rect(50, initial_y, constants.SCREEN_WIDTH - 2 * constants.PADDING,
                                                     constants.SCREEN_HEIGHT - initial_y - constants.PADDING))

    def _draw_fields(self, surface, initial_y, field_width, field_height):
        for row_index, row in enumerate(self.board_data):
            # Calculate y coordinate for each row of fields
            field_y = initial_y + (row_index + 1) * constants.BOARD_PADDING + row_index * field_height
            for column_index, num in enumerate(row):
                color = self._get_color_for_field(num)

                field_center = self._draw_field(surface, color, field_width, field_height,
                                                column_index, field_y)

                self._draw_number_on_field(surface, num, field_center)

    def _calc_width_height_of_field(self, initial_y):
        board_width = constants.SCREEN_WIDTH - 2 * constants.PADDING
        width_for_fields = board_width - (self.num_of_fields_in_row + 1) * constants.BOARD_PADDING

        board_height = constants.SCREEN_HEIGHT - initial_y - constants.PADDING
        height_for_fields = board_height - (self.num_of_fields_in_row + 1) * constants.BOARD_PADDING

        return (width_for_fields // self.num_of_fields_in_row,
                height_for_fields // self.num_of_fields_in_row)

    def _get_empty_board(self):
        temp_board_data = []
        for _ in range(self.num_of_fields_in_row):
            temp_board_data.append([None] * self.num_of_fields_in_row)
        return temp_board_data

    def add_new_random_field(self):
        empty_fields = self.get_empty_fields()
        if empty_fields:
            random_field = random.choice(empty_fields)

            possible_numbers = [2, 4]
            probabilities = [0.9, 0.1]  # 2 - 90%, 4 - 10%
            random_number = random.choices(possible_numbers, probabilities, k=1)[0]

            self.board_data[random_field[0]][random_field[1]] = random_number
            return True
        return False

    def get_empty_fields(self):
        empty_fields = []
        for i, row in enumerate(self.board_data):
            for j, num in enumerate(row):
                if not num:
                    empty_fields.append((i, j))
        return empty_fields

    def _get_color_for_field(self, num):
        if num is None:
            color = constants.LIGHT_GREY
        else:
            color = constants.COLORS_FOR_NUMBERS.get(num, constants.YELLOW)
        return color

    def _draw_number_on_field(self, surface, num, field_center):
        if num:
            color = constants.DARK_GREY if num in [2, 4] else constants.WHITE
            field_num_width, field_num_height = utilities.get_size_of_text(str(num), constants.MEDIUM_FONT)
            utilities.draw_text(surface, str(num), constants.MEDIUM_FONT, color,
                                field_center[0] - field_num_width // 2,
                                field_center[1] - field_num_height // 2)

    def _draw_field(self, surface, color, field_width, field_height, column_index, field_y):
        field_x = constants.PADDING + (column_index + 1) * constants.BOARD_PADDING + column_index * field_width
        field_rect = pygame.Rect(field_x, field_y, field_width, field_height)
        pygame.draw.rect(surface, color, field_rect)
        field_center = field_rect.center

        return field_center
