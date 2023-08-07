import pygame
import constants
import utilities
from info_printer import draw_game_info
from board import Board

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("2048")

clock = pygame.time.Clock()

if_restart_game = False
if_undo_last_move = False

restart_button_img = pygame.image.load("restart_button.png").convert_alpha()
restart_button_img = utilities.scale_img(restart_button_img, constants.RESTART_BUTTON_SCALE)
restart_button = None

undo_button_img = pygame.image.load("small_undo_button.png").convert_alpha()
undo_button_img = utilities.scale_img(undo_button_img, constants.UNDO_BUTTON_SCALE)
undo_button = None

best_score = utilities.read_best_score_from_file("best_score.txt")

board = Board([[2, 4, 8, 16], [32, 64, 128, 256], [512, 1024, 2048, 4], [2, 2, 16, 99]])

run = True
while run:
    clock.tick(constants.FPS)
    screen.fill(constants.BACKGROUND_COLOR)

    restart_button, undo_button = draw_game_info(screen, restart_button, restart_button_img,
                                                 undo_button, undo_button_img, 25805, best_score)
    board.draw(screen, 6*constants.PADDING)

    if restart_button.draw(screen) and not if_restart_game:
        print("button pressed")
        if_restart_game = True

    if undo_button.draw(screen) and not if_undo_last_move:
        print("button2 pressed")
        if_undo_last_move = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if_restart_game = False
            if_undo_last_move = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                print("LEFT")
            if event.key in [pygame.K_d, pygame.K_RIGHT]:
                print("RIGHT")
            if event.key in [pygame.K_w, pygame.K_UP]:
                print("UP")
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                print("DOWN")
            if event.key == pygame.K_ESCAPE:
                print("ESCAPE")

    pygame.display.update()

pygame.quit()
