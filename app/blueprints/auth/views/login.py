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
        if current_user.is_authenticated:
            # Направляем пользователей в зависимости от их роли
            target_url = url_for('admin_panel.admin_panel') if current_user.is_admin \
                else url_for('user_panel.user_panel', area=current_user.area_number)
            logger.info(f"Пользователь {current_user.area} уже залогинен. Перенаправляем на {target_url}.")
            return redirect(target_url)

        # Рендеринг страницы логина
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login/login.html', page_title=title, form=login_form)
    except Exception as e:
        logger.error(f"Ошибка на странице логина: {str(e)}")
        flash('Произошла ошибка при попытке открыть страницу логина. Повторите позже.')
        return redirect(url_for('exc_page.page_not_found'))


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

    form = LoginForm()

    if not form.validate_on_submit():
        flash('Некорректные данные. Пожалуйста, попробуйте снова.')
        return redirect(url_for('auth.login.login'))

    user = User.query.filter_by(area_number=form.area_number.data).first()

    if not user:
        flash('Пользователь с таким номером участка не зарегистрирован')
        return redirect(url_for('auth.login.login'))

    if not user.check_password(form.password.data):
        flash('Неверный номер участка или пароль')
        return redirect(url_for('auth.login.login'))

    # Авторизация пользователя
    login_user(user, remember=form.remember_me.data)

    # Перенаправление в зависимости от роли
    return redirect(
        url_for('admin_panel.admin_panel') if user.is_admin
        else url_for('user_panel.user_panel', area=user.area_number)
    )
