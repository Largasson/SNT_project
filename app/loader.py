from app import db
from app.lk.models import FinancialData


def insert_finance_data_db(res_dict):
    deleted_finance_data_db()
    for item in res_dict.values():
        financial_data = FinancialData(id=item['area_number'], area_number=item['area_number'],
                                       member_fee=item['member_fee'], targeted_fee=item['targeted_fee'],
                                       electricity_payments=item['electricity_payments'],
                                       published=item['date'])
        db.session.add(financial_data)
    db.session.commit()


def deleted_finance_data_db():
    info_delete = FinancialData.query.all()
    for item in info_delete:
        db.session.delete(item)
    db.session.commit()
