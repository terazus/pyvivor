from os import path

import pygame

# General settings
GAME_TITLE = 'Pyvivor'
FPS = 120


# Resources
HERE_PATH = path.dirname(__file__)
ASSETS_PATH = path.join(HERE_PATH, '..', 'assets')
MAPS_PATH = path.join(ASSETS_PATH, 'maps')
SOUNDS_PATH = path.join(ASSETS_PATH, 'sounds')
GRAPHICS_PATH = path.join(ASSETS_PATH, 'graphics')
BUTTONS_PATH = path.join(GRAPHICS_PATH, 'buttons')
TEXTURES_PATH = path.join(GRAPHICS_PATH, 'textures')
SHIPS_PATH = path.join(GRAPHICS_PATH, 'ship')
PARTICLES_PATH = path.join(GRAPHICS_PATH, 'particles')
GEMS_PATH = path.join(GRAPHICS_PATH, 'gems')
FONT_PATH = path.join(GRAPHICS_PATH, 'font', 'joystix.ttf')


class Configurator:
    def __init__(self, velocity=0.5):
        self.game_screen = pygame.display.set_mode((1920, 1080), vsync=1)
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.screen_rectangle = pygame.Rect((0, 0), (self.screen_width, self.screen_height))

        self.min_screen_width = 1920
        self.min_screen_height = 1080

        self.offset_x = 0
        self.offset_y = 0
        self.cam_speed = velocity

    def change_screen_size(self, width, height):
        new_width = width if width >= self.min_screen_width else self.min_screen_width
        new_height = height if height >= self.min_screen_height else self.min_screen_height
        self.game_screen = pygame.display.set_mode((new_width, new_height))
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()


configurator = Configurator()
