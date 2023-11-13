class GameStatus:

    def __init__(self):
        self.started = False
        self.paused = False
        self.lost = False
        self.won = False
        self.shopping = False
        self.levelling_up = False
        self.game_over = False
        self.game_saved = False

    def start_game(self):
        self.started = True

    def start_shopping(self):
        self.shopping = True

    def pause_game(self):
        self.paused = True

    def reset(self):
        self.started = False
        self.paused = False
        self.lost = False
        self.won = False
        self.shopping = False
        self.levelling_up = False
        self.game_over = False
        self.game_saved = False


game_status = GameStatus()
