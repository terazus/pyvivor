from os import path
import pygame


BUTTONS_PATH = path.dirname(__file__)


def convert():
    pygame.init()
    pygame.display.set_mode()

    buttons_spreadsheet_path = path.join(BUTTONS_PATH, 'm.jpg')
    image = pygame.image.load(buttons_spreadsheet_path).convert_alpha()
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            image_attr = image.get_at((x, y))
            if 180 < image_attr[0] and 180 < image_attr[1] and 180 < image_attr[2]:
                image.set_at((x, y), (255, 255, 255, 0))

    output = path.join(BUTTONS_PATH, "converted2.png")
    pygame.image.save(image, output)


if __name__ == "__main__":
    convert()