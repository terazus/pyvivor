from random import randrange

from .enemy import Enemy, DestroyAnimation
from .experience_gem import ExperienceGem
from pyvivor.utils import distance, configurator


class EnemyFactory:

    def __init__(self, groups, player_position=(0, 0), enemy_distance=300,):
        self.groups = groups
        self.player_position = player_position
        self.enemy_distance = enemy_distance

        self.prototypes = {
            "default": {
                "apply": self.generate_default_enemy,
                "arguments": {
                    "life": 12,
                    "exp": 20,
                },
                "quantity": 1
            },
            "boss": {
                "apply": self.generate_boss,
                "arguments": {
                    "speed": 1.2,
                    "size": 20,
                    "color": "blue",
                    "exp": 100,
                    "gold": 20,
                    "life": 100,
                    "damage": 30,
                },
                "quantity": 1
            },
        }

        self.timeline_index = 0
        self.timeline_breakpoint = 1
        self.timeline_duration = 60 * 30
        number_of_breakpoints = int(self.timeline_duration / self.timeline_breakpoint)
        self.timeline_done = [False for _ in range(0, number_of_breakpoints)]

    def generate_random_positions(self):
        enemy_x = randrange(0, configurator.screen_width)
        enemy_y = randrange(0, configurator.screen_height)
        distance_enemy_player = distance(enemy_x, enemy_y, self.player_position[0], self.player_position[1])
        if distance_enemy_player > self.enemy_distance:
            return enemy_x, enemy_y
        return self.generate_random_positions()

    def generate_default_enemy(self):
        enemy_position = self.generate_random_positions()
        return Enemy(groups=self.groups, start_pos=enemy_position,
                     **self.prototypes['default']['arguments'])

    def generate_boss(self):
        enemy_position = self.generate_random_positions()
        return Enemy(groups=self.groups, start_pos=enemy_position,
                     **self.prototypes['boss']['arguments'])

    def generate_enemies(self, quantity=5, enemy_type='default'):
        enemies = []
        for _ in range(quantity):
            if enemy_type in self.prototypes:
                enemy_unit = self.prototypes[enemy_type]
                enemies.append(enemy_unit['apply']())
        return enemies

    def timeline(self, timer):
        """ Function for repeating events

        :param timer: int or float
        """
        seconds = timer / 1000
        done = self.timeline_done[self.timeline_index]
        extra_enemies = []
        if seconds > self.timeline_breakpoint and not done:
            self.timeline_done[self.timeline_index] = True
            self.timeline_index += 1
            self.timeline_breakpoint += 1

            # every 30 seconds
            if self.timeline_index % 30 == 0:
                self.prototypes['default']['arguments']['life'] += 2
                self.prototypes['default']['arguments']['exp'] += 15

            # every 15 seconds
            if self.timeline_index % 15 == 0:
                enemies = self.generate_enemies(quantity=self.prototypes['boss']['quantity'], enemy_type='boss')
                extra_enemies = [*extra_enemies, *enemies]
                self.prototypes['boss']['arguments']['life'] += 10
                self.prototypes['boss']['arguments']['exp'] += 5

            # every 1:30 min
            if self.timeline_index % 90 == 0:
                if self.prototypes['boss']['arguments']['speed'] < 2:
                    self.prototypes['boss']['arguments']['speed'] += 0.1
                self.prototypes['boss']['quantity'] += 1 if self.prototypes['boss']['quantity'] < 5 else 0
                self.prototypes['default']['quantity'] += 2 if self.prototypes['default']['quantity'] < 20 else 0

            return [*self.generate_enemies(quantity=self.prototypes['default']['quantity']), *extra_enemies]
        return []
