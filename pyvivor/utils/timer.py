import pygame

from pyvivor.utils import game_status


class Timer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.start_timer = 0
        self.time = 0
        self.offset = 0
        self.pause_timer = 0
        self.total_offset = 0

        self.started = False
        self.paused = False
        self.resumed = False

    def update(self):
        self.__start()
        if game_status.paused or game_status.levelling_up or game_status.game_over:
            self.__pause()
        else:
            self.paused = False
            self.__resume()
            self.__run_timer()

    def __start(self):
        if not self.started:
            self.start_timer = pygame.time.get_ticks()
            self.started = True

    def __run_timer(self):
        """ Execute to update the timer when the game is not paused """
        self.time = pygame.time.get_ticks() - self.start_timer - self.total_offset

    def __pause(self):
        """ Execute to start the pause timer """
        if not self.paused:
            self.pause_timer = pygame.time.get_ticks() - self.start_timer
            self.paused = True
            self.resumed = False
        self.offset = pygame.time.get_ticks() - self.start_timer - self.pause_timer

    def __resume(self):
        if not self.resumed and not self.paused:
            self.total_offset += self.offset
            self.resumed = True

    def reset(self):
        self.start_timer = 0
        self.time = 0
        self.offset = 0
        self.pause_timer = 0
        self.total_offset = 0

        self.started = False
        self.paused = False
        self.resumed = False
