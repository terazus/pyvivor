class GameStatus:

    def __init__(self):
        self.started = False
        self.paused = False
        self.lost = False
        self.won = False
        self.shopping = False
        self.levelling_up = False

    def start_game(self):
        self.started = True

    def start_shopping(self):
        print('Shopping')
        pass

    def pause_game(self):
        self.paused = True


game_status = GameStatus()
