import os
import subprocess
import sys

from .config import load_config, ROOT_DIR

SCRIPT_DIR = os.path.join(ROOT_DIR, 'scripts')


def _run(script, args):
    script_path = os.path.join(SCRIPT_DIR, script)
    cmd = [sys.executable, script_path] + args
    subprocess.check_call(cmd)


def generate_cards(num_cards=None, output=None):
    cfg = load_config()
    if num_cards is None:
        num_cards = cfg.getint('cards', 'num_cards')
    if output is None:
        output = cfg.get('paths', 'cards_output')
    _run('gencards.py', [str(num_cards), output])


def sort_photos(input_dir=None, output_dir=None):
    cfg = load_config()
    if input_dir is None:
        input_dir = cfg.get('paths', 'input_photos')
    if output_dir is None:
        output_dir = cfg.get('paths', 'sorted_photos')
    _run('sortphotos.py', [input_dir, output_dir])


def generate_thumbnails(directory=None, width=None, height=None):
    cfg = load_config()
    if directory is None:
        directory = cfg.get('paths', 'sorted_photos')
    if width is None:
        width = cfg.get('thumbnails', 'width')
    if height is None:
        height = cfg.get('thumbnails', 'height')
    _run('genthumbs.py', [directory, str(width), str(height)])
