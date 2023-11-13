"""
The GUI class implements the mask to position graphics on the screen. All UI elements are drawn on the mask and then
mask is rendered on the display surface.
"""
import pygame

from pyvivor.utils import configurator


class GUI:
    def __init__(self, player):
        self.player = player
        self.life_bar_data = {
            'width': 360,
            'height': 10,
            'position': (20, 30),
            'surface': configurator.game_screen,
            'color': 'red',
            'left_value': 0,
            'right_value': player.max_health,
            'current_value': player.current_health
        }
        self.energy_bar_data = {
            'width': 360,
            'height': 10,
            'position': (20, 45),
            'surface': configurator.game_screen,
            'color': 'green',
            'left_value': 0,
            'right_value': player.dash_cooldown,
            'current_value': player.dash_cooldown
        }
        self.exp_bar_data = {
            'width': 360,
            'height': 10,
            'position': (20, 60)
        }

        self.screen = configurator.game_screen
        self.surface_width = self.screen.get_width()
        self.surface_height = self.screen.get_height()
        self.surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)

        self.display_sprites = pygame.sprite.Group()
        self.exp_bar = Bar(surface=self.surface, **self.exp_bar_data)
        self.life_bar = Bar(**self.life_bar_data)
        self.energy_bar = Bar(**self.energy_bar_data)

    def update(self):
        self.exp_bar.current_value = self.player.experience
        self.life_bar.current_value = self.player.current_health
        self.life_bar.right_value = self.player.max_health
        self.energy_bar.right_value = self.player.dash_cooldown

        if self.player.dash_timer:
            self.energy_bar.current_value = self.player.dash_timer.time

        if self.player.level_up:
            self.level_up(self.player.calculate_xp(self.player.level),
                          self.player.calculate_xp(self.player.level + 1),
                          self.player.experience)

        self.life_bar.update()
        self.energy_bar.update()
        self.exp_bar.update()
        self.screen.blit(self.surface, (0, 0))

    def level_up(self, left_val, right_val, current_val):
        del self.surface
        self.surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        self.exp_bar = Bar(
            **self.exp_bar_data,
            surface=self.surface,
            left_value=left_val,
            right_value=right_val,
            current_value=current_val
        )


class Bar:
    def __init__(
            self,
            surface,
            width,
            height,
            left_value=0,
            right_value=100,
            current_value=0,
            position=(50, 100),
            color='blue'
    ):
        self.width = width
        self.height = height
        self.left_value = left_value
        self.right_value = right_value
        self.current_value = current_value
        self.position = position
        self.surface = surface
        self.color = color

    def update(self):
        # Outer rectangle
        pygame.draw.rect(self.surface, 'grey', (*self.position, self.width, self.height), 1)

        # Inner rectangle
        distance_left_to_right = self.right_value - self.left_value
        adjusted_current_value = self.current_value - self.left_value
        width = self.width * adjusted_current_value / distance_left_to_right
        pygame.draw.rect(self.surface, self.color,
                         (self.position[0] + 1, self.position[1] + 1, width - 2, self.height - 2))

