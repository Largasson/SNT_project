from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

# ************ Обязательные переменные приложения ************
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("Переменная окружения SECRET_KEY не задана или пуста.")

WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')
if not WTF_CSRF_SECRET_KEY:
    raise ValueError("Переменная окружения WTF_CSRF_SECRET_KEY не задана или пуста.")

# ************ Общие настройки приложения ************
BASE_DIR = Path(__file__).resolve().parent  # Текущая директория файла
PARENT_DIR = BASE_DIR.parent  # Родительская директория
SQLALCHEMY_DATABASE_URI = f"sqlite:///{PARENT_DIR / 'app.db'}"

REMEMBER_COOKIE_DURATION = timedelta(days=30)
FLASK_DEBUG = os.getenv('FLASK_DEBUG')
LOG_FORMAT = os.getenv('LOG_FORMAT')

# ************ Константы для парсинга ************
PARSING_CONSTANTS = {
    'TARGETED_FEE': 'Целевые взносы',
    'MEMBER_FEE': 'Членские взносы',
    'ELECTRICITY_PAYMENTS': 'Электроэнергия',
    'TOTAL': 'Итого',
    'TOTAL_EXPANDED': 'Итого развернутое',
    'COUNTERPARTIES': 'Контрагенты',
    'CREDIT_FOR': 'кредит на ',
    'DEBIT_FOR': 'дебет на ',
}

# ************ Конфигурация погоды ************
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

WEATHER_SETTINGS = {
    'URL': "https://api.weather.yandex.ru/v2/forecast",
    'API_KEY': WEATHER_API_KEY,
    'LATITUDE': "55.066318",
    'LONGITUDE': "37.995591",
}
