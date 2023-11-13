import pygame

from .status import game_status


class CameraHandler:
    def __init__(self, velocity=2):
        self.offset_x = 0
        self.offset_y = 0
        self.cam_speed = velocity

    def change_screen_offset(self):
        if game_status.started and \
                (not game_status.shopping and not game_status.paused and not game_status.levelling_up
                 and not game_status.game_over):
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
                move_x += self.cam_speed
                moved += 'w'
            if pygame.key.get_pressed()[pygame.K_d]:
                move_x -= self.cam_speed
                moved += 'e'

            if 'w' in moved and 'e' in moved:
                moved = moved.replace('w', '')
                moved = moved.replace('e', '')
            if 'n' in moved and 's' in moved:
                moved = moved.replace('n', '')
                moved = moved.replace('s', '')

            # Normalize diagonal movement speed
            if move_x and move_y:
                move_x *= 0.7071
                move_y *= 0.7071

            self.offset_x += move_x
            self.offset_y += move_y
            return moved if moved else None
        return None


# Create new camera with different speed here
camera_background = CameraHandler()


def update_velocity(value):
    # Update your camera when the player movement speed changes. Try to keep the original ratio.
    camera_background.cam_speed = value
