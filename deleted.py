from webapp.model import FinancialData
from webapp import create_app, db

app = create_app()
def deleted_finance_data_db():
    with app.app_context():
        info_delete = FinancialData.query.all()
        for item in info_delete:
            db.session.delete(item)
        db.session.commit()