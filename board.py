import pygame
import constants
import utilities


class Board():
    def __init__(self, board_data: list):
        self.board_data = board_data

    def draw(self, surface, initial_y):
        self._draw_board_background(surface, constants.DARK_GREY, initial_y)

        field_width, field_height = self._calc_width_height_of_field(initial_y)

        self._draw_fields(surface, initial_y, field_width, field_height)

    def _draw_board_background(self, surface, color, initial_y):
        pygame.draw.rect(surface, color, pygame.Rect(50, initial_y, constants.SCREEN_WIDTH - 2*constants.PADDING,
                                                     constants.SCREEN_HEIGHT - initial_y - constants.PADDING))

    def _draw_fields(self, surface, initial_y, field_width, field_height):
        for i, row in enumerate(self.board_data):
            field_y = initial_y + (i+1)*constants.BOARD_PADDING + i*field_height
            for j, num in enumerate(row):
                color = constants.COLORS_FOR_NUMBERS.get(num, (237, 197, 63))
                field_x = constants.PADDING + (j+1)*constants.BOARD_PADDING + j*field_width
                field_rect = pygame.Rect(field_x, field_y, field_width, field_height)
                pygame.draw.rect(surface, color, field_rect)
                field_center = field_rect.center

                color = constants.DARK_GREY if num in [2, 4] else constants.WHITE
                field_num_width, field_num_height = utilities.get_size_of_text(str(num), constants.MEDIUM_FONT)
                utilities.draw_text(surface, str(num), constants.MEDIUM_FONT, color,
                                    field_center[0] - field_num_width // 2,
                                    field_center[1] - field_num_height // 2)

    def _calc_width_height_of_field(self, initial_y):
        board_width = constants.SCREEN_WIDTH - 2*constants.PADDING
        width_for_fields = board_width - 5*constants.BOARD_PADDING

        board_height = constants.SCREEN_HEIGHT - initial_y - constants.PADDING
        height_for_fields = board_height - 5*constants.BOARD_PADDING

        return width_for_fields // 4, height_for_fields // 4


