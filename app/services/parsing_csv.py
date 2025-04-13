import csv
from io import StringIO
from datetime import date
from typing import TypedDict, Dict
from app.config import PARSING_CONSTANTS
from app.extensions.logger import logger

# Загрузка констант из конфигурации
TARGETED_FEE = PARSING_CONSTANTS['TARGETED_FEE']
MEMBER_FEE = PARSING_CONSTANTS['MEMBER_FEE']
ELECTRICITY_PAYMENTS = PARSING_CONSTANTS['ELECTRICITY_PAYMENTS']
TOTAL = PARSING_CONSTANTS['TOTAL']
TOTAL_EXPANDED = PARSING_CONSTANTS['TOTAL_EXPANDED']
COUNTERPARTIES = PARSING_CONSTANTS['COUNTERPARTIES']
CREDIT_FOR = PARSING_CONSTANTS['CREDIT_FOR']
DEBIT_FOR = PARSING_CONSTANTS['DEBIT_FOR']


class CsvFileError(Exception):
    """Исключение для ошибок обработки CSV-файла"""
    pass


class TempDict(TypedDict):
    """Аннотирование полей словаря для временного хранения данных"""
    area_number: int
    member_fee: float
    targeted_fee: float
    electricity_payments: float
    date: date


def gen_temp_dict(format_date: date) -> TempDict:
    """
    Генерация временного словаря с нулевыми значениями для всех полей и заданной датой.
    """
    return TempDict(
        area_number=0,
        member_fee=0.0,
        targeted_fee=0.0,
        electricity_payments=0.0,
        date=format_date
    )


def string_to_float(row: dict, key: str) -> float:
    """
    Преобразует строковое значение по ключу в численное значение типа float.
    Учитывает наличие дебета/кредита и обрабатывает разделители.
    """
    try:
        if 'дебет' in key and row[key]:
            return -float(row[key].replace(',', '.').replace(' ', ''))
        elif 'кредит' in key and row[key]:
            return float(row[key].replace(',', '.').replace(' ', ''))
        return 0.0
    except (ValueError, KeyError) as e:
        logger.warning(f"Не удалось преобразовать значение: поле {key}, ошибка: {e}")
        return 0.0


def extract_date(header: str) -> tuple:
    """
    Извлечение даты документа из заголовка CSV-файла.
    Возвращает дату в виде строки и объекта `date`.
    """
    try:
        current_date = header.split(';')[0].split('-')[-1].strip()
        day, month, year = map(int, current_date.split('.'))
        return current_date, date(year, month, day)
    except (ValueError, IndexError) as e:
        logger.error(f"Ошибка извлечения даты из заголовка: {header}. Ошибка: {e}")
        raise CsvFileError("Некорректная дата в шапке CSV-файла.")


def parsing_csv(file) -> Dict[int, TempDict]:
    """
    Основная функция парсинга CSV-файла.
    Обрабатывает файл, извлекает данные и возвращает словарь с обработанными данными.
    """
    try:
        logger.info("Начало парсинга CSV-файла.")
        text = file.readlines()
        for index, row in enumerate(text):
            if row.startswith(COUNTERPARTIES):
                break
        else:
            logger.error(f"В файле отсутствует обязательное поле '{COUNTERPARTIES}'.")
            raise CsvFileError('Неправильный CSV-файл: отсутствует поле "Контрагенты".')

        # Извлечение даты из заголовка
        try:
            tuple_date = extract_date(text[1])
            current_date = tuple_date[0]  # Дата строкой
            format_date = tuple_date[1]  # Дата в формате datetime
            logger.info(f"Дата из заголовка файла успешно извлечена: {format_date}.")
        except CsvFileError as date_error:
            logger.error(f"Ошибка при извлечении даты: {date_error}")
            raise

        # Удаление строк с ненужными заголовками
        text.pop(index + 1)  # Удаление строки со словом "Договоры"
        text.pop(index + 1)  # Удаление строки с общими цифрами

        # Преобразование оставшегося текста в CSV-данные
        fin_text = ''.join(text[index:])
        data = StringIO(fin_text)
        our_dict = csv.DictReader(data, delimiter=';')

        # Инициализация констант и результирующего словаря
        list_of_stop = [TARGETED_FEE, MEMBER_FEE, ELECTRICITY_PAYMENTS, TOTAL, TOTAL_EXPANDED]
        list_of_keys = [CREDIT_FOR + current_date, DEBIT_FOR + current_date]
        res_dict = {}

        # Обработка строк CSV
        temp_dict = None
        for row in our_dict:
            try:
                if row[COUNTERPARTIES].strip() not in list_of_stop:
                    area_number = int(row[COUNTERPARTIES].split('уч.')[-1])
                    temp_dict = gen_temp_dict(format_date)
                    temp_dict['area_number'] = area_number
                    res_dict[area_number] = temp_dict
                    logger.debug(f"Обработан участок {area_number}.")
                elif row[COUNTERPARTIES].strip() == TARGETED_FEE:
                    for key in list_of_keys:
                        temp_dict['targeted_fee'] += string_to_float(row, key)
                elif row[COUNTERPARTIES].strip() == MEMBER_FEE:
                    for key in list_of_keys:
                        temp_dict['member_fee'] += string_to_float(row, key)
                elif row[COUNTERPARTIES].strip() == ELECTRICITY_PAYMENTS:
                    for key in list_of_keys:
                        temp_dict['electricity_payments'] += string_to_float(row, key)
            except KeyError as e:
                logger.warning(f"Пропущена строка из-за отсутствия поля: {e}")
        logger.info(f"Парсинг CSV завершён. Обработано участков: {len(res_dict)}.")
        return res_dict
    except Exception as e:
        logger.error(f"Ошибка во время парсинга CSV-файла: {e}")
        raise CsvFileError("Ошибка обработки CSV-файла.") from e
