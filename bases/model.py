from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://snt:qwerty123456@176.113.83.24/exmple'

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
# db.drop_all()
# db.session.commit()
