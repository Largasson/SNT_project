import csv

with open('text.csv', 'r', encoding='cp1251') as f:
    rows = csv.DictReader(f, delimiter=';')
    for row in rows:
        print(row)

