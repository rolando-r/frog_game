import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    def __init__(self, image: pygame.Surface, position: tuple[int, int]) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect(topleft=position)

    def update(self) -> None:
        pass  # Los enemigos estáticos no se mueven

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
