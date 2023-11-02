from os import path

import pygame

from pyvivor.utils import (
    PARTICLES_PATH,
    configurator,
    collide,
    calculate_movement_vector,
    camera_background,
    game_status
)

animations_path = path.join(PARTICLES_PATH, 'smoke_orange')


class Enemy(pygame.sprite.Sprite):
    def __init__(
            self,
            groups, start_pos,
            speed=1, size=10, color='red', exp=20, gold=1, life=12
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

    def update(self):
        hit_animation = self.hit_animation_current - self.hit_animation_start
        # TODO: add a condition to only draw the enemies if they are in the screen boundaries
        if (hit_animation <= 0
                or 50 <= hit_animation <= 100
                or 150 <= hit_animation <= 200
                or 250 <= hit_animation <= 300
                or 350 <= hit_animation <= 400
                or 450 <= hit_animation <= 500):
            pygame.draw.circle(self.display_surface, self.color, (self.current_x, self.current_y), self.width, 0)
        pygame.draw.circle(self.display_surface, 'white', (self.current_x - 1, self.current_y - 1), self.width + 1, 2)

        if self.hit_animation_start != 0:
            self.hit_animation_current = pygame.time.get_ticks() + 1

        if hit_animation >= self.hit_animation_duration:
            self.hit_animation_current = 0
            self.hit_animation_start = 0

        if not game_status.paused and not game_status.levelling_up:
            self.move()
            self.player_moved = False

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
            if 'w' in self.player_moved:
                self.current_x += camera_background.cam_speed
            elif 'e' in self.player_moved:
                self.current_x -= camera_background.cam_speed
            if 'n' in self.player_moved:
                self.current_y += camera_background.cam_speed
            elif 's' in self.player_moved:
                self.current_y -= camera_background.cam_speed

    def collides_with(self, target):
        position = target.current_position
        source = {
            'x': position[0],
            'y': position[1],
            'radius': target.width if hasattr(target, 'width') else target.radius
        }
        target = {
            'x': self.current_x,
            'y': self.current_y,
            'radius': self.width if hasattr(target, 'width') else target.radius
        }
        return collide(source, target)

    def is_hit(self, damage):
        self.life -= damage
        if self.hit_animation_start == 0:
            self.hit_animation_start = pygame.time.get_ticks()


class DestroyAnimation(pygame.sprite.Sprite):
    def __init__(self, groups, enemy_position, unit_size=64):
        super().__init__(groups)
        self.screen = configurator.game_screen
        self.frame = 0
        self.alpha = 255
        self.done = False
        self.position = enemy_position[0] - unit_size//2, enemy_position[1] - unit_size//2
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