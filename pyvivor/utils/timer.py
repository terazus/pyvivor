import pygame


class Timer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.start = pygame.time.get_ticks()
        self.time = 0
        self.offset = 0
        self.pause_timer = 0
        self.total_offset = 0

    def run_timer(self):
        """ Execute to update the timer when the game is not paused """
        self.time = pygame.time.get_ticks() - self.start - self.total_offset

    def pause(self):
        """ Execute to start the pause timer """
        self.pause_timer = pygame.time.get_ticks() - self.start

    def run_pause(self):
        """ Execute to update the pause timer """
        self.offset = pygame.time.get_ticks() - self.start - self.pause_timer

    def unpause(self):
        self.total_offset += self.offset
