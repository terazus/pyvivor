from pyvivor.utils import load_game_data, save_game_data


class User:

    def __init__(self):
        self.gold = 0
        self.items = {}
        self.load()

    def load(self):
        data = load_game_data()
        self.gold = data['gold']
        self.items = data['items']
        self.gold = 1000000

    def save(self):
        data = {'gold': self.gold, 'items': self.items}
        save_game_data(data)

    def reset_gold(self):
        self.gold = 0
        self.save()
