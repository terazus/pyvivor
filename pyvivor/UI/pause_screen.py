import pygame

from pyvivor.utils import configurator, FONT_PATH


class PauseScreen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.display_surface = configurator.game_screen
        self.position = (0, 0)
        self.size = (configurator.game_screen.get_width(), configurator.game_screen.get_height())
        font = pygame.font.Font(FONT_PATH, 64)
        self.text = font.render('PAUSE', True, 'red')
        self.alpha = 0

    def update(self):
        self.create_alpha()
        self.display_surface.blit(self.text, (configurator.game_screen.get_width()/2 - self.text.get_width()/2,
                                              configurator.game_screen.get_height()/2 - self.text.get_height()/2))

    def create_alpha(self):
        if self.alpha < 192:
            self.alpha += 8
        rect = pygame.Surface(self.size)
        rect.set_alpha(self.alpha)
        rect.fill('black')
        self.display_surface.blit(rect, self.position)