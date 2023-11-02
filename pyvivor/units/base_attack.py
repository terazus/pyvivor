from pyvivor.utils import configurator, rotate_point_around_point, interpolate_close_point, game_status
from .bullets import Bullet


class BaseAttack:

    def __init__(self):
        self.display_surface = configurator.game_screen
        self.player_center = configurator.screen_width // 2, configurator.screen_height // 2

        self.cooldown = 60
        self.projectile_speed = 4
        self.projectile_width = 5
        self.range = 600
        self.pierce = False
        self.damage = 10
        self.auto_shoot = True
        self.projectiles = []

        self.frame_count = 0

    def shoot(self, direction, angle):
        [self.projectiles.remove(bullet) if bullet.done else bullet.update() for bullet in self.projectiles]

        if not game_status.paused and not game_status.levelling_up:
            self.frame_count += 1

            if self.frame_count == self.cooldown:
                shoot = rotate_point_around_point(self.player_center, direction, angle)
                source = {
                    'x': configurator.screen_width // 2,
                    'y': configurator.screen_height // 2
                }
                target = {
                    'x': shoot[0],
                    'y': shoot[1]
                }
                shoot_direction = interpolate_close_point(source, target, self.range)
                bullet = Bullet(shoot, shoot_direction, self.projectile_width, self.projectile_speed, self.range)
                self.projectiles.append(bullet)

            if self.frame_count > self.cooldown:
                self.frame_count = 0
