import sys

import pygame

from .cameras import CameraHandler, camera_background, camera_foreground_slow, camera_foreground_normal, update_velocity
from .status import game_status
from .defaults import PLAYER_BASE_SPEED
from .settings import (
    GAME_TITLE,
    FPS,
    ASSETS_PATH,
    MAPS_PATH,
    GRAPHICS_PATH,
    BUTTONS_PATH,
    TEXTURES_PATH,
    SHIPS_PATH,
    FONT_PATH,
    PARTICLES_PATH,
    configurator
)
from .timer import Timer
from .math import (
    calculate_angle_between_points,
    collide,
    distance,
    rotate_point_around_point,
    interpolate_close_point,
    calculate_movement_vector
)


def leave_game():
    pygame.quit()
    sys.exit()
