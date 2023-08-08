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
            self._add_two_random_fields()

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
        for i, row in enumerate(self.board_data):
            field_y = initial_y + (i + 1) * constants.BOARD_PADDING + i * field_height
            for j, num in enumerate(row):
                if num is None:
                    color = constants.LIGHT_GREY
                else:
                    color = constants.COLORS_FOR_NUMBERS.get(num, (237, 197, 63))
                field_x = constants.PADDING + (j + 1) * constants.BOARD_PADDING + j * field_width
                field_rect = pygame.Rect(field_x, field_y, field_width, field_height)
                pygame.draw.rect(surface, color, field_rect)
                field_center = field_rect.center

                if num is not None:
                    color = constants.DARK_GREY if num in [2, 4] else constants.WHITE
                    field_num_width, field_num_height = utilities.get_size_of_text(str(num), constants.MEDIUM_FONT)
                    utilities.draw_text(surface, str(num), constants.MEDIUM_FONT, color,
                                        field_center[0] - field_num_width // 2,
                                        field_center[1] - field_num_height // 2)

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

    def _add_two_random_fields(self):
        # Used at the beginning of the game
        counter = 0
        while counter != 2:
            random_field = random.choices(range(4), k=2)
            random_number = random.choice([2, 4])

            if not self.board_data[random_field[0]][random_field[1]]:
                self.board_data[random_field[0]][random_field[1]] = random_number
                counter += 1

    def add_new_random_field(self):
        empty_fields = self.get_empty_fields()
        if empty_fields:
            random_field = random.choice(empty_fields)
            random_number = random.choice([2, 4])
            self.board_data[random_field[0]][random_field[1]] = random_number
            return True
        return False

    def get_empty_fields(self):
        empty_fields = []
        for i, row in enumerate(self.board_data):
            for j, num in enumerate(row):
                if num is None:
                    empty_fields.append((i, j))
        return empty_fields
