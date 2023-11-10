from sys import exit
from os import path
import pygame


HERE_PATH = path.dirname(__file__)
DEFAULT_OUTPUT_PATH = path.join(HERE_PATH, 'background.png')


def main():
    pygame.init()
    pygame.display.set_caption('Background Generator')
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    clock = pygame.time.Clock()

    while True:
        generate_background()
        clock.tick(60)
        pygame.quit()
        exit()


def generate_background(
    screen=(1980, 1024),
    grid_width=3,
    grid_height=3
):
    surface = pygame.Surface((screen[0] * grid_width, screen[1] * grid_height), pygame.SRCALPHA)
    surface.fill((255, 255, 255, 0))

    for width in range(grid_width):
        for height in range(grid_height):
            rect = pygame.Rect(width * screen[0], height * screen[1], screen[0], screen[1])
            pygame.draw.rect(surface, 'red', rect, 1)

    pygame.image.save(surface, DEFAULT_OUTPUT_PATH)


if __name__ == '__main__':
    main()
