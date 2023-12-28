# from webapp.model import FinancialData
# from webapp import create_app, db
#
#
# def deleted_finance_data_db():
#     info_delete = FinancialData.query.all()
#     for item in info_delete:
#         db.session.delete(item)
#     db.session.commit()
#
#
# if __name__ == '__main__':
#     app = create_app()
#     with app.app_context():
#         deleted_finance_data_db()
