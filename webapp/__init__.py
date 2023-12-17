from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import Form, SubmitField, StringField, PasswordField, validators
from wtforms.validators import DataRequired
import io
from webapp.parsing_csv import parsing_csv
from webapp.config import SECRET_KEY, WTF_CSRF_SECRET_KEY


class User:
    def __init__(self, area_number, email, phone, password):
        self.area_number = area_number
        self.email = email
        self.phone = phone
        self.password = password

    def __repr__(self):
        return f"{self.area_number} - (({self.email})({self.phone})({self.password}))"


def create_app():
    class UploadFileForm(FlaskForm):
        file = FileField(render_kw={'class': 'form-control'})
        submit = SubmitField(label='Загрузить', render_kw={'class': 'btn btn-info'})

    class RegistrationForm(Form):
        area = StringField(render_kw={
                                    'class': 'form-control',
                                    'type': 'area',
                                    'placeholder': '12'
                                    }, validators=[validators.Length(min=1, max=2)])
        email = StringField(render_kw={
                                    'class': 'form-control',
                                    'type': 'text',
                                    'placeholder': 'name@example.com'
                                        }, validators=[DataRequired()])
        phone = StringField(render_kw={
                                    'class': 'form-control',
                                    'type': 'text',
                                    'placeholder': '89262521235'
                                         }, validators=[validators.Length(min=10, max=10)])
        password1 = PasswordField(render_kw={
                                    'class': 'form-control',
                                    'type': 'password1',
                                    'placeholder': 'Password'
                                            }, validators=[
                                                        DataRequired(),
                                                        validators.EqualTo('password',
                                                                           message='Passwords must match')
                                                         ])
        password = PasswordField(render_kw={
                                        'class': 'form-control',
                                        'type': 'password',
                                        'placeholder': 'Password'
                                            })
        submit = SubmitField(label='Зарегистрироваться', render_kw={'class': 'btn btn-primary w-100 py-2'})

    class LoginForm(FlaskForm):
        area = StringField('area_number')
        password = PasswordField('Password')
        submit = SubmitField('Submit')

    app = Flask(__name__)

    app.config.update(dict(
        SECRET_KEY=SECRET_KEY,
        WTF_CSRF_SECRET_KEY=WTF_CSRF_SECRET_KEY
    ))

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    @app.route('/log_in', methods=['GET', 'POST'])
    def log_in():
        # if current_user.is_authenticated:
        #     return redirect(url_for('index'))
        form = LoginForm()
        # if form.validate_on_submit():
        #     user = form.area.data
        #     if user is None or not user.check_password(form.password.data):
        #         flash('Invalid username or password')
        #         return redirect(url_for('login'))
        #     login_user(user, remember=form.remember_me.data)
        #     return redirect(url_for('index'))
        # return render_template('login.html', title='Sign In', form=form)
        #


        return render_template('log_in.html')

    @app.route('/registration', methods=['GET', 'POST'])
    def registration():
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            user = User(form.area.data,
                        form.email.data,
                        form.phone.data,
                        form.password1.data)
            print(user)
            return redirect(url_for('log_in'))
        return render_template('registration.html', form=form)

    @app.route('/board_office', methods=['GET', 'POST'])
    def board_office():
        form = UploadFileForm()
        if form.validate_on_submit():
            f = form.file.data
            text_from_csv = f.read().decode('cp1251')
            data = io.StringIO(text_from_csv)
            our_dict = parsing_csv(data)
            key_sort = list(sorted(our_dict))
            for k in key_sort:
                print(f'КЛЮЧ {k}: {our_dict[k]}')
            return render_template('board_office.html', a=form)
        return render_template('board_office.html', a=form)

    @app.route('/lk_page')
    def lk_page():
        return render_template('lk_page.html')

    return app
