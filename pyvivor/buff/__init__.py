from random import choice

import pygame

from pyvivor.utils import FONT_PATH, configurator

class BuffManager:
    def __init__(self, player):
        self.player = player
        self.display_surface = configurator.game_screen
        self.buff = {
            "heal": {
                "apply": self.heal,
                "selected": 0,
                "max": 0,
            },
            "+100g": {
                "apply": self.increase_gold,
                "selected": 0,
                "max": 0
            },
            "max life": {
                "apply": self.increase_max_life,
                "selected": 0,
                "max": 3
            },
            "velocity": {
                "apply": self.increase_velocity,
                "selected": 0,
                "max": 10
            },
            "atk speed": {
                "apply": self.increase_attack_speed,
                "selected": 0,
                "max": 10
            },
            "proj. speed": {
                "apply": self.increase_projectile_speed,
                "selected": 0,
                "max": 10
            },
            "proj. width": {
                "apply": self.increase_projectile_width,
                "selected": 0,
                "max": 10

            },
            "range": {
                "apply": self.increase_range,
                "selected": 0,
                "max": 10
            },
            "damage": {
                "apply": self.increase_damage,
                "selected": 0,
                "max": 10
            },
            "better exp": {
                "apply": self.increase_exp_ratio,
                "selected": 0,
                "max": 10
            },
            "dash": {
                "apply": self.improve_dash,
                "selected": 0,
                "max": 10
            }
        }
        self.selected_buffs = []
        self.buff_rects = []
        self.font = pygame.font.Font(FONT_PATH, 16)

    # INFINITE BUFFS #
    def heal(self):
        if self.player.life < self.player.max_life:
            self.player.life += 1
            return True
        return True

    def increase_gold(self):
        self.player.gold += 100
        return True

    # LIMITED BUFFS #
    def increase_max_life(self):
        buff = self.buff['max life']
        if buff['selected'] < buff['max']:
            self.player.max_life += 1
            buff['selected'] += 1
            self.player.life += 1
            return True
        return False

    def increase_velocity(self):
        buff = self.buff['velocity']
        if buff['selected'] < buff['max']:
            self.player.movement_speed += 0.1
            buff['selected'] += 1
            return True
        return False

    def increase_attack_speed(self):
        buff = self.buff['atk speed']
        if buff['selected'] < buff['max']:
            self.player.attack.cooldown -= 2
            buff['selected'] += 1
            self.player.frame_count = 0
            return True
        return False

    def increase_projectile_speed(self):
        buff = self.buff['proj. speed']
        if buff['selected'] < buff['max']:
            self.player.attack.projectile_speed += 0.2
            buff['selected'] += 1
            return True
        return False

    def increase_damage(self):
        buff = self.buff['damage']
        if buff['selected'] < buff['max']:
            self.player.attack.damage += 2
            buff['selected'] += 1
            return True
        return False

    def increase_projectile_width(self):
        buff = self.buff['proj. width']
        if buff['selected'] < buff['max']:
            self.player.attack.projectile_width += 0.5
            buff['selected'] += 1
            return True
        return False

    def increase_range(self):
        buff = self.buff['range']
        if buff['selected'] < buff['max']:
            self.player.attack.range += 50
            buff['selected'] += 1
            return True
        return False

    def increase_exp_ratio(self):
        buff = self.buff['better exp']
        if buff['selected'] < buff['max']:
            self.player.experience_rate += 0.1
            buff['selected'] += 1
            return True
        return False

    def improve_dash(self):
        buff = self.buff['dash']
        if buff['selected'] < buff['max']:
            if not self.player.can_dash:
                self.player.can_dash = True
            else:
                self.player.dash_cooldown -= 10
                self.player.dash_force += 0.2
            buff['selected'] += 1
            return True
        return False

    # BUFF SELECTION #
    def select_buffs(self, quantity=3):
        while len(self.selected_buffs) < quantity:
            buff = choice(list(self.buff.keys()))
            can_select = self.buff[buff]['selected'] < self.buff[buff]['max'] or self.buff[buff]['max'] == 0
            if (buff not in self.selected_buffs and can_select) or len(self.buff) < quantity:
                self.selected_buffs.append(buff)
            if not can_select:
                del self.buff[buff]

        return self.selected_buffs

    def draw_buffs(self, rect):
        width = 250
        offset = 12
        height = 130
        pos_x = rect.x + offset
        pos_y = rect.y + rect.height / 2 - height / 2
        self.buff_rects = []

        for buff_name in self.selected_buffs:
            buff_value = self.buff[buff_name]
            stacks_text = f" {buff_value['selected']}/{buff_value['max']}" if buff_value['max'] != 0 else '\u221e'
            new_rect = pygame.Rect(pos_x, pos_y, width, height)
            self.buff_rects.append(new_rect)
            pygame.draw.rect(self.display_surface, 'white', new_rect, 0)
            text = self.font.render(buff_name, True, 'black')
            cost = self.font.render(f"{stacks_text}", True, 'black')
            self.display_surface.blit(text, (pos_x + width / 2 - text.get_width() / 2,
                                             pos_y + height / 2 - 20 - text.get_height() / 2))
            self.display_surface.blit(cost, (pos_x + width / 2 - cost.get_width() / 2,
                                             pos_y + height / 2 + 20 - cost.get_height() / 2))
            pos_x += width + offset
