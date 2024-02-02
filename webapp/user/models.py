from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.db import db


class User(db.Model, UserMixin):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    area_number = db.Column(db.Integer, index=True, unique=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'Пользователь с участка {self.area_number} с id={self.id}'

    @property
    def is_admin(self):
        return self.role == 'admin'
