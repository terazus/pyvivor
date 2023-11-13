import pygame

from pyvivor.utils import configurator, calculate_movement_vector, game_status, camera_background


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_position, end_position, width=5, speed=4, range_=300, pierce_count=0):
        super().__init__()
        self.display_surface = configurator.game_screen
        self.end_position = end_position
        self.current_position = start_position
        self.movement = calculate_movement_vector(start_position, end_position, speed)
        self.width = width
        self.speed = speed
        self.range = range_
        self.done = False
        self.pierce_count = pierce_count
        self.distance_travelled = 0
        self.movement_vector = calculate_movement_vector(self.current_position, self.end_position, self.speed)

    def update(self):
        if self.movement_vector:
            if not game_status.paused and not game_status.levelling_up and not game_status.game_over:
                self.current_position = (self.current_position[0] + self.movement_vector[0],
                                         self.current_position[1] + self.movement_vector[1])
                self.distance_travelled += self.speed
            pygame.draw.circle(self.display_surface, 'yellow', self.current_position, self.width, 0)
        if self.distance_travelled >= self.range:
            self.done = True

    def offset_movement(self, direction):
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
        self.current_position = (self.current_position[0] + move_x, self.current_position[1] + move_y)

    def can_pierce(self):
        return False if self.pierce_count == 0 else True
