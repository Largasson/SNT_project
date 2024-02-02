from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# общие переменные для приложения
SECRET_KEY = os.getenv('SECRET_KEY')
WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'webapp.db')
REMEMBER_COOKIE_DURATION = timedelta(days=30)

# Константы для функции парсинга
TARGETED_FEE = 'Целевые взносы'
MEMBER_FEE = 'Членские взносы'
ELECTRICITY_PAYMENTS = 'Электроэнергия'
TOTAL = 'Итого'
TOTAL_EXPANDED = 'Итого развернутое'
COUNTERPARTIES = 'Контрагенты'
CREDIT_FOR = 'кредит на '
DEBIY_FOR = 'дебет на '

# Константы для сервиса погоды
WEATHER_URL = "https://api.weather.yandex.ru/v2/forecast"
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

LATITUDE = "55.066318"
LONGITUDE = "37.995591"
