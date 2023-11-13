from shapely.geometry import Point, Polygon
import pygame

from pyvivor.utils import configurator, distance, FONT_PATH


GRID_WIDTH = 1400
GRID_HEIGHT = 900
DATA = {
    0: {
        'width': 824,
        'offset_x': 32,
        'offset_y': 10,
    },
    1: {
        'width': 867,
        'offset_x': 29,
        'offset_y': 22,
    },
    2: {
        'width': 917,
        'offset_x': 26,
        'offset_y': 46,
    },
    # 3: {
    #     'width': 977,
    #     'offset_x': 23,
    #     'offset_y': 82,
    # },
    4: {
        'width': 1046,
        'offset_x': 19,
        'offset_y': 130,
    },
    # 5: {
    #     'width': 1121,
    #     'offset_x': 15,
    #     'offset_y': 190,
    # },
    6: {
        'width': 1206,
        'offset_x': 11,
        'offset_y': 262,
    },
    7: {
        'width': 1299,
        'offset_x': 5,
        'offset_y': 346,
    },
    8: {
        'width': 1400,
        'offset_x': 0,
        'offset_y': 442,
    }
}


def generate_tiles():
    font = pygame.font.Font(FONT_PATH, 10)
    lines = [[] for _ in range(len(DATA))]
    mouse_pos = pygame.mouse.get_pos()

    mask = pygame.Surface((GRID_WIDTH + 1, GRID_HEIGHT + 1), pygame.SRCALPHA)

    l_ = []
    for line, line_data in DATA.items():
        offset_y = line_data['offset_y']
        offset_x = line_data['offset_x']
        top_distance = line_data['width']
        top_left = ((GRID_WIDTH - top_distance) // 2 - offset_x, (line * 50) + offset_y)
        top_right = (top_left[0] + top_distance, (line * 50) + offset_y)
        points_left_right = equidistant_points(top_left, top_right, 10)
        lines.append(points_left_right)

        if line == 0 or line == 8:
            l_.append((top_left, points_left_right[-2]))

    pos_x = configurator.screen_width // 2 - GRID_WIDTH // 2
    pos_y = configurator.screen_height // 2 - GRID_HEIGHT // 2
    for line_index in range(1, len(lines) - 1):
        for point_index in range(len(lines[line_index]) - 2):
            point_a = lines[line_index][point_index]
            point_b = lines[line_index][point_index + 1]
            point_c = lines[line_index + 1][point_index]
            point_d = lines[line_index + 1][point_index + 1]

            pygame.draw.polygon(mask, 'white', (point_a, point_b, point_d, point_c), 1)
            polygon = Polygon((point_a, point_b, point_d, point_c))
            polygon_center = list(polygon.centroid.coords)[0]

            mouse_corrected_pos = Point(mouse_pos[0] - pos_x, mouse_pos[1] - pos_y)
            if polygon.contains(mouse_corrected_pos):
                pygame.draw.polygon(mask, 'red', (point_a, point_b, point_d, point_c))

            text = f'({polygon_center[0]:.0f}, {polygon_center[1]:.0f})'
            render_text = font.render(text, True, 'white')
            text_pos = (
                polygon_center[0] - render_text.get_width() // 2,
                polygon_center[1] - render_text.get_height() // 2)
            mask.blit(render_text, text_pos)

            pygame.draw.circle(mask, 'red', point_a, 2, 0)
            pygame.draw.circle(mask, 'red', point_b, 2, 0)
            pygame.draw.circle(mask, 'red', point_c, 2, 0)
            pygame.draw.circle(mask, 'red', point_d, 2, 0)

    # draw_borders(l_, mask)
    configurator.game_screen.blit(mask, (pos_x, pos_y))


def draw_borders(l_, mask):
    line_0 = l_[0]
    last_line = l_[-1]
    pygame.draw.line(mask, 'yellow', line_0[0], last_line[0], 1)
    pygame.draw.line(mask, 'yellow', line_0[1], last_line[1], 1)


def equidistant_points(point_a, point_b, max_points):
    if max_points < 2:
        return []

    length = distance(*point_a, *point_b)
    distance_between_points = length / (max_points - 1)

    points = [point_a]
    current_point = point_a
    direction_vector = (point_b[0] - point_a[0], point_b[1] - point_a[1])
    step = distance_between_points / length

    while len(points) < max_points:
        x, y = current_point
        dx, dy = direction_vector
        new_point = (x + step * dx, y + step * dy)
        points.append(new_point)
        current_point = new_point
    return points


def point_coordinate(point_a, point_b, distance_):
    """ Return the coordinate of the point at distance_ from point_a in the direction of point_b """
    x_a, y_a = point_a
    x_b, y_b = point_b
    direction_vector = (x_b - x_a, y_b - y_a)
    direction_length = (direction_vector[0] ** 2 + direction_vector[1] ** 2) ** 0.5
    scaled_direction_vector = (
        direction_vector[0] * distance_ / direction_length,
        direction_vector[1] * distance_ / direction_length)
    x_new = x_a + scaled_direction_vector[0]
    y_new = y_a + scaled_direction_vector[1]
    return x_new, y_new
