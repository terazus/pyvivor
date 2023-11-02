import datetime

import pygame

from pyvivor.utils import configurator, FONT_PATH


class GlobalTimer(pygame.sprite.Sprite):
    def __init__(self, world):
        super().__init__()
        self.start = pygame.time.get_ticks()
        self.screen = configurator.game_screen
        self.time = 0
        self.offset = 0
        self.pause_timer = 0
        self.playable_area = world
        self.font = pygame.font.Font(FONT_PATH, 18)
        self.total_offset = 0

    def update(self):
        text = self.font.render(f'Time: {str(datetime.timedelta(milliseconds=self.time)).split(".")[0]}', True, 'white')
        rect = self.playable_area
        top = rect.top + 10
        center_x = rect.centerx - text.get_width()/2
        self.screen.blit(text, (center_x, top))

    def get_timer(self):
        self.time = pygame.time.get_ticks() - self.start - self.total_offset

    def pause(self):
        self.pause_timer = pygame.time.get_ticks() - self.start

    def run_pause(self):
        self.offset = pygame.time.get_ticks() - self.start - self.pause_timer

    def unpause(self):
        self.total_offset += self.offset
