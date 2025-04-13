from app.blueprints.auth.forms import LoginForm
from app.extensions.logger import logger
from app.models.user import User
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user

blueprint = Blueprint('login', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ручка для обработки запросов на странице логина.

    Если пользователь уже залогинен, перенаправляет на:
        - панель администратора, если это админ.
        - пользовательскую панель, если это обычный пользователь.
    Если нет:
        - Рендерит страницу логина с формой авторизации.
    """
    try:
        logger.info('Открыта страница логина')  # Логируем открытие страницы

        if current_user.is_authenticated:
            # Перенаправляем пользователей в зависимости от их роли
            target_url = url_for('admin_panel.admin_panel') if current_user.is_admin \
                else url_for('user_panel.user_panel', area=current_user.area_number)

            logger.info(f"Пользователь {current_user.area_number} уже залогинен. Перенаправляем на {target_url}.")
            return redirect(target_url)

        # Рендеринг страницы логина
        logger.info('Пользователь не авторизован. Отображается форма логина.')
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login/login.html', page_title=title, form=login_form)

    except Exception as e:
        # Логируем ошибку при попытке отобразить страницу логина
        logger.error(f'Ошибка при отображении страницы логина: {str(e)}')
        return render_template('error.html', page_title='Ошибка'), 500


@blueprint.route('/process_login', methods=['POST'])
def process_login():
    """
    Ручка для обработки данных логина.

    Проверяет:
        - Прошли ли данные валидацию.
        - Существует ли пользователь в БД.
        - Совпадает ли пароль.
    В случае успеха: перенаправляет в нужную панель (админскую или пользовательскую).
    Если что-то пошло не так: возвращает на страницу логина с соответствующими сообщениями.
    """
    try:
        logger.info('Началась обработка данных логина.')  # Лог начала обработки
        form = LoginForm()

        # Проверка валидности формы
        if not form.validate_on_submit():
            logger.warning('Данные не прошли валидацию.')  # Лог ошибки валидации
            flash('Некорректные данные. Пожалуйста, попробуйте снова.')
            return redirect(url_for('auth.login.login'))

        # Проверка наличия пользователя в базе данных
        logger.info(f"Ищем пользователя с номером участка: {form.area_number.data}")
        user = User.query.filter_by(area_number=form.area_number.data).first()

        if not user:
            logger.warning(
                f"Пользователь с номером участка {form.area_number.data} не зарегистрирован.")  # Лог отсутствия пользователя
            flash('Пользователь с таким номером участка не зарегистрирован')
            return redirect(url_for('auth.login.login'))

        # Проверка правильности пароля
        logger.info(f"Проверяем пароль для пользователя с номером участка: {user.area_number}")
        if not user.check_password(form.password.data):
            logger.warning(
                f"Ошибка авторизации: неверный пароль для пользователя {user.area_number}.")  # Лог неверного пароля
            flash('Неверный номер участка или пароль')
            return redirect(url_for('auth.login.login'))

        # Авторизация пользователя
        login_user(user, remember=form.remember_me.data)
        logger.info(f"Пользователь {user.area_number} успешно авторизован.")  # Лог успешной авторизации

        # Перенаправление в зависимости от роли
        target_url = url_for('admin_panel.admin_panel') if user.is_admin \
            else url_for('user_panel.user_panel', area=user.area_number)
        logger.info(f"Пользователь {user.area_number} перенаправлен на {target_url}.")  # Лог перенаправления
        return redirect(target_url)

    except Exception as e:
        # Логируем ошибку при обработке данных логина
        logger.error(f'Ошибка при обработке логина: {str(e)}')
        return render_template('error.html', page_title='Ошибка'), 500
