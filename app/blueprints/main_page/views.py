from flask import Blueprint, render_template
from app.extensions.logger import logger
from app.models.news import News
from app.services.weather import get_weather

# Создание blueprint для главной страницы
blueprint = Blueprint('main_page', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def main_page():
    """
    Генерация главной страницы.
    Передаёт в шаблон информацию о погоде и новостях.
    """
    title = 'Главная страница'
    forecast, condition, news = None, None, None

    try:
        # Получение списка новостей
        news = News.query.all()
        if not news:
            logger.warning("Новости не найдены.")
        else:
            logger.info(f"Загружено {len(news)} новостей.")
    except Exception as err:
        logger.error(f"Ошибка при запросе списка новостей: {err}")

    try:
        # Получение данных о погоде
        forecast, condition = get_weather()
        logger.info("Данные о погоде успешно загружены.")
    except Exception as err:
        logger.error(f"Ошибка при получении данных о погоде: {err}")

    try:
        # Рендеринг страницы
        return render_template(
            'main_page/main_page.html',
            page_title=title,
            forecast=forecast,
            condition=condition,
            news=news
        )
    except Exception as err:
        logger.error(f"Ошибка во время рендеринга главной страницы: {err}")
        return render_template('error.html', page_title='Ошибка'), 500
