import pygame

from pyvivor.utils import configurator, FONT_PATH, GAME_TITLE
from .button import WelcomeScreenButton


class WelcomeScreen:
    def __init__(self):
        self.display_surface = configurator.game_screen

        # GROUPS
        self.buttons = pygame.sprite.Group()

        # TITLE
        self.game_title_text = pygame.font.Font(FONT_PATH, 64).render(f'Welcome to {GAME_TITLE}', True, 'white')
        surface_width = self.game_title_text.get_width()
        surface_height = configurator.screen_height
        self.surface = {
            'width': surface_width,
            'height': surface_height,
            'x': (configurator.screen_width - surface_width) // 2,
            'y': (configurator.screen_height - surface_height) // 2 + (15 * configurator.screen_height // 100)
        }

        # BUTTONS
        self.button_width = 300
        self.start_button = WelcomeScreenButton('START', self.buttons)
        self.shop_button = WelcomeScreenButton('SHOP', self.buttons)
        self.quit_button = WelcomeScreenButton('QUIT', self.buttons)

    def run(self):
        self.buttons.update()
        self.create_buttons()

    def create_buttons(self):
        surface = pygame.Surface((self.surface['width'], self.surface['height']), pygame.SRCALPHA).convert_alpha()
        surface_rect = surface.get_rect()
        surface.blit(self.game_title_text, ((self.surface['width'] - self.game_title_text.get_width()) // 2, 0))

        # Start button
        surface.blit(self.start_button.button_surface,
                     (surface_rect.centerx - self.button_width // 2, self.start_button.offset))

        # Shop button
        surface.blit(self.shop_button.button_surface,
                     (surface_rect.centerx - self.button_width // 2, self.shop_button.offset))

        # Quit button
        surface.blit(self.quit_button.button_surface,
                     (surface_rect.centerx - self.button_width // 2, self.quit_button.offset))

        self.display_surface.blit(surface, (self.surface['x'], self.surface['y']))
