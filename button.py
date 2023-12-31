import pygame


class Button():
    def __init__(self, x: int, y: int, image: pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw_and_check_if_clicked(self, surface: pygame.Surface) -> bool:
        action = False
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                action = True

        surface.blit(self.image, self.rect)
        return action
