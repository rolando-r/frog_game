import os, pygame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_image(path: str) -> pygame.Surface:
    return pygame.image.load(path).convert_alpha()


def load_sound(path: str) -> pygame.mixer.Sound:
    return pygame.mixer.Sound(path)


def scale_image(image: pygame.Surface, scale: float) -> pygame.Surface:
    width = int(image.get_width() * scale)
    height = int(image.get_height() * scale)
    return pygame.transform.scale(image, (width, height))