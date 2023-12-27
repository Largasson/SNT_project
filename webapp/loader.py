from webapp import create_app, db
from model import FinancialData
from parsing_csv import parsing_csv

app = create_app()

my_list = []


def save_data(filename):
    with app.app_context():
        with open(filename, 'r', encoding='cp1251') as file:
            res_dict = parsing_csv(file)
            for row in res_dict.items():
                my_list.append(row[1])
                # print(row)
            for item in my_list:
                financial_data = FinancialData(id=item['area_number'], area_number=item['area_number'],
                                               member_fee=item['member_fee'], targeted_fee=item['targeted_fee'],
                                               electricity_payments=item['electricity_payments'],
                                               published=item['date'])
                db.session.add(financial_data)
                db.session.commit()


if __name__ == '__main__':
    save_data('test-1.csv')
