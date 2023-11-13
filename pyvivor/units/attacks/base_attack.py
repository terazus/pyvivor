from random import randint
from os import path

import pygame

from pyvivor.utils import (
    configurator,
    rotate_point_around_point,
    interpolate_close_point,
    Timer,
    FPS,
    SOUNDS_PATH
)
from pyvivor.units.defaults import (
    ATTACK_BASE_COOLDOWN,
    ATTACK_BASE_PROJECTILE_SPEED,
    ATTACK_BASE_PROJECTILE_WIDTH,
    ATTACK_BASE_RANGE,
    ATTACK_BASE_DAMAGE,
    ATTACK_BASE_CRITICAL_CHANCE,
    ATTACK_BASE_CRITICAL_MULTIPLIER,
    ATTACK_BASE_PIERCE_COUNT,
)
from pyvivor.units.bullets import Bullet


# Move this to a sound loader
pygame.mixer.init()
LAZER_SOUND_FILE = path.join(SOUNDS_PATH, 'laser.mp3')
LAZER_SOUND = pygame.mixer.Sound(LAZER_SOUND_FILE)


class BaseAttack:

    def __init__(self):
        self.display_surface = configurator.game_screen
        self.player_center = configurator.screen_width // 2, configurator.screen_height // 2

        self.cooldown = ATTACK_BASE_COOLDOWN
        self.cooldown_multiplier = 1
        self.projectile_speed = ATTACK_BASE_PROJECTILE_SPEED
        self.projectile_width = ATTACK_BASE_PROJECTILE_WIDTH
        self.range = ATTACK_BASE_RANGE
        self.damage = ATTACK_BASE_DAMAGE
        self.damage_multiplier = 1
        self.projectiles = []
        self.critical_chance = ATTACK_BASE_CRITICAL_CHANCE
        self.critical_multiplier = ATTACK_BASE_CRITICAL_MULTIPLIER

        self.frame_count = 0
        self.timer = Timer()
        self.pierce_count = ATTACK_BASE_PIERCE_COUNT

    def get_cooldown(self):
        return self.cooldown * self.cooldown_multiplier

    def shoot(self, direction, angle):
        [self.projectiles.remove(bullet) if bullet.done else bullet.update() for bullet in self.projectiles]
        self.timer.update()
        if self.timer.time >= self.get_cooldown():
            shoot = rotate_point_around_point(self.player_center, direction, angle)
            source = {'x': configurator.screen_width // 2, 'y': configurator.screen_height // 2}
            target = {'x': shoot[0], 'y': shoot[1]}
            shoot_direction = interpolate_close_point(source, target, self.range)
            bullet = Bullet(
                start_position=shoot,
                end_position=shoot_direction,
                width=self.projectile_width,
                speed=self.projectile_speed,
                range_=self.range,
                pierce_count=self.pierce_count)
            self.projectiles.append(bullet)
            self.timer.reset()

            # play sound
            LAZER_SOUND.set_volume(0.01)
            LAZER_SOUND.play()

    def get_damage(self):
        base_dmg = self.damage * self.damage_multiplier
        crit_roll = randint(0, 100)
        if crit_roll <= self.critical_chance:
            return int(base_dmg * self.critical_multiplier), True
        return base_dmg, False

    def __iter__(self):
        yield from {
            "damage": {
                "value": self.damage,
                "unit": None
            },
            "cooldown": {
                "value": self.get_cooldown() / 1000,
                "unit": "s"
            },
            "proj. speed": {
                "value": self.projectile_speed * FPS,
                "unit": "px/s"
            },
            "proj. width": {
                "value": self.projectile_width,
                "unit": "px"
            },
            "range": {
                "value": self.range,
                "unit": "px"
            },
            "crit. chance": {
                "value": self.critical_chance,
                "unit": "%"
            },
            "crit. multiplier": {
                "value": self.critical_multiplier,
                "unit": "x"
            },
            "pierce": {
                "value": self.pierce_count,
                "unit": None
            }
        }.items()

    def update_player_position(self, direction):
        for bullet in self.projectiles:
            bullet.offset_movement(direction)