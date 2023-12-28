from webapp import create_app, db
from model import FinancialData
# from webapp.deleted import deleted_finance_data_db
from parsing_csv import parsing_csv


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


if __name__ == '__main__':
    app = create_app()
    try:
        with open('test-1.csv', 'r', encoding='cp1251') as file:
            res_dict = parsing_csv(file)
    except FileNotFoundError:
        print('Файл не найден')
    with app.app_context():
        insert_finance_data_db(res_dict)
