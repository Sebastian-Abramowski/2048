from pygame import font

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000

FPS = 60

BACKGROUND_COLOR = (251, 248, 240)
DARK_GREY = (116, 110, 106)
LIGHT_GREY = (160, 152, 157)
LIGHT_BROWN = (187, 173, 160)
WHITE = (255, 255, 255)

font.init()
BIG_FONT = font.Font("Roboto-Black.ttf", 120)
NORMAL_FONT = font.Font("Roboto-Black.ttf", 30)
NORMAL_LIGHT_FONT = font.Font("Roboto-Light.ttf", 30)
SMALL_FONT = font.Font("Roboto-Black.ttf", 15)
PADDING = 50

RESTART_BUTTON_SCALE = 1/8
SCORE_BOX_WIDTH = 170
SCORE_BOX_HEIGHT = 80
