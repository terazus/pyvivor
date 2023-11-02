import math


def calculate_angle_between_points(a, b, c):
    vector_ab = (a[0] - b[0], a[1] - b[1])
    vector_bc = (c[0] - b[0], c[1] - b[1])
    dot_product = vector_ab[0] * vector_bc[0] + vector_ab[1] * vector_bc[1]
    magnitude_ab = math.sqrt(vector_ab[0] ** 2 + vector_ab[1] ** 2)
    magnitude_bc = math.sqrt(vector_bc[0] ** 2 + vector_bc[1] ** 2)
    if magnitude_ab != 0 and magnitude_bc != 0:
        cos_theta = dot_product / (magnitude_ab * magnitude_bc)
        angle_radians = math.acos(cos_theta)
        cross_product = vector_ab[0] * vector_bc[1] - vector_ab[1] * vector_bc[0]
        if cross_product < 0:
            angle_radians = -angle_radians
        angle_degrees = math.degrees(angle_radians)
        return -angle_degrees
    return None


def distance(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))


def collide(source, target):
    return distance(source['x'], source['y'], target['x'], target['y']) < source['radius'] + target['radius']


def rotate_point_around_origin(point, angle_degrees):
    x, y = point
    angle_radians = math.radians(-angle_degrees)
    new_x = x * math.cos(angle_radians) - y * math.sin(angle_radians)
    new_y = x * math.sin(angle_radians) + y * math.cos(angle_radians)
    return new_x, new_y


def rotate_point_around_point(a, b, angle_degrees):
    relative_x = b[0] - a[0]
    relative_y = b[1] - a[1]
    new_relative_x, new_relative_y = rotate_point_around_origin((relative_x, relative_y), angle_degrees)

    new_x = a[0] + new_relative_x
    new_y = a[1] + new_relative_y
    return new_x, new_y


def interpolate_close_point(source, target, distance_):
    total_distance = distance(source['x'], source['y'], target['x'], target['y'])
    ratio = distance_ / total_distance
    x = math.ceil(source['x'] + (ratio * (target['x'] - source['x'])))
    y = math.ceil(source['y'] + (ratio * (target['y'] - source['y'])))
    return x, y


def calculate_movement_vector(a, b, speed):
    direction_x = b[0] - a[0]
    direction_y = b[1] - a[1]
    distance_ = math.sqrt(direction_x**2 + direction_y**2)
    if distance_ < speed:
        return None
    scaled_direction_x = (direction_x / distance_) * speed
    scaled_direction_y = (direction_y / distance_) * speed
    return scaled_direction_x, scaled_direction_y


