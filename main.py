import pygame
import constants
import utilities
from info_printer import draw_game_info

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("2048")

clock = pygame.time.Clock()

if_restart_game = False

restart_button_img = pygame.image.load("restart_button.png").convert_alpha()
restart_button_img = utilities.scale_img(restart_button_img, constants.RESTART_BUTTON_SCALE)
restart_button = None

best_score = utilities.read_best_score_from_file("best_score.txt")

run = True
while run:
    clock.tick(constants.FPS)
    screen.fill(constants.BACKGROUND_COLOR)

    restart_button = draw_game_info(screen, restart_button, restart_button_img, 25805, best_score)

    if restart_button.draw(screen) and not if_restart_game:
        print("button pressed")
        if_restart_game = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if_restart_game = False
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
