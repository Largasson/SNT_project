from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, PasswordField, TelField, FileField, StringField
from wtforms.validators import Email, DataRequired, EqualTo


class RegistrationForm(FlaskForm):
    area_number = StringField(label='Введите номер участка',
                              validators=[DataRequired(message='Поле не должно быть пустым')],
                              render_kw={'class': 'form-control'})
    email = EmailField(label='Введите e-mail', validators=[Email(message='Некорректный email')],
                       render_kw={'class': 'form-control'})
    phone = TelField(label='Введите номер телефона', validators=[DataRequired(message='Поле не должно быть пустым')],
                     render_kw={'class': 'form-control'})
    password = PasswordField(label='Введите пароль',
                             validators=[DataRequired(), EqualTo('confirm', 'Пороли должны совпадать')],
                             render_kw={'class': 'form-control'})
    confirm = PasswordField(label='Введите пароль еще раз', render_kw={'class': 'form-control'})
    submit = SubmitField(label='Зарегистрироваться', render_kw={'class': 'btn btn-primary w-100 py-2'})


class LoginForm(FlaskForm):
    area_number = StringField(label='Введите номер участка',
                              validators=[DataRequired(message='Поле не должно быть пустым')],
                              render_kw={'class': 'form-control'})
    password = PasswordField(label='Введите пароль', validators=[DataRequired()],
                             render_kw={'class': 'form-control'})
    submit = SubmitField(label='Войти', render_kw={'class': 'btn btn-primary w-100 py-2'})


class UploadFileForm(FlaskForm):
    file = FileField(render_kw={'class': 'form-control'})
    submit = SubmitField(label='Загрузить', render_kw={'class': 'btn btn-info'})
