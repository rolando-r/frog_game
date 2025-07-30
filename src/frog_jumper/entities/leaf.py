import pygame

class Leaf:
    def __init__(self, image: pygame.Surface, position: tuple[int, int]) -> None:
        self.image = image
        self.rect = self.image.get_rect(center=position)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)