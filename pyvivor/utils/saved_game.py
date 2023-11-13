from os import path
import pickle

HERE_PATH = path.dirname(path.abspath(__file__))
DATA_PATH = path.join(HERE_PATH, '..', 'saved_game.pkl')
DEFAULT = {
    "gold": 0,
    "buffs": [],
    "items": {
        "weapon": "",
        "armour": "",
        "pierce": "",
        "health": "",
        "critchance": "",
        "critdmg": "",
        "attackspeed": "",
        "betterexp": "",
        "bettergold": "",
        "movementspeed": "",
        "pickuprange": "",
        "liferegen": "",

        "lifeleech": "",
        "aoe": "",

    }
}


def load_game_data():
    if path.exists(DATA_PATH):
        with open(DATA_PATH, 'rb') as f:
            data = pickle.load(f)
        return data
    return DEFAULT


def save_game_data(data=None):
    if not data:
        data = DEFAULT
    with open(DATA_PATH, 'wb') as f:
        pickle.dump(data, f)
