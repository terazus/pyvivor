from sys import exit
from os import path
from random import randrange
import math
import json

import pygame


HERE_PATH = path.dirname(__file__)
GRAPHICS_PATH = path.join(HERE_PATH, '..', '..', 'assets', 'graphics')
DEFAULT_IMG = path.join(GRAPHICS_PATH, 'star.png')
DEFAULT_OUTPUT_PATH = path.join(GRAPHICS_PATH, 'backgrounds', 'background.png')
DEFAULT_INPUT_PATH = path.join(HERE_PATH, 'worlds', 'test.json')
TRANSPARENT = (255, 255, 255, 0)


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    pygame.display.set_caption('Background Generator')
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    clock = pygame.time.Clock()

    while True:
        generate_background()
        clock.tick(60)
        pygame.quit()
        exit()


def generate_background(file=DEFAULT_INPUT_PATH, image=DEFAULT_IMG):
    data = read_input_file(file)

    images = load_image(data['items'], image)
    screen = data['screen']
    grid_width = data['grid_width']
    grid_height = data['grid_height']

    surface = pygame.Surface((screen[0] * grid_width, screen[1] * grid_height), pygame.SRCALPHA)
    surface.fill('black')

    for width in range(grid_width):
        for height in range(grid_height):

            items = []
            min_left = width * screen[0]
            max_right = min_left + screen[0]
            min_top = height * screen[1]
            max_bottom = min_top + screen[1]

            for itemName, itemProps in data['items'].items():
                for i in range (itemProps['quantity']):
                    rand_x = randrange(min_left, max_right)
                    rand_y = randrange(min_top, max_bottom)
                    while (rand_x, rand_y) in items:
                        rand_x = randrange(min_left, max_right)
                        rand_y = randrange(min_top, max_bottom)
                    surface.blit(images[itemName], (rand_x, rand_y))

    pygame.image.save(surface, DEFAULT_OUTPUT_PATH)


def load_image(items, image):
    images = {}
    for item_name, item in items.items():
        if item_name not in images:
            img = pygame.transform.scale(pygame.image.load(image).convert_alpha(), item['scale'])
            img.set_alpha(item['alpha'])
            images[item_name] = img
    return images


def read_input_file(file):
    with open(file) as f:
        data = json.load(f)
    return data


def test_particles():
    pygame.init()
    screen = pygame.display.set_mode((2200, 1100))
    pygame.display.set_caption('Background Generator')
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    clock = pygame.time.Clock()
    particles = []

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill('black')
        generate_particles(screen, particles, clock)
        pygame.display.update()
        clock.tick(120)


def generate_particles(screen, particles, clock):
    circle_speed = 20
    screen_rect = screen.get_rect()
    origin_point = (screen_rect.centerx, screen_rect.centery)
    surface = pygame.Surface((20, 20), pygame.SRCALPHA).convert_alpha()
    pygame.draw.circle(surface, 'white', (10, 10), 5)

    for i in range(150):
        target_x = randrange(0, screen_rect.width)
        target_y = randrange(0, screen_rect.height)
        screen.blit(surface, origin_point)
        vector = calculate_movement_vector(origin_point, (target_x, target_y), circle_speed)
        particles.append((surface, vector, origin_point))

    for i, (surface, vector, current_position) in enumerate(particles):
        if vector:
            next_position = (current_position[0] + vector[0], current_position[1] + vector[1])
            surface_rect = surface.get_rect()
            surface_rect.x = next_position[0]
            surface_rect.y = next_position[1]
            if next_position[0] < 0 or next_position[0] > screen_rect.width or next_position[1] < 0 or next_position[1] > screen_rect.height:
                particles.remove((surface, vector, current_position))
            else:
                screen.blit(surface, surface_rect)
                particles[i] = (surface, vector, next_position)
        else:
            particles.remove((surface, vector, current_position))

    print(len(particles))
    print(clock.get_fps())


def calculate_movement_vector(a, b, speed):
    direction_x = b[0] - a[0]
    direction_y = b[1] - a[1]
    distance_ = math.sqrt(direction_x**2 + direction_y**2)
    if distance_ < speed:
        return None
    scaled_direction_x = (direction_x / distance_) * speed
    scaled_direction_y = (direction_y / distance_) * speed
    return scaled_direction_x, scaled_direction_y


if __name__ == '__main__':
    test_particles()
