from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, EmailField, PasswordField, TelField, StringField, IntegerField
from wtforms.validators import Email, DataRequired, EqualTo, NumberRange

# Общие стили для полей форм
COMMON_STYLE = {'class': 'form-control'}
BUTTON_STYLE = {'class': 'btn btn-primary w-100 py-2'}
CHECKBOX_STYLE = {'class': 'form-check-input'}


class RegistrationForm(FlaskForm):
    """Форма регистрации пользователей"""
    area_number = IntegerField(
        label='Введите номер участка',
        validators=[
            NumberRange(message='Номер участка должен быть от 1 до 43', min=1, max=43),
            DataRequired(message='Поле не должно быть пустым'),
        ],
        render_kw=COMMON_STYLE
    )
    email = EmailField(
        label='Введите e-mail',
        validators=[
            Email(message='Некорректный формат email, проверьте правильность ввода'),
            DataRequired(message='Поле e-mail не должно быть пустым'),
        ],
        render_kw=COMMON_STYLE,
    )
    phone = TelField(
        label='Введите номер телефона',
        validators=[DataRequired(message='Поле не должно быть пустым')],
        render_kw=COMMON_STYLE,
    )
    password = PasswordField(
        label='Введите пароль',
        validators=[
            DataRequired(message='Пароль обязателен'),
            EqualTo('confirm', 'Пароли должны совпадать'),
        ],
        render_kw=COMMON_STYLE,
    )
    confirm = PasswordField(
        label='Введите пароль еще раз',
        render_kw=COMMON_STYLE,
    )
    submit = SubmitField(label='Зарегистрироваться', render_kw=BUTTON_STYLE)


class LoginForm(FlaskForm):
    """Форма авторизации пользователей"""

    area_number = StringField(
        label='Введите номер участка',
        validators=[DataRequired(message='Поле не должно быть пустым')],
        render_kw=COMMON_STYLE,
    )
    password = PasswordField(
        label='Введите пароль',
        validators=[DataRequired(message='Необходимо ввести пароль')],
        render_kw=COMMON_STYLE,
    )
    remember_me = BooleanField(label='Запомнить меня', default=True, render_kw=CHECKBOX_STYLE)
    submit = SubmitField(label='Войти', render_kw=BUTTON_STYLE)
