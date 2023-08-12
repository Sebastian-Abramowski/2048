import utilities
import constants
import pygame
from button import Button


def draw_game_title(surface, game_title: str) -> tuple[int, int]:
    text_width, text_height = utilities.draw_text(surface, game_title, constants.HUGE_FONT,
                                                  constants.DARK_GREY, constants.PADDING, constants.PADDING)

    return text_width, text_height


def draw_helping_text(surface: pygame.Surface, big_text_height: int) -> tuple[int, int]:
    coord_y_of_info_text = constants.PADDING + big_text_height
    info_text_width1, info_text_height = utilities.draw_text(surface, "Join the number and get to the ",
                                                             constants.NORMAL_LIGHT_FONT,
                                                             constants.GREY, constants.PADDING,
                                                             coord_y_of_info_text)
    info_text_width2, _ = utilities.draw_text(surface, "2048 tile!", constants.NORMAL_FONT, constants.DARK_GREY,
                                              constants.PADDING + info_text_width1, coord_y_of_info_text)
    info_text_width = info_text_width1 + info_text_width2

    return info_text_width, info_text_height


def draw_score_info_background(surface: pygame.Surface,
                               big_text_width: int) -> tuple[tuple[int, int], int, int, int, int]:
    coord_x_of_score_info = 2 * constants.PADDING + big_text_width
    rect_on_left = pygame.Rect(coord_x_of_score_info, constants.PADDING,
                               constants.SCORE_BOX_WIDTH, constants.SCORE_BOX_HEIGHT)
    pygame.draw.rect(surface, constants.LIGHT_BROWN, rect_on_left)
    score_text_width, score_text_height = utilities.get_size_of_text("SCORE", constants.SMALL_FONT)
    coord_y_of_scores_info = constants.PADDING + 10
    utilities.draw_text(surface, "SCORE", constants.SMALL_FONT, constants.BACKGROUND_COLOR,
                        coord_x_of_score_info + (constants.SCORE_BOX_WIDTH // 2) - (score_text_width // 2),
                        coord_y_of_scores_info)
    pygame.draw.rect(surface, constants.LIGHT_BROWN,
                     pygame.Rect(2 * constants.PADDING + big_text_width + constants.SCORE_BOX_WIDTH + 14,
                                 constants.PADDING, constants.SCORE_BOX_WIDTH, constants.SCORE_BOX_HEIGHT))
    best_text_width, best_score_text_height = utilities.get_size_of_text("BEST", constants.SMALL_FONT)
    utilities.draw_text(surface, "BEST", constants.SMALL_FONT, constants.BACKGROUND_COLOR,
                        coord_x_of_score_info + (
                            constants.SCORE_BOX_WIDTH // 2) - (
                            best_text_width // 2) + constants.SCORE_BOX_WIDTH + 14,
                        coord_y_of_scores_info)

    return [rect_on_left.center, coord_x_of_score_info,
            coord_y_of_scores_info, score_text_height, best_score_text_height]


def draw_scores(surface: pygame.Surface, score: int, best_score: int, coord_x_of_score_info: int,
                coord_y_of_scores_info: int, score_text_height: int, best_score_text_height: int) -> None:
    score_width, _ = utilities.get_size_of_text(str(score), constants.NORMAL_FONT)
    utilities.draw_text(surface, str(score), constants.NORMAL_FONT, constants.WHITE,
                        coord_x_of_score_info + (constants.SCORE_BOX_WIDTH // 2) - (score_width // 2),
                        coord_y_of_scores_info + score_text_height + 5)
    best_score_width, _ = utilities.get_size_of_text(str(best_score), constants.NORMAL_FONT)
    utilities.draw_text(surface, str(best_score), constants.NORMAL_FONT, constants.WHITE,
                        coord_x_of_score_info + (
                            constants.SCORE_BOX_WIDTH // 2) - (
                            best_score_width // 2) + constants.SCORE_BOX_WIDTH + 14,
                        coord_y_of_scores_info + best_score_text_height + 5)


def draw_game_info(surface: pygame.Surface, restart_button: Button, restart_button_img: pygame.Surface,
                   undo_button: Button, undo_button_img: pygame.Surface,
                   score: int, best_score: int) -> tuple[Button, Button, tuple[int, int]]:
    # Draw "2048"
    big_text_width, big_text_height = draw_game_title(surface, "2048")

    # Draw "Join the number and get to the 2048 tile!"
    info_text_width, _ = draw_helping_text(surface, big_text_height)

    # Draw boxes for information about score and the best score
    score_info = draw_score_info_background(surface, big_text_width)

    # Draw score and the best score
    draw_scores(surface, score, best_score, *score_info[1::])

    # Create restart_button (it is dependent on the text info sizes)
    if not restart_button:
        restart_button = Button(constants.PADDING + info_text_width + 25,
                                constants.PADDING + big_text_height,
                                restart_button_img)

    if not undo_button:
        px_move_right = restart_button_img.get_width() // 2 - undo_button_img.get_width() // 2
        undo_button = Button(constants.PADDING + info_text_width + 25 + px_move_right,
                             constants.PADDING + big_text_height + 38,
                             undo_button_img)

    background_score_rect_center = score_info[0]

    return restart_button, undo_button, background_score_rect_center


def draw_end_of_game_info(surface: pygame.Surface, text: str, secondary_text: str,
                          color: tuple[int, int, int]) -> None:
    text_width, text_height = utilities.get_size_of_text(text, constants.BIG_FONT)
    text_x = (constants.SCREEN_WIDTH - text_width) // 2
    text_y = (constants.SCREEN_HEIGHT - text_height) // 2 + 35
    utilities.draw_text(surface, text, constants.BIG_FONT, color, text_x, text_y)

    sec_text_width, sec_text_height = utilities.get_size_of_text(secondary_text, constants.NORMAL_FONT)
    sec_text_x = (constants.SCREEN_WIDTH - sec_text_width) // 2
    sec_text_y = (constants.SCREEN_HEIGHT - sec_text_height) // 2 + 95
    utilities.draw_text(surface, secondary_text, constants.NORMAL_FONT,
                        color, sec_text_x, sec_text_y)
