from os import path
from abc import ABC, abstractmethod
from copy import copy

import pygame

from pyvivor.utils import (
    configurator, SHIPS_PATH,
    update_velocity,
    camera_background,
    PLAYER_BASE_SPEED,
    game_status,
    calculate_angle_between_points,
    FPS
)
from .base_attack import BaseAttack


SHIP_FILENAME = 'ship5.png'
SPRITE_SCALE = (128, 128)


class AbstractPlayer(ABC):
    def __init__(self):
        self.current_health = 3
        self.max_health = 3
        self.movement_speed = PLAYER_BASE_SPEED
        self.radius = SPRITE_SCALE[0] // 2
        self.attack = BaseAttack()

        self.gold_rate = 1
        self.gold = 1

        self.experience_rate = 1
        self.level_up = False
        self.level_constant = 100
        self.level = 1
        self.experience = 0

        self.can_dash = True
        self.dash_cooldown = FPS * 3
        self.dash_duration = 15
        self.dash_start = 0
        self.dashing = False
        self.dash_force = 8
        self.dash_animation_positions = []
        self.dash_immune_damage = False
        self.animation_offset = (0, 0)

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @property
    def is_immune_damage(self):
        return self.dashing and self.dash_immune_damage

    @property
    def experience(self):
        return self.__experience

    @experience.setter
    def experience(self, value):
        self.__experience = value
        if self.experience >= self.calculate_xp(self.level + 1) and value > 1:
            self.level_up = True
            self.level += 1

    def calculate_xp(self, level):
        if level <= 1:
            return 0
        return level * (level - 1) * self.level_constant // 2

    def dash(self):
        user_input = pygame.key.get_pressed()
        if self.dash_start > 0:
            self.dash_start += 1

        if (self.can_dash and user_input[pygame.K_LSHIFT] and
                (user_input[pygame.K_z] or user_input[pygame.K_s] or user_input[pygame.K_q] or user_input[pygame.K_d])):
            self.can_dash = False
            self.dashing = True
            self.movement_speed += self.dash_force
            update_velocity(self.dash_force)
            self.dash_start = 1
            self.animation_offset = (camera_background.offset_x, -camera_background.offset_y)

        if self.dash_start == self.dash_duration:
            self.movement_speed -= self.dash_force
            update_velocity(-self.dash_force)
            self.dashing = False
            self.dash_animation_positions = []

        if self.dash_start == self.dash_cooldown:
            self.dash_start = 0
            self.can_dash = True


class Player(AbstractPlayer):
    def __init__(self, groups):
        super().__init__()
        self.player_sprite = PlayerSprite(groups=groups)
        self.corrected_position = self.player_sprite.player_surface.get_rect().move(
            camera_background.offset_x,
            camera_background.offset_y
        )
        center = configurator.screen_width // 2, configurator.screen_height // 2
        size = self.player_sprite.image.get_size()
        self.rect = pygame.Rect(center, size)

    def update(self):
        self.attack.shoot(self.player_sprite.rotation_point, self.player_sprite.last_angle)

        if not game_status.paused and not game_status.levelling_up:
            self.dash()

            if self.dashing:
                self.dash_animation_positions.append((
                    configurator.screen_width // 2 + self.animation_offset[0] - camera_background.offset_x,
                    configurator.screen_height // 2 + self.animation_offset[1] + camera_background.offset_y
                ))

        color = (60, 179, 113)
        draw_surface = pygame.Surface((configurator.screen_width, configurator.screen_height), pygame.SRCALPHA)

        animations = copy(self.dash_animation_positions)
        animations.reverse()
        for a, animation_position in enumerate(animations):
            alpha = 150//self.dash_duration * (a + 1)
            pygame.draw.circle(draw_surface, (*color, alpha), animation_position, self.radius // 2, 0)

        configurator.game_screen.blit(draw_surface, (0, 0))
        self.player_sprite.update((self.rect.x, self.rect.y))


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.display_surface = configurator.game_screen
        img = pygame.image.load(path.join(SHIPS_PATH, SHIP_FILENAME)).convert_alpha()
        self.image = pygame.transform.scale(img, SPRITE_SCALE)
        self.x = configurator.screen_width // 2 - self.image.get_width() // 2
        self.y = configurator.screen_height // 2 - self.image.get_height() // 2
        self.player_surface = pygame.Surface(
            (self.image.get_width(), self.image.get_height()), pygame.SRCALPHA
        ).convert_alpha()
        self.last_angle = 0
        self.rotation_point = None

    def update(self, player_position):
        surface = self.player_surface

        if game_status.paused or game_status.levelling_up:
            self.player_surface.blit(self.image, (0, 0))
            surface, rotated_rect = self.rotate_surface(self.player_surface, self.last_angle)
            self.display_surface.blit(surface, rotated_rect)
            return

        rotated_rect = surface.get_rect(center=self.player_surface.get_rect().center)
        mouse_pos = pygame.mouse.get_pos()
        circle_center = configurator.screen_width // 2, configurator.screen_height // 2
        rotation_point = configurator.screen_width // 2, configurator.screen_height // 2 + 9
        angle = calculate_angle_between_points(circle_center, rotation_point, mouse_pos)
        if angle is not None:
            self.last_angle = angle
            surface, rotated_rect = self.rotate_surface(self.player_surface, angle)

        self.rotation_point = (configurator.screen_width // 2,
                               configurator.screen_height // 2 - rotated_rect.height // 2)

        self.player_surface.blit(self.image, (0, 0))
        self.display_surface.blit(surface, rotated_rect)

    @staticmethod
    def rotate_surface(surface, angle):
        """Rotate a surface while keeping its center and size"""
        rotated_surface = pygame.transform.rotozoom(surface, angle, 1)
        rotated_rect = rotated_surface.get_rect(center=surface.get_rect().center)
        rotated_rect.center = configurator.screen_width // 2, configurator.screen_height // 2 + 9
        return rotated_surface, rotated_rect
