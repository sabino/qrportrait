import csv
import os

from qrportrait_app import payment


def test_calculate_total_applies_progressive_discount():
    total = payment.calculate_total(3, base_price=1.0, discount_rate=0.2, min_price=0.5)
    # price per photo: 1.0, 0.8, 0.6 -> total 2.4
    assert total == 2.4


def test_record_payment_writes_csv(tmp_path, monkeypatch):
    records = tmp_path / 'pay.csv'
    cfg = tmp_path / 'config.ini'
    cfg.write_text('[pricing]\nbase_price=1\ndiscount_rate=0.1\nmin_price=0.5\n'
                   '\n[payments]\nrecords_file=' + str(records) + '\n')
    monkeypatch.setenv('QRPORTRAIT_CONFIG', str(cfg))

    total = payment.checkout('ABC', 2, extra_discount=0.0)
    assert os.path.exists(records)
    with open(records, newline='') as fh:
        rows = list(csv.DictReader(fh))
    assert rows[0]['customer'] == 'ABC'
    assert rows[0]['num_photos'] == '2'
    assert float(rows[0]['total']) == total
