import os
import sys
from unittest import mock



def create_config(tmp_path):
    cfg = tmp_path / 'config.ini'
    cfg.write_text('[paths]\n' \
                   'cards_output=out.pdf\n' \
                   'input_photos=in_dir\n' \
                   'sorted_photos=sorted\n' \
                   '\n[thumbnails]\n' \
                   'width=100\n' \
                   'height=150\n' \
                   '\n[cards]\n' \
                   'num_cards=7\n')
    return cfg


def test_generate_cards_uses_config(tmp_path, monkeypatch):
    cfg_path = create_config(tmp_path)
    monkeypatch.setenv('QRPORTRAIT_CONFIG', str(cfg_path))
    import qrportrait_app.scripts_runner as sr
    called = {}

    def fake_call(cmd):
        called['cmd'] = cmd
    monkeypatch.setattr('subprocess.check_call', fake_call)

    sr.generate_cards()
    cmd = called['cmd']
    assert cmd[0] == sys.executable
    assert cmd[1].endswith('gencards.py')
    assert cmd[2:] == ['7', 'out.pdf']


def test_sort_photos_uses_config(tmp_path, monkeypatch):
    cfg_path = create_config(tmp_path)
    monkeypatch.setenv('QRPORTRAIT_CONFIG', str(cfg_path))
    import qrportrait_app.scripts_runner as sr
    called = {}

    def fake_call(cmd):
        called['cmd'] = cmd
    monkeypatch.setattr('subprocess.check_call', fake_call)

    sr.sort_photos()
    cmd = called['cmd']
    assert cmd[1].endswith('sortphotos.py')
    assert cmd[2:] == ['in_dir', 'sorted']


def test_generate_thumbnails_uses_config(tmp_path, monkeypatch):
    cfg_path = create_config(tmp_path)
    monkeypatch.setenv('QRPORTRAIT_CONFIG', str(cfg_path))
    import qrportrait_app.scripts_runner as sr
    called = {}

    def fake_call(cmd):
        called['cmd'] = cmd
    monkeypatch.setattr('subprocess.check_call', fake_call)

    sr.generate_thumbnails()
    cmd = called['cmd']
    assert cmd[1].endswith('genthumbs.py')
    assert cmd[2:] == ['sorted', '100', '150']
