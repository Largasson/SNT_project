
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


from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "POSTGRES"

db = SQLAlchemy(app)

with app.app_context():
    class Personal(db.Model):
        __tablename__ = 'PersonalProfile'
        id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
        email = db.Column(db.String(30), nullable=False)
        user = db.relationship('User', backref='personal', lazy='dynamic')


    class User(db.Model):
        __tablename__ = 'UserProfile'
        id = db.Column(db.Integer, unique=True, autoincrement=True, primary_key=True)
        personal_id = db.Column(db.Integer, db.ForeignKey('PersonalProfile.id'))
        region = db.relationship('Region', backref='user', lazy='dynamic')
        name = db.Column(db.String(30), nullable=False)
        surname = db.Column(db.String(30), nullable=False)
        patronymic = db.Column(db.String(30))
        phone_number = db.Column(db.Text, nullable=True, unique=True)


    class Region(db.Model):
        __tablename__ = 'RegionProfile'
        id = db.Column(db.Integer, unique=True, autoincrement=True, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('UserProfile.id'))
        region_number = db.Column(db.String, unique=True, primary_key=True)
        cadastral_number = db.Column(db.String, unique=True)


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


    db.create_all()
@app.route('/')
def index():
    return render_template('index.html', titte='Главная страница')


@app.route("/registration", methods=("POST", "GET"))
def register():
    if request.method == 'POST':
        # Добавить проверку корректности данных
        try:
            # hash = generate_password_hash(request.form['psw'])  # Добавить поле psw
            ivan_petron_personal = Personal(email='ivanov@ya.ru')
            db.session.add(ivan_petron_personal)
            db.session.flush()

            ivan_petrov = User(personal_id=ivan_petron_personal.id, name='Иван', surname='Иванов',patronymic='Иванович', phone_number='+79005456919')
            db.session.add(ivan_petrov)
            db.session.flush()

            ivan_petrov_region = Region(user_id=ivan_petrov.id, region_number='45',cadastral_number='47:14:1203001:814')
            db.session.add(ivan_petrov_region)

            db.session.commit()
        except:
            db.session.rollback()
            print('Ошибка добавления в БД')

    return render_template('registration.html', title='Зарегистрироваться')





if __name__ == 'main':
    app.run(debug=True)


# print(User.query.all())
#     db.drop_all()
#     db.session.commit()

# print(User.query.all())
# db.drop_all()
# db.session.commit()

