import csv
import io
from datetime import date
from typing import TypedDict
from webapp.config import (TARGETED_FEE, MEMBER_FEE, ELECTRICITY_PAYMENTS,
                           TOTAL, TOTAL_EXPANDED, COUNTERPARTIES,
                           CREDIT_FOR, DEBIY_FOR)



class Error_csv_file(Exception):
    pass


class TempDict(TypedDict):
    """Аннотирование значений словаря"""
    area_number: int
    member_fee: float
    targeted_fee: float
    electricity_payments: float
    date: date


def gen_temp_dict(format_date):
    """Функция генерирует временный словарь с заданными по умолчанию значениями для всех требуемых ключей"""
    return TempDict(
        area_number=0,
        member_fee=0,
        targeted_fee=0,
        electricity_payments=0,
        date=format_date
    )


def string_to_float(row: dict, key: str):
    """Функция проверяет есть ли в поле по ключу какие-то значение.
    Если есть, то обрабатывает строку и приводит ее значение к float."""
    if 'кредит' in key and row[key]:
        return -float(row[key].replace(',', '.').replace(' ', ''))
    elif 'дебет' in key and row[key]:
        return float(row[key].replace(',', '.').replace(' ', ''))
    return 0


def extract_date(header: str):
    """Получение даты формирования "оборотки" из шапки csv-файла"""
    current_date = header.split(';')
    current_date = current_date[0].split('-')[-1].strip()
    day, month, year = map(int, current_date.split('.'))
    return current_date, date(year, month, day)


def parsing_csv(file):
    """Главная функция парсинга"""

    text = file.readlines()
    for index, row in enumerate(text):
        if row.startswith(COUNTERPARTIES):
            break
    else:
        raise Error_csv_file('Неправильный csv-файл. Нет поля "Контрагенты"')

    try:
        tuple_date = extract_date(text[1])
        current_date = tuple_date[0]  # строка используемая при подстановке
        format_date = tuple_date[1]  # дада в формате datetime
    except ValueError as err:
        print(f'Некорректные данные строки с датой - {err}')
        raise Error_csv_file('Проверь csv-файл')

    list_of_stop = [TARGETED_FEE, MEMBER_FEE, ELECTRICITY_PAYMENTS, TOTAL, TOTAL_EXPANDED]
    list_of_keys = [CREDIT_FOR + current_date, DEBIY_FOR + current_date]

    text.pop(index + 1)  # удаление строки со словом Договоры
    text.pop(index + 1)  # удаление строки с общими цифрами
    l = ''.join(text[index:])
    data = io.StringIO(l)
    our_dict = csv.DictReader(data, delimiter=';')  # исходный csv.DictReader список словарей
    # for row in our_dict:
    #     print(row)

    res_dict = {}  # итоговый словарь

    temp_dict = None
    for row in our_dict:
        if row[COUNTERPARTIES].strip() not in list_of_stop:
            area_number = int(row[COUNTERPARTIES].split()[-1])
            temp_dict = gen_temp_dict(format_date)
            temp_dict['area_number'] = int(area_number)
            res_dict[area_number] = temp_dict
        elif row[COUNTERPARTIES].strip() == TARGETED_FEE:
            for key in list_of_keys:
                temp_dict['targeted_fee'] += string_to_float(row, key)
        elif row[COUNTERPARTIES].strip() == MEMBER_FEE:
            for key in list_of_keys:
                temp_dict['member_fee'] += string_to_float(row, key)
        elif row[COUNTERPARTIES].strip() == ELECTRICITY_PAYMENTS:
            for key in list_of_keys:
                temp_dict['electricity_payments'] += string_to_float(row, key)
    return res_dict









