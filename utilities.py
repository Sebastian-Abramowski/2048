import pygame


def draw_text(surface, text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    surface.blit(img, (x, y))

    return img.get_width(), img.get_height()


def get_size_of_text(text, font):
    img = font.render(text, True, (0, 0, 0))

    return img.get_width(), img.get_height()


def scale_img(image, scale):
    width = image.get_width()
    height = image.get_height()
    new_iamge = pygame.transform.scale(image, (width * scale, height * scale))
    return new_iamge


def read_best_score_from_file(file_path):
    with open(file_path, 'r') as file_handle:
        for line in file_handle:
            return int(line)


def update_best_score_in_file(file_path, new_best_score):
    with open(file_path, 'w') as file_handle:
        file_handle.write(str(new_best_score))
