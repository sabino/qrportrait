import configparser
import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE = os.environ.get(
    "QRPORTRAIT_CONFIG",
    os.path.join(ROOT_DIR, "config.ini")
)

DEFAULT_CONFIG = {
    'paths': {
        'cards_output': os.path.join(ROOT_DIR, 'cards.pdf'),
        'input_photos': os.path.join(ROOT_DIR, 'input_photos'),
        'sorted_photos': os.path.join(ROOT_DIR, 'sorted_photos'),
    },
    'thumbnails': {
        'width': '200',
        'height': '200',
    },
    'cards': {
        'num_cards': '10',
    }
}

def load_config():
    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    return config
