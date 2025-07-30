import pygame

class Menu:
    def __init__(self, screen: pygame.Surface, assets: dict) -> None:
        self.screen = screen
        self.options = ['PLAY', 'QUIT']
        self.selected = 0
        self.font = pygame.font.SysFont(None, 48)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None

    def draw(self) -> None:
        for index, option in enumerate(self.options):
            color = (255, 0, 0) if index == self.selected else (0, 0, 0)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() / 2, 200 + index * 60))
            self.screen.blit(text, rect)