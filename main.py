import pygame
import constants
import utilities
from board import Board
from game import Game
from info_printer import draw_game_info, draw_end_of_game_info

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

best_score = utilities.read_best_score_from_file("best_score.txt")

board = Board([[1024, 1024, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]], game_start=True)
game = Game(board)

run = True
while run:
    clock.tick(constants.FPS)
    screen.fill(constants.BACKGROUND_COLOR)

    restart_button, undo_button, score_rect_center = draw_game_info(
        screen,
        restart_button, restart_button_img,
        undo_button, undo_button_img,
        game.score, best_score,
    )

    board.draw(screen, 6 * constants.PADDING)

    if restart_button.draw(screen) and not if_restart_game:
        game.update_scores_in_file("best_score.txt")
        game.score = 0
        game.score_text_group.empty()
        board = Board(game_start=True)
        game.board = board

        if_restart_game = True

    if undo_button.draw(screen) and not game.if_undo_move:
        game.undo_last_move()

    game.score_text_group.update()
    game.score_text_group.draw(screen)

    if game.check_for_win() and not game.if_skip_win and not game.if_ai_play:
        draw_end_of_game_info(screen, if_win=True)
        game.if_blocked_moving = True

    if best_score < game.score:
        utilities.update_best_score_in_file("best_score.txt", game.score, game.if_ai_play)
        best_score = game.score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.update_scores_in_file("best_score.txt")
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if_restart_game = False
        if event.type == pygame.KEYDOWN:
            if not game.if_blocked_moving:
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    if game.move_horiziontally("left", score_rect_center):
                        board.add_new_random_field()
                        merge_sound.play()
                if event.key in [pygame.K_d, pygame.K_RIGHT]:
                    if game.move_horiziontally("right", score_rect_center):
                        board.add_new_random_field()
                        merge_sound.play()
                if event.key in [pygame.K_w, pygame.K_UP]:
                    if game.move_vertically("up", score_rect_center):
                        board.add_new_random_field()
                        merge_sound.play()
                if event.key in [pygame.K_s, pygame.K_DOWN]:
                    if game.move_vertically("down", score_rect_center):
                        board.add_new_random_field()
                        merge_sound.play()
            if event.key == pygame.K_ESCAPE:
                game.update_scores_in_file("best_score.txt")
                run = False
            if event.key == pygame.K_SPACE:
                game.if_skip_win = True
                game.if_blocked_moving = False

    pygame.display.update()

pygame.quit()
