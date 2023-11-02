import pygame

from .levels import WelcomeScreen, World
from .utils import leave_game, GAME_TITLE, configurator, FPS, game_status
from .UI import PauseScreen


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

        self.screen = configurator.game_screen
        self.clock = pygame.time.Clock()
        self.welcome_screen = WelcomeScreen()
        self.world = World()

        self.pause_screen = PauseScreen()

    def run(self):
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    leave_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and game_status.started and not game_status.shopping:
                        if game_status.paused:
                            self.world.unpause()
                        else:
                            self.world.pause()

            self.screen.fill('black')
            self.world.run()
            if not game_status.started and not game_status.shopping:
                self.welcome_screen.run()

            if game_status.started and game_status.paused:
                self.pause_screen.update()

            pygame.display.update()
            self.clock.tick(FPS)
