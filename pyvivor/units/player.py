from os import path
from abc import ABC, abstractmethod
from copy import copy

import pygame

from pyvivor.utils import (
    configurator, SHIPS_PATH,
    update_velocity,
    camera_background,
    game_status,
    calculate_angle_between_points,
    Timer,
    FPS
)
from .defaults import (
    PLAYER_BASE_SPEED,
    PLAYER_BASE_LIFE,
    PLAYER_BASE_DASH_COOLDOWN,
    PLAYER_BASE_LIFE_REGEN,
    PLAYER_BASE_PICKUP_RANGE,
    PLAYER_BASE_EXP_RATE,
    PLAYER_BASE_GOLD_RATE,
    PLAYER_BASE_DASH_FORCE,
    PLAYER_BASE_ARMOUR
)
from pyvivor.units.attacks import BaseAttack, ClawAttack

SHIP_PATH = path.join('Main Ship - Bases', 'PNGs')
BASE_NAME = 'Main Ship - Base -'
SHIP_FULL_LIFE = path.join(SHIP_PATH, f'{BASE_NAME} Full health.png')
SHIP_SLIGHTLY_DAMAGED = path.join(SHIP_PATH, f'{BASE_NAME} Slight damage.png')
SHIP_DAMAGED = path.join(SHIP_PATH, f'{BASE_NAME} Damaged.png')
SHIP_VERY_DAMAGED = path.join(SHIP_PATH, f'{BASE_NAME} Very damaged.png')
SPRITE_SCALE = (80, 80)


class AbstractPlayer(ABC):
    def __init__(self):

        self.current_health = PLAYER_BASE_LIFE
        self.max_health = PLAYER_BASE_LIFE
        self.armour = PLAYER_BASE_ARMOUR
        self.life_regen = PLAYER_BASE_LIFE_REGEN
        self.pickup_range = PLAYER_BASE_PICKUP_RANGE
        self.movement_speed = PLAYER_BASE_SPEED
        self.gold_rate = PLAYER_BASE_GOLD_RATE
        self.experience_rate = PLAYER_BASE_EXP_RATE
        self.dash_force = PLAYER_BASE_DASH_FORCE
        self.dash_cooldown = PLAYER_BASE_DASH_COOLDOWN

        self.life_regen_timer = Timer()
        self.radius = SPRITE_SCALE[0] // 2
        self.attack = BaseAttack()

        self.gold = 0
        self.level_up = False
        self.level_constant = 100
        self.level = 1
        self.experience = 0
        self.can_dash = False
        self.dashing = False
        self.dash_animation_positions = []
        self.dash_immune_damage = False
        self.animation_offset = (0, 0)
        self.dash_timer = None
        self.dash_duration = 166

        self.current_position = (configurator.screen_width // 2, configurator.screen_height // 2)

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

    @property
    def movement_speed(self):
        return self.__movement_speed

    @movement_speed.setter
    def movement_speed(self, value):
        self.__movement_speed = value
        update_velocity(value)

    def calculate_xp(self, level):
        return 0 if level <= 1 else level * (level - 1) * self.level_constant // 2

    def dash(self):
        user_input = pygame.key.get_pressed()
        if self.dash_timer:
            self.dash_timer.update()

        if (self.can_dash and user_input[pygame.K_LSHIFT] and
                (user_input[pygame.K_z] or user_input[pygame.K_s] or user_input[pygame.K_q] or user_input[pygame.K_d])):
            self.can_dash = False
            self.dashing = True
            self.movement_speed += self.dash_force
            update_velocity(self.movement_speed)
            self.dash_timer = Timer()
            self.animation_offset = (-camera_background.offset_x, -camera_background.offset_y)

        if self.dash_timer and self.dash_timer.time >= self.dash_duration and self.dashing:
            self.movement_speed -= self.dash_force
            update_velocity(self.movement_speed)
            self.dashing = False
            self.dash_animation_positions = []

        if self.dash_timer and self.dash_timer.time >= self.dash_cooldown:
            self.dash_timer = None
            self.can_dash = True

    def is_hit(self, damage):
        if not self.is_immune_damage:
            reduction = (self.armour * damage / 100) // 5 if self.armour < 400 else 80 * damage / 100
            self.current_health -= damage - reduction
            if self.current_health <= 0:
                game_status.game_over = True

    def regenerate_life(self):
        if self.life_regen > 0:
            self.life_regen_timer.update()
            if self.life_regen_timer.time >= 1000:
                self.life_regen_timer.reset()
                self.current_health += self.life_regen
                if self.current_health > self.max_health:
                    self.current_health = self.max_health

    def __iter__(self):
        data = {
            "general": {
                "level": self.level,
                "experience": self.experience,
                "next level": self.calculate_xp(self.level + 1),
                "gold": self.gold
            },
            "defences": {
                "health": self.current_health,
                "max health": self.max_health,
                "armour": self.armour,
                "life regen": self.life_regen,
            },
            "attack": dict(self.attack),
            "movement": {
                "speed": {
                    "value": self.movement_speed * FPS,
                    "unit": "px/s"
                }
            },
            "miscellaneous": {
                "pickup range": {
                    "value": self.pickup_range,
                    "unit": "px"
                },
                "gold rate": {
                    "value": self.gold_rate,
                    "unit": "x"
                },
                "experience rate": {
                    "value": self.experience_rate,
                    "unit": "x"
                },
            }
        }
        if self.can_dash:
            data['movement']['dash cooldown'] = {
                "value": self.dash_cooldown / 1000,
                "unit": "s"
            }
        yield from data.items()


class Player(AbstractPlayer):
    def __init__(self, groups, shop):
        super().__init__()
        self.player_sprite = PlayerSprite(groups=groups)
        self.corrected_position = self.player_sprite.player_surface.get_rect().move(
            camera_background.offset_x,
            camera_background.offset_y
        )
        center = configurator.screen_width // 2, configurator.screen_height // 2
        self.rect = pygame.Rect(center, self.player_sprite.image.get_size())
        self.equip_items(dict(shop))

    def update(self):
        self.attack.shoot(self.player_sprite.rotation_point, self.player_sprite.last_angle)
        self.player_sprite.update_image(self.current_health / self.max_health)
        self.regenerate_life()

        if not game_status.paused and not game_status.levelling_up and not game_status.game_over:
            self.dash()

            if self.dashing:
                self.dash_animation_positions.append((
                    configurator.screen_width // 2 + self.animation_offset[0] + camera_background.offset_x,
                    configurator.screen_height // 2 + self.animation_offset[1] + camera_background.offset_y
                ))

        color = (60, 179, 113)
        draw_surface = pygame.Surface((configurator.screen_width, configurator.screen_height), pygame.SRCALPHA)

        animations = copy(self.dash_animation_positions)
        animations.reverse()
        for a, animation_position in enumerate(animations):
            alpha = 255//len(animations) * (a + 1)
            pygame.draw.circle(draw_surface, (*color, alpha), animation_position, self.radius // 4, 0)

        configurator.game_screen.blit(draw_surface, (0, 0))
        self.player_sprite.update((self.rect.x, self.rect.y))

    def equip_items(self, items):
        for section, item in items.items():
            if item:
                item.apply(self)


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.display_surface = configurator.game_screen

        full_life_image = pygame.image.load(path.join(SHIPS_PATH, SHIP_FULL_LIFE)).convert_alpha()
        slightly_damaged_image = pygame.image.load(path.join(SHIPS_PATH, SHIP_SLIGHTLY_DAMAGED)).convert_alpha()
        damaged_image = pygame.image.load(path.join(SHIPS_PATH, SHIP_DAMAGED)).convert_alpha()
        very_damaged_image = pygame.image.load(path.join(SHIPS_PATH, SHIP_VERY_DAMAGED)).convert_alpha()

        self.images = {
            'full_life': pygame.transform.scale(full_life_image, SPRITE_SCALE),
            'slightly_damaged': pygame.transform.scale(slightly_damaged_image, SPRITE_SCALE),
            'damaged': pygame.transform.scale(damaged_image, SPRITE_SCALE),
            'very_damaged': pygame.transform.scale(very_damaged_image, SPRITE_SCALE)
        }
        self.image = self.images['full_life']

        self.x = configurator.screen_width // 2 - self.image.get_width() // 2
        self.y = configurator.screen_height // 2 - self.image.get_height() // 2

        img_size = (self.image.get_width(), self.image.get_height())
        self.player_surface = pygame.Surface(img_size, pygame.SRCALPHA).convert_alpha()
        self.last_angle = 0
        self.rotation_point = None

    def update(self, player_position):
        surface = self.player_surface
        if game_status.paused or game_status.levelling_up or game_status.game_over:
            self.player_surface.blit(self.image, (0, 0))
            surface, rotated_rect = self.rotate_surface(self.player_surface, self.last_angle)
            self.display_surface.blit(surface, rotated_rect)
            return

        rotated_rect = surface.get_rect(center=self.player_surface.get_rect().center)
        mouse_pos = pygame.mouse.get_pos()
        circle_center = configurator.screen_width // 2, configurator.screen_height // 2
        rotation_point = configurator.screen_width // 2, configurator.screen_height // 2 + 2
        angle = calculate_angle_between_points(circle_center, rotation_point, mouse_pos)
        if angle is not None:
            self.last_angle = angle
            surface, rotated_rect = self.rotate_surface(self.player_surface, angle)

        self.rotation_point = (configurator.screen_width // 2,
                               configurator.screen_height // 2 - rotated_rect.height // 2)

        self.player_surface.blit(self.image, (0, 0))
        self.display_surface.blit(surface, rotated_rect)

    def update_image(self, value):
        if value == 1:
            self.image = self.images['full_life']
        if value < 1:
            self.image = self.images['slightly_damaged']
        if value < 0.66:
            self.image = self.images['damaged']
        if value < 0.33:
            self.image = self.images['very_damaged']

    @staticmethod
    def rotate_surface(surface, angle):
        """Rotate a surface while keeping its center and size"""
        rotated_surface = pygame.transform.rotozoom(surface, angle, 1)
        rotated_rect = rotated_surface.get_rect(center=surface.get_rect().center)
        rotated_rect.center = configurator.screen_width // 2, configurator.screen_height // 2
        return rotated_surface, rotated_rect


