import csv
import os
from datetime import datetime

from .config import load_config, ROOT_DIR


def calculate_total(num_photos, base_price, discount_rate, min_price):
    """Return total cost applying progressive discount."""
    total = 0.0
    for i in range(num_photos):
        price = base_price * (1 - discount_rate * i)
        if price < min_price:
            price = min_price
        total += price
    return total


def record_payment(customer, num_photos, total, records_file):
    """Append a payment record to the CSV file."""
    fields = ['datetime', 'customer', 'num_photos', 'total']
    now = datetime.now().isoformat()
    exists = os.path.exists(records_file)
    with open(records_file, 'a', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow({
            'datetime': now,
            'customer': customer,
            'num_photos': num_photos,
            'total': f"{total:.2f}",
        })


def checkout(customer, num_photos, extra_discount=0.0):
    """Compute final price and record payment."""
    cfg = load_config()
    base_price = cfg.getfloat('pricing', 'base_price', fallback=1.0)
    rate = cfg.getfloat('pricing', 'discount_rate', fallback=0.0)
    min_price = cfg.getfloat('pricing', 'min_price', fallback=0.0)
    records_file = cfg.get('payments', 'records_file', fallback=os.path.join(ROOT_DIR, 'payments.csv'))

    total = calculate_total(num_photos, base_price, rate, min_price)
    if extra_discount:
        total *= max(0.0, 1 - extra_discount)

    record_payment(customer, num_photos, total, records_file)
    return total
