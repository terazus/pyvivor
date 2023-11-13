import pygame

from pyvivor.utils import configurator, FONT_PATH


class GameOverScreen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.text = pygame.font.Font(FONT_PATH, 64).render('GAME OVER', True, 'red')

        self.retry_rect = pygame.Rect(0, 520, 400, 100)
        self.retry_rect.centerx = configurator.screen_width / 2
        self.exit_rect = self.retry_rect.copy()
        self.exit_rect.y += self.retry_rect.height + 20

        self.position = (0, 0)
        self.text_position = (configurator.screen_width / 2 - self.text.get_width() / 2, 100)
        self.alpha = 0
        self.size = (configurator.screen_width, configurator.screen_height)

        self.timer = "00:00:00"
        self.kill_count = 0
        self.gold_obtained = 0

    def update(self):
        self.draw()
        configurator.game_screen.blit(self.text, self.text_position)
        self.create_text_summary()
        self.create_buttons()

    def draw(self):
        if self.alpha < 192:
            self.alpha += 16
        rect = pygame.Surface(self.size)
        rect.set_alpha(self.alpha)
        rect.fill('black')
        configurator.game_screen.blit(rect, self.position)

    def create_text_summary(self):
        text_font = pygame.font.Font(FONT_PATH, 18)
        rect_y = self.text_position[1] + self.text.get_height() + 20
        rect = pygame.Rect(configurator.screen_width / 2 - 200, rect_y, 400, 300)

        time_text = text_font.render('Time:', True, 'white')
        time_value = text_font.render(self.timer, True, 'white')
        configurator.game_screen.blit(time_text, (rect.x + 20, rect.y + 20))
        configurator.game_screen.blit(time_value, (rect.right - time_value.get_rect().width - 20, rect.y + 20))

        kill_text = text_font.render('Kills:', True, 'white')
        kill_value = text_font.render(str(self.kill_count), True, 'white')
        configurator.game_screen.blit(kill_text, (rect.x + 20, rect.y + 60))
        configurator.game_screen.blit(kill_value, (rect.right - kill_value.get_rect().width - 20, rect.y + 60))

        gold_text = text_font.render('Gold:', True, 'white')
        gold_value = text_font.render(str(self.gold_obtained), True, 'white')
        pygame.draw.rect(configurator.game_screen, 'white', rect, 1)
        configurator.game_screen.blit(gold_value, (rect.right - gold_value.get_rect().width - 20, rect.y + 100))

        configurator.game_screen.blit(gold_text, (rect.x + 20, rect.y + 100))

    def create_buttons(self):
        # Retry button
        text_font = pygame.font.Font(FONT_PATH, 28)
        pygame.draw.rect(configurator.game_screen, 'white', self.retry_rect, 0)
        retry_text = text_font.render('RETRY', True, 'black')
        configurator.game_screen.blit(retry_text,
                                      (self.retry_rect.x + self.retry_rect.width/2 - retry_text.get_width()/2,
                                       self.retry_rect.y + self.retry_rect.height/2 - retry_text.get_height()/2))

        # Back to menu button
        pygame.draw.rect(configurator.game_screen, 'white', self.exit_rect, 0)
        back_text = text_font.render('BACK TO MENU', True, 'black')
        configurator.game_screen.blit(back_text,
                                      (self.exit_rect.x + self.exit_rect.width/2 - back_text.get_width()/2,
                                       self.exit_rect.y + self.exit_rect.height/2 - back_text.get_height()/2))
