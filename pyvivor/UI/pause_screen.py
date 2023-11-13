import pygame

from pyvivor.utils import configurator, FONT_PATH


class PauseScreen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.display_surface = configurator.game_screen
        self.position = (0, 0)
        self.size = (configurator.game_screen.get_width(), configurator.game_screen.get_height())
        font = pygame.font.Font(FONT_PATH, 64)
        self.text = font.render('PAUSE', True, 'red')
        self.alpha = 0

        self.player = None
        self.player_stats = None

    def update(self):
        self.create_alpha()
        self.display_surface.blit(self.text, (configurator.game_screen.get_width()/2 - self.text.get_width()/2, 100))

        if self.player:
            if not self.player_stats:
                self.player_stats = PlayerStatScreen(self.player)
            self.player_stats.update()
            self.display_surface.blit(self.player_stats.surface, (100, 240))

    def create_alpha(self):
        if self.alpha < 192:
            self.alpha += 8
        rect = pygame.Surface(self.size)
        rect.set_alpha(self.alpha)
        rect.fill('black')
        self.display_surface.blit(rect, self.position)


class PlayerStatScreen:
    def __init__(self, player):
        self.player = player
        self.surface = pygame.Surface((500, 720)).convert_alpha()
        self.color = "white"
        self.thickness = 1

        self.title_font = pygame.font.Font(FONT_PATH, 22)
        self.content_font = pygame.font.Font(FONT_PATH, 14)

        self.text_value_offset = 10

    def update(self):
        self.surface = pygame.Surface((500, 720)).convert_alpha()
        outer_rectangle = pygame.Rect(0, 0, self.surface.get_width(), self.surface.get_height())
        pygame.draw.rect(self.surface, self.color, outer_rectangle, self.thickness)
        self.draw_general_section()
        self.draw_defences_section()
        self.draw_attack_section()
        self.draw_misc_section(self.draw_movement_section())

    def draw_general_section(self):
        general_section_rectangle = pygame.Rect(0, 0, self.surface.get_width(), 40)
        pygame.draw.rect(self.surface, self.color, general_section_rectangle, self.thickness)
        general_section_title = self.title_font.render("General Stats", True, self.color)
        self.surface.blit(general_section_title, (10, 5))

        for stat_name, stat_value in dict(self.player).get('general').items():
            stat_name = self.content_font.render(stat_name, True, self.color)
            stat_value = self.content_font.render(str(stat_value), True, self.color)
            self.surface.blit(stat_name, (10, general_section_rectangle.bottom + 5))
            self.surface.blit(stat_value, (self.surface.get_width() - stat_value.get_width() - self.text_value_offset,
                                           general_section_rectangle.bottom + 5))
            general_section_rectangle.height += 20

    def draw_defences_section(self):
        offset = 150
        defences_section_rectangle = pygame.Rect(0, offset, self.surface.get_width(), 40)
        pygame.draw.rect(self.surface, self.color, defences_section_rectangle, self.thickness)
        draw_defences_section_title = self.title_font.render("Defences", True, self.color)
        self.surface.blit(draw_defences_section_title, (10, offset + 5))

        for stat_name, stat_value in dict(self.player).get('defences').items():
            stat_name = self.content_font.render(stat_name, True, self.color)
            stat_value = self.content_font.render(str(stat_value), True, self.color)
            self.surface.blit(stat_name, (10, defences_section_rectangle.bottom + 5))
            self.surface.blit(stat_value, (self.surface.get_width() - stat_value.get_width() - self.text_value_offset,
                                           defences_section_rectangle.bottom + 5))
            defences_section_rectangle.height += 20

    def draw_attack_section(self):
        offset = 300
        attack_section_rectangle = pygame.Rect(0, offset, self.surface.get_width(), 40)
        pygame.draw.rect(self.surface, self.color, attack_section_rectangle, self.thickness)
        draw_attack_section_title = self.title_font.render("Attack", True, self.color)
        self.surface.blit(draw_attack_section_title, (10, offset + 5))

        for stat_name, stat_value in dict(self.player).get('attack').items():
            stat_name = self.content_font.render(stat_name, True, self.color)
            value = f"{stat_value['value']:0.1f}"
            if stat_value['unit']:
                value += f" {stat_value['unit']}"
            stat_value = self.content_font.render(str(value), True, self.color)
            self.surface.blit(stat_name, (10, attack_section_rectangle.bottom + 5))
            self.surface.blit(stat_value, (self.surface.get_width() - stat_value.get_width() - self.text_value_offset,
                                           attack_section_rectangle.bottom + 5))
            attack_section_rectangle.height += 20

    def draw_movement_section(self):
        offset = 520
        movement_section_rectangle = pygame.Rect(0, offset, self.surface.get_width(), 40)
        pygame.draw.rect(self.surface, self.color, movement_section_rectangle, self.thickness)
        draw_movement_section_title = self.title_font.render("Movement", True, self.color)
        self.surface.blit(draw_movement_section_title, (10, offset + 5))

        next_offset = offset + 50
        for stat_name, stat_value in dict(self.player).get('movement').items():
            stat_name = self.content_font.render(stat_name, True, self.color)
            value = f"{stat_value['value']:0.1f}"
            if stat_value['unit']:
                value += f" {stat_value['unit']}"
            stat_value = self.content_font.render(str(value), True, self.color)
            self.surface.blit(stat_name, (10, movement_section_rectangle.bottom + 5))
            self.surface.blit(stat_value, (self.surface.get_width() - stat_value.get_width() - self.text_value_offset,
                                           movement_section_rectangle.bottom + 5))
            movement_section_rectangle.height += 20
            next_offset += 30
        return next_offset

    def draw_misc_section(self, offset):
        mist_section_rectangle = pygame.Rect(0, offset, self.surface.get_width(), 40)
        pygame.draw.rect(self.surface, self.color, mist_section_rectangle, self.thickness)
        draw_mist_section_title = self.title_font.render("Miscellaneous", True, self.color)
        self.surface.blit(draw_mist_section_title, (10, offset + 5))

        for stat_name, stat_value in dict(self.player).get('miscellaneous').items():
            stat_name = self.content_font.render(stat_name, True, self.color)
            value = f"{stat_value['value']:0.1f}"
            if stat_value['unit']:
                value += f" {stat_value['unit']}"
            stat_value = self.content_font.render(str(value), True, self.color)
            self.surface.blit(stat_name, (10, mist_section_rectangle.bottom + 5))
            self.surface.blit(stat_value, (self.surface.get_width() - stat_value.get_width() - self.text_value_offset,
                                           mist_section_rectangle.bottom + 5))
            mist_section_rectangle.height += 20

