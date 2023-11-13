import pygame

from .levels import WelcomeScreen, World
from .utils import leave_game, GAME_TITLE, configurator, FPS, game_status, FONT_PATH
from .UI import PauseScreen, GameOverScreen, ShopScreen
from .user import User


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(128)
        pygame.display.set_caption(GAME_TITLE)
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

        self.screen = configurator.game_screen
        self.clock = pygame.time.Clock()

        self.user = User()
        self.welcome_screen = WelcomeScreen()
        self.shop_screen = ShopScreen(self.user)
        self.game_over_screen = GameOverScreen()
        self.pause_screen = PauseScreen()
        self.world = World(pause_screen=self.pause_screen, shop=self.shop_screen)

    def run(self):
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    leave_game()

                if event.type == pygame.KEYDOWN:
                    condition = (game_status.started and not game_status.shopping
                                 and not game_status.levelling_up and not game_status.game_over)
                    if event.key == pygame.K_ESCAPE and condition:
                        self.world.unpause() if game_status.paused else self.world.pause()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if game_status.shopping:
                        mouse_position = pygame.mouse.get_pos()
                        self.shop_screen.handle_clicks(action="sell", mouse_position=mouse_position)
                        self.shop_screen.handle_clicks(action="buy", mouse_position=mouse_position)

            self.screen.fill('black')
            self.main_loop()

            font = pygame.font.Font(FONT_PATH, 20)
            text = font.render(f'FPS: {str(int(self.clock.get_fps()))}', True, 'white')
            self.screen.blit(text, (self.screen.get_rect().right - text.get_rect().width - 10, 0))

            pygame.display.update()
            self.clock.tick(FPS)

    def main_loop(self):
        self.world.run()
        if not game_status.started and not game_status.shopping:
            self.welcome_screen.run()

        if game_status.started and game_status.paused:
            self.pause_screen.update()

        if game_status.game_over:
            self.game_over_screen.gold_obtained = self.world.player.gold
            self.game_over_screen.timer = self.world.global_timer.get_text_time()
            self.game_over_screen.kill_count = self.world.kill_count

            self.game_over_screen.update()
            self.retry()
            self.back_to_menu()

            if not game_status.game_saved:
                self.user.gold += self.world.player.gold
                self.user.save()
                game_status.game_saved = True

        if game_status.shopping:
            self.shop_screen.update()
            if self.shop_screen.exit_shop():
                self.world = World(pause_screen=self.pause_screen, shop=self.shop_screen)

    def retry(self):
        rect = self.game_over_screen.retry_rect
        mouse = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        if mouse[0] and rect.collidepoint(mouse_position):
            self.pause_screen = PauseScreen()
            self.world = World(pause_screen=self.pause_screen, shop=self.shop_screen)
            game_status.reset()
            game_status.started = True
            self.game_over_screen.alpha = 0
            self.game_over_screen = GameOverScreen()

    def back_to_menu(self):
        rect = self.game_over_screen.exit_rect
        mouse = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        if mouse[0] and rect.collidepoint(mouse_position):
            self.pause_screen = PauseScreen()
            self.world = World(pause_screen=self.pause_screen, shop=self.shop_screen)
            game_status.reset()
            self.game_over_screen.alpha = 0
            self.game_over_screen = GameOverScreen()
