import sys

import pygame

from .cameras import CameraHandler, camera_background, update_velocity
from .status import game_status
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
    GEMS_PATH,
    SOUNDS_PATH,
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
from .saved_game import load_game_data, save_game_data


def leave_game():
    pygame.quit()
    sys.exit()
