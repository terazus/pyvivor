from os import path
import pygame

from pyvivor.utils import FONT_PATH, configurator, BUTTONS_PATH, game_status
from pyvivor.utils import leave_game


OFFSETS = {
    'START': 200,
    'SHOP': 370,
    'QUIT': 620
}
ACTIONS = {
    'START': game_status.start_game,
    'SHOP': game_status.start_shopping,
    'QUIT': leave_game
}

buttons_spreadsheet_path = path.join(BUTTONS_PATH, 'converted2.png')
buttons_spreadsheet = pygame.image.load(buttons_spreadsheet_path).convert_alpha()
button_image = pygame.transform.scale(
    buttons_spreadsheet.subsurface(pygame.Rect(300, 1780, 1100, 550)),
    (300, 150)
)


class WelcomeScreenButton(pygame.sprite.Sprite):
    def __init__(self, text, groups):
        super().__init__(groups)
        self.rectangle = None
        self.button_surface = None

        # Fonts
        font = pygame.font.Font(FONT_PATH, 32)
        self.button_text = font.render(text, True, 'white')

        # Style
        self.height = 150
        self.width = 300
        self.position_x = (configurator.screen_width // 2) - self.width // 2
        self.position_y = ((configurator.screen_height - configurator.screen_height) // 2
                           + (15 * configurator.screen_height // 100))
        self.offset = OFFSETS[text]

        # Interaction
        self.is_hovering = False
        self.hover_rectangle = None
        self.action = ACTIONS[text]

    def update(self):
        self.create_button()
        self.hovering()
        self.click()
        self.button_surface.blit(
            self.button_text,
            (
                (self.width - self.button_text.get_width()) // 2,
                button_image.get_height() // 2 - self.button_text.get_height() // 2
            )
        )

    def create_button(self):
        button_surface_position = (self.width, self.height)
        button_surface = pygame.Surface(button_surface_position, pygame.SRCALPHA).convert_alpha()
        rect = pygame.Rect(0, 0, self.width, self.height)

        # draw image now
        button_surface.blit(button_image, rect)

        self.rect = rect
        self.button_surface = button_surface

    def hovering(self):
        rect = self.rect.move(self.position_x, self.position_y + self.offset)
        if rect.collidepoint(pygame.mouse.get_pos()):
            self.is_hovering = True
            try:
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            except Exception:
                pass
        else:
            if self.is_hovering:
                self.is_hovering = False
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    def click(self):
        mouse = pygame.mouse.get_pressed()
        rect = self.rect.move(self.position_x, self.position_y + self.offset)
        if rect.collidepoint(pygame.mouse.get_pos()) and mouse[0]:
            self.action()
