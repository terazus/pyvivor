from random import randrange
from os import path
from abc import ABCMeta, abstractmethod

import pygame

from pyvivor.utils import (
    configurator,
    GRAPHICS_PATH,
    camera_background,
    camera_foreground_slow,
    camera_foreground_normal
)


STAR_PATH = path.join(GRAPHICS_PATH, 'star.png')
FOG_PATH = path.join(GRAPHICS_PATH, 'particles', 'fog.png')
FOG2_PATH = path.join(GRAPHICS_PATH, 'particles', 'fog2.png')
FOG3_PATH = path.join(GRAPHICS_PATH, 'particles', 'fog3.png')

STAR = pygame.image.load(STAR_PATH).convert_alpha()
FOG_2_LARGE = pygame.transform.scale(pygame.image.load(FOG2_PATH).convert_alpha(), (400, 200))
FOG_3_LARGE = pygame.transform.scale(pygame.image.load(FOG3_PATH).convert_alpha(), (600, 150))


class Ground(pygame.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, groups):
        super().__init__(groups)
        self.display_surface = configurator.game_screen
        self.grid_width = 3
        self.grid_height = 3
        self.grid = [[[] for _ in range(self.grid_height)] for _ in range(self.grid_width)]
        self.positions = []
        self.camera_handler = camera_background
        self.moved = False

    @abstractmethod
    def draw(self):
        raise NotImplementedError

    def update(self):
        moved = self.camera_handler.change_screen_offset()
        if moved:
            self.camera(moved)
        self.draw()
        self.moved = moved

    @abstractmethod
    def generate_positions(self):
        raise NotImplementedError

    def camera(self, direction):
        if self.camera_handler.offset_x % configurator.screen_width == 0:
            for line in self.grid:
                if 'w' in direction:
                    tile = line.pop(2)
                    for star in tile:
                        star['x'] -= 3 * configurator.screen_width
                    line.insert(0, tile)
                elif 'e' in direction:
                    tile = line.pop(0)
                    for star in tile:
                        star['x'] += 3 * configurator.screen_width
                    line.append(tile)

        if self.camera_handler.offset_y % configurator.screen_height == 0:
            if 'n' in direction:
                line_ = self.grid.pop(2)
                for row in line_:
                    for star in row:
                        star['y'] -= 3 * configurator.screen_height
                self.grid.insert(0, line_)
            elif 's' in direction:
                line_ = self.grid.pop(0)
                for row in line_:
                    for star in row:
                        star['y'] += 3 * configurator.screen_height
                self.grid.append(line_)


class BackgroundStars(Ground):
    def __init__(self, groups):
        super().__init__(groups)
        self.stars_data = {
            'mini': {
                'scale': (4, 4),
                'image': pygame.transform.scale(STAR, (4, 4)),
                'quantity': 2000
            },
            'small': {
                'scale': (6, 6),
                'image': pygame.transform.scale(STAR, (6, 6)),
                'quantity': 250
            },
            'medium': {
                'scale': (12, 12),
                'image': pygame.transform.scale(STAR, (12, 12)),
                'quantity': 100
            },
            'large': {
                'scale': (22, 22),
                'image': pygame.transform.scale(STAR, (26, 26)),
                'quantity': 50
            }
        }
        self.generate_positions()

    def draw(self):
        for line in self.grid:
            for row in line:
                for star in row:
                    image = star['image']
                    star_x = star['x'] - self.camera_handler.offset_x
                    star_y = star['y'] + self.camera_handler.offset_y
                    if 0 <= star_x <= configurator.screen_width and 0 <= star_y <= configurator.screen_height:
                        self.display_surface.blit(image, (star_x, star_y))

    def generate_positions(self):
        for star_size in self.stars_data:
            quantity = self.stars_data[star_size]['quantity']
            for i in range(quantity):
                x = randrange(-configurator.screen_width, configurator.screen_width * 2)
                y = randrange(-configurator.screen_height, configurator.screen_height * 2)
                while (x, y) in self.positions:
                    x = randrange(0, configurator.screen_width)
                    y = randrange(0, configurator.screen_height)
                self.positions.append((x, y))

                grid_y = 0 if x < 0 else 1 if x < configurator.screen_width else 2
                grid_x = 0 if y < 0 else 1 if y < configurator.screen_height else 2
                self.grid[grid_x][grid_y].append({'x': x, 'y': y, 'image': self.stars_data[star_size]['image']})

        self.positions = []


class ForegroundFog(Ground):
    def __init__(self, groups, speed='slow'):
        super().__init__(groups)
        self.speed = speed
        fogs_per_tile = {
            'slow': 10,
            'normal': 3
        }
        self.fogs_per_tile = fogs_per_tile[speed]
        self.camera_handler = camera_foreground_normal if speed == 'normal' else camera_foreground_slow
        self.generate_positions()

    def generate_positions(self):
        for li, line in enumerate(self.grid):
            for r, row in enumerate(line):
                for i in range(self.fogs_per_tile):
                    x_min = 0 if r == 1 else -configurator.screen_width if r == 0 else configurator.screen_width
                    x_max = configurator.screen_width if r == 1 else 0 if r == 0 else configurator.screen_width * 2
                    x = randrange(x_min, x_max)
                    y_min = 0 if li == 1 else -configurator.screen_height if li == 0 else configurator.screen_height
                    y_max = configurator.screen_height if li == 1 else 0 if li == 0 else configurator.screen_height * 2
                    y = randrange(y_min, y_max)
                    while (x, y) in self.positions:
                        x = randrange(x_min, x_max)
                    self.positions.append((x, y))

                    grid_y = 0 if x < 0 else 1 if x < configurator.screen_width else 2
                    grid_x = 0 if y < 0 else 1 if y < configurator.screen_height else 2
                    self.grid[grid_x][grid_y].append({'x': x, 'y': y})

        self.positions = []

    def draw(self):
        for line in self.grid:
            for row in line:
                for fog in row:
                    fog_x = fog['x'] - self.camera_handler.offset_x
                    fog_y = fog['y'] + self.camera_handler.offset_y
                    if 0 <= fog_x <= configurator.screen_width and 0 <= fog_y <= configurator.screen_height:
                        alpha = 100
                        fog_image = FOG_2_LARGE
                        if self.speed == 'normal':
                            fog_image = FOG_3_LARGE
                            alpha = 150

                        img = fog_image.copy()
                        img.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                        self.display_surface.blit(img, (fog_x, fog_y))

