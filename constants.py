from pygame import font

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000

FPS = 60

BACKGROUND_COLOR = (251, 248, 240)
DARK_GREY = (116, 110, 106)
GREY = (160, 152, 157)
LIGHT_GREY = (214, 205, 196)
LIGHT_BROWN = (187, 173, 160)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

COLORS_FOR_NUMBERS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 96),
    64: (246, 94, 59),
    128: (237, 207, 115),
    256: (237, 204, 98),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 45),
}


font.init()
BIG_FONT = font.Font("Roboto-Black.ttf", 120)
NORMAL_FONT = font.Font("Roboto-Black.ttf", 30)
NORMAL_LIGHT_FONT = font.Font("Roboto-Light.ttf", 30)
SMALL_FONT = font.Font("Roboto-Black.ttf", 15)
MEDIUM_FONT = font.Font("Roboto-Black.ttf", 50)

PADDING = 50
BOARD_PADDING = 15
NUM_OF_FIELDS_IN_ROW = 4

RESTART_BUTTON_SCALE = 1 / 8
UNDO_BUTTON_SCALE = 1
SCORE_BOX_WIDTH = 170
SCORE_BOX_HEIGHT = 80
