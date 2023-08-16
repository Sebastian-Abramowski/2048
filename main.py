import pygame
import constants
import utilities
import info_printer
from expectimax import expectimax
from board import Board
from game import Game

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("2048")

clock = pygame.time.Clock()

# load sound effect
merge_sound = pygame.mixer.Sound("Assets/merge_sound.wav")
merge_sound.set_volume(0.2)

if_restart_game = False

icon_img = pygame.image.load("Assets/icon.png")
pygame.display.set_icon(icon_img)

restart_button_img = pygame.image.load("Assets/restart_button.png").convert_alpha()
restart_button_img = utilities.scale_img(
    restart_button_img, constants.RESTART_BUTTON_SCALE
)
restart_button = None

undo_button_img = pygame.image.load("Assets/small_undo_button.png").convert_alpha()
undo_button_img = utilities.scale_img(undo_button_img, constants.UNDO_BUTTON_SCALE)
undo_button = None

best_score = utilities.read_best_score_from_file(constants.SCORES_FILE_PATH)

board = Board(game_start=True)
game = Game(board)

run = True
while run:
    clock.tick(constants.FPS)
    screen.fill(constants.BACKGROUND_COLOR)

    restart_button, undo_button, score_rect_center = info_printer.draw_game_info(
        screen,
        restart_button, restart_button_img,
        undo_button, undo_button_img,
        game.score, best_score,
    )

    game.board.draw(screen, 6 * constants.PADDING)

    if restart_button.draw(screen) and not if_restart_game:
        game.restart_game(constants.SCORES_FILE_PATH)

        if_restart_game = True

    if_there_was_no_win_or_blockade = not game.if_blocked and not game.if_moving_is_blocked
    if undo_button.draw(screen) and not game.if_undo_move and if_there_was_no_win_or_blockade:
        game.undo_last_move()

    if not game.if_started:
        info_printer.draw_helping_text_three_parts(screen, 5 * constants.PADDING - 10, "Press ", "'enter'",
                                                   " for the bot to play", constants.SMALL_FONT2,
                                                   constants.SMALL_LIGHT_FONT2)

    game.score_text_group.update()
    game.score_text_group.draw(screen)

    if Game.check_for_win(game.board) and not game.if_skip_win and not game.if_ai_play:
        info_printer.draw_end_of_game_info(screen, "YOU WON!", "Press 'space' to continue",
                                           constants.GREEN)
        game.if_moving_is_blocked = True

    if Game.check_if_blocked(game.board):
        info_printer.draw_end_of_game_info(screen, "GAME OVER!", "Press 'space' to restart",
                                           constants.BLACK)
        game.if_blocked = True

    if best_score < game.score:
        utilities.update_best_score_in_file(constants.SCORES_FILE_PATH, game.score, game.if_ai_play)
        best_score = game.score

    # AI move
    if game.if_ai_play and not game.if_moving_is_blocked and not game.if_blocked:
        _, best_direction = expectimax(game.board, 4, True)
        if best_direction:
            game.move(best_direction, if_save_last_move=False)
            game.board.add_new_random_field()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.update_score_in_file(constants.SCORES_FILE_PATH)
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if_restart_game = False
        if event.type == pygame.KEYDOWN:
            if not game.if_moving_is_blocked and not game.if_ai_play:
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    if game.move("left", score_rect_center):
                        game.if_started = True
                        game.board.add_new_random_field()
                        merge_sound.play()
                if event.key in [pygame.K_d, pygame.K_RIGHT]:
                    if game.move("right", score_rect_center):
                        game.if_started = True
                        game.board.add_new_random_field()
                        merge_sound.play()
                if event.key in [pygame.K_w, pygame.K_UP]:
                    if game.move("up", score_rect_center):
                        game.if_started = True
                        game.board.add_new_random_field()
                        merge_sound.play()
                if event.key in [pygame.K_s, pygame.K_DOWN]:
                    if game.move("down", score_rect_center):
                        game.if_started = True
                        game.board.add_new_random_field()
                        merge_sound.play()
            if event.key == pygame.K_ESCAPE:
                game.update_score_in_file(constants.SCORES_FILE_PATH)
                run = False
            if event.key == pygame.K_SPACE:
                if game.if_moving_is_blocked:  # win case
                    game.if_moving_is_blocked = False
                    game.if_skip_win = True
                if game.if_blocked:
                    game.restart_game(constants.SCORES_FILE_PATH)
            if event.key == pygame.K_RETURN:  # enter, turn on the bot
                if not game.if_started:
                    game.if_started = True
                    game.if_ai_play = True

    pygame.display.update()

pygame.quit()
