from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, EmailField, PasswordField, TelField, StringField, IntegerField
from wtforms.validators import Email, DataRequired, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    area_number = IntegerField(label='Введите номер участка',
                               validators=[NumberRange(message='Номер участка должен быть от 1 до 43', min=1, max=43),
                                           DataRequired(message='Поле не должно быть пустым')],
                               render_kw={'class': 'form-control'})
    # area_number = StringField(label='Введите номер участка',
    #                           validators=[DataRequired(message='Поле не должно быть пустым')],
    #                           render_kw={'class': 'form-control'})
    email = EmailField(label='Введите e-mail', validators=[Email(message='Некорректный email')],
                       render_kw={'class': 'form-control'})
    phone = TelField(label='Введите номер телефона', validators=[DataRequired(message='Поле не должно быть пустым')],
                     render_kw={'class': 'form-control'})
    password = PasswordField(label='Введите пароль',
                             validators=[DataRequired(), EqualTo('confirm', 'Пароли должны совпадать')],
                             render_kw={'class': 'form-control'})
    confirm = PasswordField(label='Введите пароль еще раз', render_kw={'class': 'form-control'})
    submit = SubmitField(label='Зарегистрироваться', render_kw={'class': 'btn btn-primary w-100 py-2'})


class LoginForm(FlaskForm):
    area_number = StringField(label='Введите номер участка',
                              validators=[DataRequired(message='Поле не должно быть пустым')],
                              render_kw={'class': 'form-control'})
    password = PasswordField(label='Введите пароль', validators=[DataRequired()],
                             render_kw={'class': 'form-control'})
    remember_me = BooleanField(label='Запомнить меня', default=True,
                               render_kw={'class': 'form-check-input'})
    submit = SubmitField(label='Войти', render_kw={'class': 'btn btn-primary w-100 py-2'})
