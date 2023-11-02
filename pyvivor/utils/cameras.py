import pygame

from .status import game_status
from .defaults import PLAYER_BASE_SPEED


class CameraHandler:
    def __init__(self, velocity=0.5):
        self.offset_x = 0
        self.offset_y = 0
        self.cam_speed = velocity

    def change_screen_offset(self):
        if game_status.started and \
                (not game_status.shopping and not game_status.paused and not game_status.levelling_up):
            moved = ''
            move_x = 0
            move_y = 0
            if pygame.key.get_pressed()[pygame.K_s]:
                move_y -= self.cam_speed
                moved += 's'
            if pygame.key.get_pressed()[pygame.K_z]:
                move_y += self.cam_speed
                moved += 'n'
            if pygame.key.get_pressed()[pygame.K_q]:
                move_x -= self.cam_speed
                moved += 'w'
            if pygame.key.get_pressed()[pygame.K_d]:
                move_x += self.cam_speed
                moved += 'e'
            self.offset_x += move_x
            self.offset_y += move_y
            return moved if moved else None
        return None


camera_background = CameraHandler(velocity=PLAYER_BASE_SPEED)
camera_foreground_slow = CameraHandler(velocity=3*PLAYER_BASE_SPEED/4)
camera_foreground_normal = CameraHandler(velocity=PLAYER_BASE_SPEED*4)


def update_velocity(value):
    camera_background.cam_speed = camera_background.cam_speed + value
    camera_foreground_slow.cam_speed = camera_foreground_slow.cam_speed + value
    camera_foreground_normal.cam_speed = camera_foreground_normal.cam_speed + value
