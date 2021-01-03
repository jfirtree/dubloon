import csv
import json
from datetime import datetime
from pathlib import Path

from money import Money

from dubloon import Transaction


def get_amount(row, field_names):
    if 'amount' in field_names:
        return Money(row[field_names['amount']], 'USD')
    amount = row[field_names['debit']]
    if amount != '':
        return -1 * Money(amount, 'USD')
    else:
        return Money(row[field_names['credit']], 'USD')


def import_transactions(csv_filename, field_names, default_payment_identifier=''):
    transaction_data = []
    with open(csv_filename) as csvfile:
        transaction_reader = csv.DictReader(csvfile)
        should_import_category = 'card_category' in field_names

        for row in transaction_reader:
            transaction_to_add = Transaction()
            date_string = row[field_names['transaction_date']]
            transaction_datetime = datetime.strptime(date_string, field_names['date_format'])
            transaction_to_add.transaction_date = transaction_datetime.strftime('%Y-%m-%d')
            transaction_to_add.description = row[field_names['description']]
            if should_import_category:
                transaction_to_add.category = row[field_names['card_category']]
            transaction_to_add.amount = get_amount(row, field_names)
            transaction_to_add.payment_identifier = default_payment_identifier
            transaction_data.append(transaction_to_add)
    return transaction_data


def import_configs(config_dir):
    csv_format_schemas = dict()
    for file in Path(config_dir).iterdir():
        if file.suffix == '.json':
            structure_file = open(file.absolute())
            csv_format_schemas[file.stem] = json.load(structure_file)
    return csv_format_schemas


def import_csvs(csv_dir, csv_format_schemas):
    data = []
    for file in Path(csv_dir).iterdir():
        if file.suffix == '.csv':
            for key in csv_format_schemas.keys():
                if key in str(file.stem):
                    print('importing {} file {}'.format(key, file))
                    data.extend(import_transactions(file, csv_format_schemas[key], key))
    return data


def export(transactions, dest_file):
    with open(dest_file, 'w') as export_file:
        csv_writer = csv.writer(export_file)
        for transaction in transactions:
            row_to_write = [transaction.description, transaction.category, transaction.amount,
                            transaction.payment_identifier, transaction.transaction_date]
            csv_writer.writerow(row_to_write)


def pipeline():
    formats = import_configs('../config/')
    csv_data = import_csvs('../import/', formats)
    csv_data.sort()
    export(csv_data, 'aggregate.csv')


if __name__ == '__main__':
    pipeline()
