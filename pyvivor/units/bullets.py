import pygame

from pyvivor.utils import configurator, calculate_movement_vector, game_status


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_position, end_position, width=5, speed=4, range_=300):
        super().__init__()
        self.display_surface = configurator.game_screen
        self.end_position = end_position
        self.current_position = start_position
        self.movement = calculate_movement_vector(start_position, end_position, speed)
        self.width = width
        self.speed = speed
        self.range = range_
        self.done = False

    def update(self):
        movement_vector = calculate_movement_vector(self.current_position, self.end_position, self.speed)
        if movement_vector:
            if not game_status.paused and not game_status.levelling_up:
                self.current_position = (self.current_position[0] + movement_vector[0],
                                         self.current_position[1] + movement_vector[1])
            pygame.draw.circle(self.display_surface, 'yellow', self.current_position, self.width, 0)
        else:
            self.done = True
