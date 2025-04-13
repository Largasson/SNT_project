from flask import Blueprint, render_template, flash, redirect, url_for
from app.blueprints.auth.forms import RegistrationForm
from app.extensions.db import db
from app.extensions.logger import logger
from app.models import User


blueprint = Blueprint('registration', __name__)


def flash_and_redirect(message: str,
                       endpoint: str = 'auth.registration.registration'):
    """
    Выводит сообщение об ошибке и
    перенаправляет на страницу регистрации.
    """
    flash(message)
    logger.info(f'Перенаправление на {endpoint} с сообщением: {message}')
    return redirect(url_for(endpoint))


@blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    """Функция, отвечающая за страницу регистрации"""
    try:
        logger.info('Открыта страница регистрации')
        title = 'Регистрация'
        registration_form = RegistrationForm()
        return render_template('login/registration.html', page_title=title, form=registration_form)
    except Exception as e:
        # Логируем ошибку при обработке страницы регистрации
        logger.error(f'Ошибка при отображении страницы регистрации: {str(e)}')
        return render_template('error.html', page_title='Ошибка'), 500


@blueprint.route('/reg_processing', methods=['POST'])
def reg_processing():
    """
    Обработка данных, отправленных с формы регистрации. Если данные валидны,
    то пользователь добавляется в базу данных. В противном случае
    перенаправляется обратно с отображением ошибок.
    """
    try:
        logger.info('Начата обработка данных регистрации')
        form = RegistrationForm()

        if not form.validate_on_submit():
            # Если форма не проходит валидацию, то отображаем ошибку
            error_message = ', '.join([''.join(err_value).lower() for err_value in form.errors.values()])
            logger.warning(f'Данные не прошли валидацию: {error_message}')  # Лог ошибки валидации
            return flash_and_redirect(message=f'Введены некорректные данные: {error_message}')

        # Проверяем, существует ли пользователь с таким номером участка
        logger.info(f'Проверка пользователя с номером участка: {form.area_number.data}')
        user_with_area = User.query.filter_by(area_number=form.area_number.data).first()
        if user_with_area:
            logger.warning(
                f'Пользователь с номером участка {form.area_number.data} уже зарегистрирован')
            return flash_and_redirect(message=f'Пользователь с таким номером участка уже зарегистрирован')

        # Добавляем нового пользователя
        new_user = User(
            area_number=form.area_number.data,
            email=form.email.data,
            phone=form.phone.data,
            role='user',
        )
        new_user.set_password(form.password.data)
        logger.info(f'Создаётся новый пользователь с email {form.email.data}')

        try:
            db.session.add(new_user)
            db.session.commit()
            logger.info(f'Пользователь {form.email.data} успешно добавлен в базу данных')
        except Exception as e:
            db.session.rollback()  # Откат изменений
            logger.error(f'Ошибка при сохранении нового пользователя: {str(e)}')
            return flash_and_redirect(message=f'Ошибка при сохранении данных: {str(e)}')

        flash('Вы успешно зарегистрированы', 'success')
        logger.info(f'Пользователь {form.email.data} успешно зарегистрирован')
        return redirect(url_for('auth.login.login'))

    except Exception as e:
        # Логируем ошибку во время обработки данных регистрации
        logger.error(f'Ошибка при обработке данных регистрации: {str(e)}')
        return render_template('error.html', page_title='Ошибка'), 500

