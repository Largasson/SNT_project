import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    area_number = db.Column(db.Integer, index=True, unique=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), nullable=True)
    # user_finance = relationship("FinancialData", backref='user_table')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'Пользователь с участка {self.area_number} с id={self.id}'

    @property
    def is_admin(self):
        return self.role == 'admin'


# Таблица с новостями на главной странице
class News(db.Model):
    __tablename__ = 'news_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    published: Mapped[datetime.datetime] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return '<News {} {}>'.format(self.id, self.published)


# Общая финансовая таблица, загружаемая извне в ЛК у админа
class FinancialData(db.Model):
    __tablename__ = 'financial_data'
    id: Mapped[int] = mapped_column(autoincrement=True, nullable=False)
    area_number: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    member_fee: Mapped[int] = mapped_column(nullable=True)
    targeted_fee: Mapped[int] = mapped_column(nullable=True)
    electricity_payments: Mapped[int] = mapped_column(nullable=True)
    published = db.Column(Date, nullable=False)
    # user_data = relationship('financial_data_user', back_populates='financial_data', lazy=True)

