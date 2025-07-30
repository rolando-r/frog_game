import pygame
from pygame.sprite import Sprite

class Bird(Sprite):
    SPEED = 5

    def __init__(self, image: pygame.Surface, position: tuple[int, int], speed: int) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.speed = speed

    def update(self) -> None:
        self.rect.x += self.speed

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)