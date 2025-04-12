from app.extensions.logger import logger
from flask import Blueprint, render_template, flash, redirect, url_for

blueprint = Blueprint('exc_page', __name__)

# Обработчик для ошибки 404
@blueprint.app_errorhandler(404)
def page_not_found(e):
    logger.warning("Ошибка 404: Страница не найдена")
    # Рендер кастомной HTML-страницы ошибки
    return render_template('error.html', error_code=404, error_message="Страница не найдена"), 404


# Обработчик для ошибки 500
@blueprint.app_errorhandler(500)
def internal_server_error(e):
    logger.error("Ошибка 500: Внутренняя ошибка сервера")
    # Рендер кастомной HTML-страницы ошибки
    return render_template('error.html', error_code=500, error_message="Внутренняя ошибка сервера"), 500
