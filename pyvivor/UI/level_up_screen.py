import pygame

from pyvivor.utils import configurator, FONT_PATH


class LevelUpScreen:
    def __init__(self, buff_manager):
        self.position = (0, 0)
        self.title_text = pygame.font.Font(FONT_PATH, 64).render('LEVEL UP', True, 'white')
        self.quit_text = pygame.font.Font(FONT_PATH, 32).render('EXIT', True, 'black')
        self.title_pos_x = (configurator.screen_width / 2) - self.title_text.get_width() / 2
        self.title_pos_y = 200
        self.quit_rect = None
        self.alpha = 0
        self.buff_manager = buff_manager

    def update(self):
        self.draw()
        configurator.game_screen.blit(self.title_text, (self.title_pos_x, self.title_pos_y))

        width = 800
        pos_x = (configurator.screen_width / 2) - width / 2
        shop_rect = pygame.Rect(pos_x, self.title_pos_y + 100, width, 300)
        overlay_rect = pygame.Rect(pos_x + 1, self.title_pos_y + 101, width - 2, 298)

        pygame.draw.rect(configurator.game_screen, 'white', shop_rect, 1)
        pygame.draw.rect(configurator.game_screen, 'black', overlay_rect, 0)

        self.buff_manager.draw_buffs(shop_rect)

    def draw(self):
        if self.alpha < 192:
            self.alpha += 16
        rect = pygame.Surface((configurator.screen_width, configurator.screen_height), pygame.SRCALPHA)
        rect.set_alpha(self.alpha)
        rect.fill('black')
        configurator.game_screen.blit(rect, self.position)
