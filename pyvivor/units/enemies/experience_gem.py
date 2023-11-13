from os import path

import pygame

from pyvivor.utils import (
    configurator,
    game_status,
    camera_background,
    collide,
    calculate_movement_vector,
    GEMS_PATH
)

RED_GEM_PATH = path.join(GEMS_PATH, 'red.png')
GOLD_GEM_PATH = path.join(GEMS_PATH, 'yellow.png')
PURPLE_GEM_PATH = path.join(GEMS_PATH, 'purple.png')

RED_GEM = pygame.transform.scale(pygame.image.load(RED_GEM_PATH).convert_alpha(), (16, 16))
GOLD_GEM = pygame.transform.scale(pygame.image.load(GOLD_GEM_PATH).convert_alpha(), (16, 16))
PURPLE_GEM = pygame.transform.scale(pygame.image.load(PURPLE_GEM_PATH).convert_alpha(), (16, 16))


class ExperienceGem(pygame.sprite.Sprite):

    def __init__(self, groups, position, worth):
        super().__init__(groups)
        self.other_gems = groups[0]
        self.position = position
        self.surface = configurator.game_screen
        self.rectangle = None
        self.player_moved = False
        self.worth = worth
        self.final_destination = (configurator.screen_width // 2, configurator.screen_height // 2)

        self.move_to_player = False
        self.move_speed = 5

        self.caps = [1000, 10000]
        self.color = 'purple' if worth < self.caps[0] else 'gold' if worth < self.caps[1] else 'red'
        self.image = PURPLE_GEM if worth < self.caps[0] else GOLD_GEM if worth < self.caps[1] else RED_GEM
        self.can_merge = True if worth < self.caps[1] else False
        self.merge_range = 200
        self.merge_circle_position = (self.position[0] + self.merge_range // 2,
                                      self.position[1] + self.merge_range // 2)
        self.player_collision_range = 10
        self.merge_with_other_gems()

    def update_player_position(self, direction):
        self.player_moved = direction

    def update(self):
        self.rectangle = pygame.Rect(self.position[0], self.position[1], 10, 10)
        self.merge_circle_position = (self.position[0] + 5,
                                      self.position[1] + 5)

        if not game_status.paused and not game_status.levelling_up and not game_status.game_over:
            self.move()
            self.player_moved = False

        # Optimize this to check if the sprite is on the screen before rendering it
        self.surface.blit(self.image, self.position)

    def move(self):
        if self.move_to_player:
            x, y = self.position
            vector = calculate_movement_vector(self.position, self.final_destination, self.move_speed)
            if vector:
                self.position = (x + vector[0], y + vector[1])
            return

        if self.player_moved:
            move_x = 0
            move_y = 0
            if 'w' in self.player_moved:
                move_x = camera_background.cam_speed
            elif 'e' in self.player_moved:
                move_x = -camera_background.cam_speed
            if 'n' in self.player_moved:
                move_y = camera_background.cam_speed
            elif 's' in self.player_moved:
                move_y = -camera_background.cam_speed
            if move_x and move_y:
                move_x *= 0.7071
                move_y *= 0.7071
            x = self.position[0] + move_x
            y = self.position[1] + move_y
            self.position = (x, y)

    def merge_with_other_gems(self):
        if self.can_merge:
            total_worth = self.worth
            merging_gems = [self]
            source = {
                'x': self.merge_circle_position[0],
                'y': self.merge_circle_position[1],
                'radius': self.merge_range // 2
            }
            for gem in self.other_gems:
                if gem != self and gem.can_merge:
                    target = {
                        'x': gem.merge_circle_position[0],
                        'y': gem.merge_circle_position[1],
                        'radius': gem.merge_range // 2
                    }
                    if collide(source, target):
                        total_worth += gem.worth
                        merging_gems.append(gem)

            if total_worth > self.worth and len(merging_gems) > 50:
                self.worth = total_worth
                for remove_gem in merging_gems:
                    remove_gem.kill()
                    if remove_gem in self.other_gems:
                        self.other_gems.remove(remove_gem)
                pos = self.position
                groups = [self.other_gems]
                self.kill()
                ExperienceGem(groups, pos, total_worth)

    def collides_with(self, player_pickup_range):
        source = {
            "x": self.merge_circle_position[0],
            "y": self.merge_circle_position[1],
            "radius": self.player_collision_range // 2
        }
        target = {
            "x": configurator.screen_width // 2,
            "y": configurator.screen_height // 2,
            "radius": player_pickup_range
        }
        return collide(source, target)
