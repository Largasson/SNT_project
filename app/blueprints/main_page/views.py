from flask import Blueprint, render_template

from app.models.news import News
from app.services.weather import get_weather

blueprint = Blueprint('main_page', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def main_page():
    """ Функция, отвечающая за главную страницу. Передает в функцию
            рендеринга макет главной страницы, информацию по погоде """
    title = 'Главная страница'
    news = None
    forecast, condition = None, None
    try:
        news = News.query.all()
    except (TypeError, ValueError) as err:
        temp = err
        # info(err)
    try:
        forecast, condition = get_weather()
    except (TypeError, ValueError) as err:
        temp = err
        # info(err)

    return render_template('main_page/main_page.html', page_title=title,
                           forecast=forecast, condition=condition, news=news)
