from os import path

import pygame

from pyvivor.utils import (
    configurator,
    GRAPHICS_PATH,
    camera_background
)

BACKGROUND_IMAGE = pygame.image.load(path.join(GRAPHICS_PATH, 'backgrounds', 'background.png')).convert_alpha()


class BackgroundScroller(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.moved = False
        self.screen = configurator.game_screen
        self.camera_handler = camera_background

        # This is manually done, maybe try to automate it.
        self.grid_width = 2
        self.grid_height = 2
        self.grid = []
        for i in range(-1, self.grid_width):
            line = []
            for j in range(-1, self.grid_height):
                line.append(BackgroundTile(j, i))
            self.grid.append(line)

        self.left = self.grid[0][0].grid_origin_position[0]
        self.top = self.grid[0][0].grid_origin_position[1]
        self.right = self.grid[-1][-1].grid_origin_position[0]
        self.bottom = self.grid[-1][-1].grid_origin_position[1]

    def update(self):
        self.moved = self.camera_handler.change_screen_offset()
        self.draw()

    def draw(self):
        for line in self.grid:
            for tile in line:
                tile.draw()
                if tile.visibility_changed and tile.visible:
                    self.__rebuild_graph(tile)

    def __rebuild_graph(self, tile):
        x = tile.grid_origin_position[0]
        y = tile.grid_origin_position[1]
        self.__rebuild_y_movement(x, y)
        self.__rebuild_x_movement(x)

    def __rebuild_y_movement(self, x, y):
        if y == self.top:
            self.grid.insert(0, [
                BackgroundTile(x - 2, y - 1),
                BackgroundTile(x - 1, y - 1),
                BackgroundTile(x, y - 1),
                BackgroundTile(x + 1, y - 1),
                BackgroundTile(x + 2, y - 1)
            ])
            if len(self.grid) >= 5:
                del self.grid[-1]
            self.top = self.grid[0][0].grid_origin_position[1]
            self.bottom = self.grid[-1][-1].grid_origin_position[1]

        if y == self.bottom:
            self.grid.append([
                BackgroundTile(x - 2, y + 1),
                BackgroundTile(x - 1, y + 1),
                BackgroundTile(x, y + 1),
                BackgroundTile(x + 1, y + 1),
                BackgroundTile(x + 2, y + 1)
            ])

            if len(self.grid) >= 5:
                del self.grid[0]

            self.top = self.grid[0][0].grid_origin_position[1]
            self.bottom = self.grid[-1][-1].grid_origin_position[1]

    def __rebuild_x_movement(self, x):
        if x == self.left:
            for line in self.grid:
                y = line[0].grid_origin_position[1]
                line.insert(0, BackgroundTile(x - 1, y))
                if len(line) >= 5:
                    del line[-1]
            self.left = self.grid[0][0].grid_origin_position[0]
            self.right = self.grid[-1][-1].grid_origin_position[0]

        if x == self.right:
            for line in self.grid:
                y = line[0].grid_origin_position[1]
                line.append(BackgroundTile(x + 1, y))
                if len(line) >= 5:
                    del line[0]
            self.left = self.grid[0][0].grid_origin_position[0]
            self.right = self.grid[-1][-1].grid_origin_position[0]


class BackgroundTile:
    def __init__(self, x, y):
        image_width = BACKGROUND_IMAGE.get_width() // 3
        image_height = BACKGROUND_IMAGE.get_height() // 3

        self.grid_origin_position = (x, y)

        image_position_x = 0
        if x % 4 == 0 or x == 1 or x == -1:
            image_position_x = image_width
        if x % 5 == 0 or x == 2 or x == -2:
            image_position_x = image_width * 2

        image_position_y = 0
        if y % 4 == 0 or y == 1 or y == -1:
            image_position_y = image_height
        if y % 5 == 0 or y == 2 or y == -2:
            image_position_y = image_height * 2

        self.image = BACKGROUND_IMAGE.subsurface((image_position_x, image_position_y, image_width, image_height))
        self.visible = True if x == y == 0 else False
        self.visibility_changed = False

    def draw(self):
        x = self.grid_origin_position[0] * configurator.game_screen.get_width() + camera_background.offset_x
        y = self.grid_origin_position[1] * configurator.game_screen.get_height() + camera_background.offset_y
        self.set_visibility(x, y)
        if self.visible:
            configurator.game_screen.blit(self.image, (x, y))

    def set_visibility(self, x, y):
        collision_rect = pygame.Rect(0, 0,
                                     configurator.game_screen.get_width(), configurator.game_screen.get_height())
        image_rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        visible = True if collision_rect.colliderect(image_rect) else False
        self.visibility_changed = True if visible is not self.visible else False
        self.visible = visible
