import csv
from typing import Any


def save_to_csv(form: dict[str, Any]) -> None:
    with open(
        './data/cafes.csv', mode='a', encoding='utf-8', newline=''
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=form.keys())
        writer.writerow(form)


def read_csv() -> dict[str, Any]:
    with open('./data/cafes.csv', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        rows = list(reader)

    return {'headers': reader.fieldnames, 'rows': rows}
