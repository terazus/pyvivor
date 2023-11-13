from os import path

import pygame

from pyvivor.utils import (
    PARTICLES_PATH,
    configurator,
    collide,
    calculate_movement_vector,
    camera_background,
    game_status,
    Timer,
    FONT_PATH
)

animations_path = path.join(PARTICLES_PATH, 'smoke_orange')


class Enemy(pygame.sprite.Sprite):
    def __init__(
            self,
            groups, start_pos,
            speed=1, size=10, color='red', exp=20, gold=1, life=12, damage=10
    ):
        super().__init__(groups)

        self.display_surface = configurator.game_screen
        self.end_x = configurator.game_screen.get_width() // 2
        self.end_y = configurator.game_screen.get_height() // 2
        self.current_x = start_pos[0]
        self.current_y = start_pos[1]

        self.width = size
        self.speed = speed

        self.color = color
        self.exp_value = exp
        self.gold_value = gold
        self.life = life

        self.hit_animation_start = 0
        self.hit_animation_current = 0
        self.hit_animation_duration = 500

        self.player_moved = False
        self.damage = damage
        self.can_attack = True
        self.attack_cooldown = 500
        self.attack_timer = None

        self.damage_shown_timers = []
        self.damage_shown_duration = 800
        self.damage_taken_font = pygame.font.Font(FONT_PATH, 15)
        self.damage_taken_crit = pygame.font.Font(FONT_PATH, 25)

        self.collided_with = []
        self.damage_animations = pygame.sprite.Group()

        self.is_on_screen = True

    def update(self):
        if self.attack_timer:
            self.attack_timer.update()
            if self.attack_timer.time >= self.attack_cooldown:
                self.can_attack = True
                self.attack_timer = None

        hit_animation = self.hit_animation_current - self.hit_animation_start

        if 0 <= self.current_x <= configurator.screen_width and 0 <= self.current_y <= configurator.screen_height:
            self.is_on_screen = True
            if (hit_animation <= 0
                    or 50 <= hit_animation <= 100
                    or 150 <= hit_animation <= 200
                    or 250 <= hit_animation <= 300
                    or 350 <= hit_animation <= 400
                    or 450 <= hit_animation <= 500):
                pygame.draw.circle(self.display_surface, self.color, (self.current_x, self.current_y), self.width, 0)
            pygame.draw.circle(self.display_surface, 'white', (self.current_x - 1, self.current_y - 1),
                               self.width + 1, 2)
        else:
            self.is_on_screen = False

        if self.hit_animation_start != 0:
            self.hit_animation_current = pygame.time.get_ticks() + 1

        if hit_animation >= self.hit_animation_duration:
            self.hit_animation_current = 0
            self.hit_animation_start = 0

        if not game_status.paused and not game_status.levelling_up and not game_status.game_over:
            self.move()
            self.player_moved = False

        self.damage_animations.update()

    def update_player_position(self, direction):
        self.player_moved = direction

    def move(self):
        movement_vector = calculate_movement_vector(
            (self.current_x, self.current_y),
            (self.end_x, self.end_y),
            self.speed)
        if movement_vector:
            self.current_x += movement_vector[0]
            self.current_y += movement_vector[1]

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
            self.current_x += move_x
            self.current_y += move_y

    def collides_with(self, target):
        return collide(
            source={
                'x': self.current_x,
                'y': self.current_y,
                'radius': self.width // 2
            },
            target={
                'x': target.current_position[0],
                'y': target.current_position[1],
                'radius': target.width if hasattr(target, 'width') else target.radius
            }
        )

    def is_hit(self, damage, is_crit, bullet):
        if bullet not in self.collided_with:
            DamageTakenAnimation([self.damage_animations], self, damage, is_crit)
            self.collided_with.append(bullet)
            self.damage_shown_timers.append((Timer(), damage, is_crit))
            self.life -= damage
            if self.hit_animation_start == 0:
                self.hit_animation_start = pygame.time.get_ticks()

    def attack(self):
        self.attack_timer = Timer()
        self.can_attack = False


class DestroyAnimation(pygame.sprite.Sprite):
    def __init__(self, groups, enemy_position, unit_size=64):
        super().__init__(groups)
        self.screen = configurator.game_screen
        self.frame = 0
        self.alpha = 255
        self.done = False
        self.position = enemy_position[0] - unit_size // 2, enemy_position[1] - unit_size // 2
        self.images = [
            pygame.transform.scale(pygame.image.load(path.join(animations_path, f'{i}.png')).convert_alpha(),
                                   (unit_size, unit_size))
            for i in range(1, 6)
        ]
        self.image = self.images[0]

    def update(self):
        width, height = self.image.get_size()
        transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        transparent_surface.set_alpha(self.alpha)
        transparent_surface.blit(self.image, (0, 0))
        self.screen.blit(transparent_surface, self.position)

        if not self.done and not game_status.paused and not game_status.levelling_up:
            self.frame += 1
            self.update_image()

    def update_image(self):
        if self.frame % 5 == 0:
            del self.images[0]
            if len(self.images) == 0:
                self.done = True
            else:
                self.image = self.images[0]


class DamageTakenAnimation(pygame.sprite.Sprite):
    def __init__(self, groups, enemy, damage, is_crit):
        super().__init__(groups)
        self.display_surface = configurator.game_screen
        self.enemy = enemy
        self.damage = damage
        self.is_crit = is_crit
        self.timer = Timer()
        self.damage_shown_duration = 800
        self.damage_taken_font = pygame.font.Font(FONT_PATH, 15)
        self.damage_taken_crit = pygame.font.Font(FONT_PATH, 25)
        self.position = (self.enemy.current_x, self.enemy.current_y)
        self.done = False

    def update(self):
        if self.timer.time >= self.damage_shown_duration:
            self.done = True

        if not self.done:
            self.timer.update()
            color = 'white' if not self.is_crit else 'yellow'
            text = self.damage_taken_font.render(str(self.damage), True, color)
            if self.is_crit:
                text = self.damage_taken_crit.render(str(self.damage), True, color)

            offset = self.timer.time // 40
            x, y = (self.position[0] - text.get_width() // 2 - offset,
                    self.position[1] - text.get_height() - offset)
            if self.enemy:
                x = self.enemy.current_x - text.get_width() // 2 - offset
                y = self.enemy.current_y - self.enemy.width - text.get_height() - offset
                self.position = (x, y)
            self.display_surface.blit(text, (x, y))

    def update_player_position(self, direction):
        if direction:
            move_x = 0
            move_y = 0
            if 'w' in direction:
                move_x = camera_background.cam_speed
            elif 'e' in direction:
                move_x = -camera_background.cam_speed
            if 'n' in direction:
                move_y = camera_background.cam_speed
            elif 's' in direction:
                move_y = -camera_background.cam_speed
            if move_x and move_y:
                move_x *= 0.7071
                move_y *= 0.7071
            self.position = (self.position[0] + move_x, self.position[1] + move_y)

