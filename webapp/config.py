import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')
TARGETED_FEE = 'Целевые взносы'
MEMBER_FEE = 'Членские взносы'
ELECTRICITY_PAYMENTS = 'Электроэнергия'
TOTAL = 'Итого'
TOTAL_EXPANDED = 'Итого развернутое'
COUNTERPARTIES = 'Контрагенты'
CREDIT_FOR = 'кредит на '
DEBIY_FOR = 'дебет на '