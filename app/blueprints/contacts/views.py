from flask import Blueprint, render_template
from app.extensions.logger import logger

blueprint = Blueprint('contacts', __name__)


@blueprint.route('/contacts')
def contacts():
    """Функция отображения страницы контактов."""
    title = 'Контакты'
    logger.info('Запрос на страницу контактов выполнен')  # Логируем успешный запрос

    try:
        # Отображение страницы с использованием шаблона
        return render_template('contacts/contacts.html', page_title=title)
    except Exception as e:
        # Логируем ошибку при попытке отобразить контакты
        logger.error(f'Ошибка при отображении страницы контактов: {str(e)}')
        return render_template('error.html', page_title='Ошибка'), 500
