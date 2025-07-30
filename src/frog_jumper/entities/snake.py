import pygame
from pygame.sprite import Sprite

class Snake(Sprite):
    def __init__(self, image: pygame.Surface, position: tuple[int, int]) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

    def update(self) -> None:
        # La serpiente estática
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)