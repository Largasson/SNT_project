import csv
import io
from datetime import date

class Exception_csv_file(Exception):
    pass
def gen_temp_dict(day, month, year):
    """Функция генерирует временный словарь с заданными по умолчанию значениями для всех требуемых ключей"""
    return {
        'area_number': 0,
        'member_fee': 0,
        'targeted_fee': 0,
        'electricity_payments': 0,
        'date': date(year, month, day)
        }

def string_to_float(row: dict, key: str):
    """Функция проверяет есть ли в поле по ключу какие-то значение.
    Если есть, то обрабатывает строку и приводит ее значение к float."""
    if 'кредит' in key and row[key]:
        return -float(row[key].replace(',', '.').replace(' ', ''))
    elif 'дебет' in key and row[key]:
        return float(row[key].replace(',', '.').replace(' ', ''))


def parsing_csv(file):

# with (open('../76.csv', 'r', encoding='cp1251') as file):
    text = file.readlines()
    for index, row in enumerate(text):
        if row.startswith('Контрагенты'):
            break
    else:
        raise Exception_csv_file('Неправильный csv-файл. Нет поля "Контрагенты"')
    # получаем дату формирования "оборотки"
    # проверка файла на форматную запись даты
    try:
        current_date = text[1].split(';')
        current_date = current_date[0].split('-')[-1].strip()
        day, month, year = map(int, current_date.split('.'))
    except ValueError as err:
        print(f'Некорректные данные строки с датой - {err}')
        raise Exception_csv_file('Проверь csv-файл')

    text.pop(index+1) # удаление строки со словом Договоры
    text.pop(index+1) # удаление строки с общими цифрами
    l = ''.join(text[index:])
    data = io.StringIO(l)
    our_dict = csv.DictReader(data, delimiter=';')  # словарь для БД
    # for row in our_dict:
    #     print(row)

    list_of_stop = ['Целевые взносы', 'Членские взносы', 'Электроэнергия', 'Итого', 'Итого развернутое']
    list_of_keys = [f'кредит на {current_date}', f'дебет на {current_date}']
    res_dict = {} # итоговый словарь
    area_number = 0
    temp_dict = 0
    for row in our_dict:
        if row['Контрагенты'].strip() not in list_of_stop:
            res_dict[area_number] = temp_dict
            temp_dict = gen_temp_dict(day, month, year)
            area_number = int(row['Контрагенты'].split()[-1])
            temp_dict['area_number'] = int(area_number)
        elif row['Контрагенты'].strip() == 'Целевые взносы':
            for key in list_of_keys:
                value_by_key = string_to_float(row, key)
                if value_by_key:
                    temp_dict['targeted_fee'] = value_by_key
        elif row['Контрагенты'].strip() == 'Членские взносы':
            for key in list_of_keys:
                value_by_key = string_to_float(row, key)
                if value_by_key:
                    temp_dict['member_fee'] = value_by_key
        elif row['Контрагенты'].strip() == 'Электроэнергия':
            for key in list_of_keys:
                value_by_key = string_to_float(row, key)
                if value_by_key:
                    temp_dict['electricity_payments'] = value_by_key

    res_dict[area_number] = temp_dict
    del res_dict[0]
    return res_dict




if __name__ == '__main__':
    res_dict = parsing_csv(file)
    for k, v in res_dict.items():
        print(v)