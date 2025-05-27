import configparser
import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

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
    },
    'pricing': {
        'base_price': '1.0',
        'discount_rate': '0.1',
        'min_price': '0.5',
    },
    'payments': {
        'records_file': os.path.join(ROOT_DIR, 'payments.csv'),
    },
}

def load_config():
    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)
    config_file = os.environ.get(
        "QRPORTRAIT_CONFIG",
        os.path.join(ROOT_DIR, "config.ini")
    )
    if os.path.exists(config_file):
        config.read(config_file)
    return config
