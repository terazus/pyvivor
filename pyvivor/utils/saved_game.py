from os import path

HERE_PATH = path.dirname(path.abspath(__file__))
DATA_PATH = path.join(HERE_PATH, '..', 'saved_game.pkl')


def load_game_data():
    import pickle
    with open(DATA_PATH, 'rb') as f:
        data = pickle.load(f)
    return data