from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template
from app import app, db


with app.app_context():

    class RegistrationForm(db.Model):
        __tablename__ = 'registration_form'
        __table_args__ = {'extend_existing': True}
        id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, unique=True)
        email: Mapped[str] = mapped_column(nullable=True, unique=True)
        phone_number: Mapped[str] = mapped_column(nullable=True, unique=True)
        psw: Mapped[str] = mapped_column(db.Text, unique=True)
        administration_table = db.relationship('AdministrationTable', backref='RegistrationForm', lazy='dynamic')
        financial_table = db.relationship('AdministrationTable', backref='RegistrationForm', lazy='dynamic')


    class AdministrationTable(db.Model):
        __tablename__ = 'administration_table'
        __table_args__ = {'extend_existing': True}
        id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True)
        user_id: Mapped[int] = mapped_column(db.ForeignKey(RegistrationForm.id))
        email: Mapped[str] = mapped_column(nullable=False)
        cadastral_number: Mapped[str] = mapped_column(unique=True)
        name: Mapped[str] = mapped_column(nullable=False)
        patronymic: Mapped[str] = mapped_column()
        target_contribution: Mapped[int] = mapped_column()
        membership_fee: Mapped[int] = mapped_column()


    class FinancialTable(db.Model):
        __tablename__ = 'financial_table'
        id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True)
        user_id: Mapped[int] = mapped_column(db.ForeignKey(RegistrationForm.id))
        phone_number: Mapped[str] = mapped_column(nullable=True, unique=True)
        target_contribution: Mapped[int] = mapped_column()
        membership_fee: Mapped[int] = mapped_column()


        def __repr__(self):
            return '<User {} {} {}>'.format(self.name, self.surname, self.region_number)

    db.create_all()



# @app.route('/')
# def index():
#     return render_template('index.html', titte='Главная страница')


# @app.route("/registration", methods=("POST", "GET"))
# def register():
# if request.method == 'POST':
# Добавить проверку корректности данных
# try:
# hash = generate_password_hash(request.form['psw'])  # Добавить поле psw
# ivan_petron_personal = Personal(email='ivanov@ya.ru')
# db.session.add(ivan_petron_personal)
# db.session.flush()
# db.session.commit()
# except:
#     db.session.rollback()
#     print('Ошибка добавления в БД')

# return render_template('registration.html', title='Зарегистрироваться')


if __name__ == 'main':
    app.run(debug=True)

# print(User.query.all())
#     db.drop_all()
#     db.session.commit()
