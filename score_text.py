import pygame


class ScoreText(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, damage: str, color: tuple[int, int, int],
                 font: pygame.font.Font):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.image = self.font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        self.creation_time = pygame.time.get_ticks()
        self.cooldown = 200

    def update(self) -> None:
        # move damage text up
        self.rect.y -= 2

        self.counter += 1
        if self.counter > 30:
            self.kill()
