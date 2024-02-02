from flask import Blueprint, render_template

from webapp.news.models import News
from webapp.weather import get_weather

# from logging import basicConfig, info, INFO

# basicConfig(filename='webapp/logs/news_views_log.log', level=INFO, format="%(asctime)s %(levelname)s %(message)s")

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
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

    return render_template('news/index.html', page_title=title,
                           forecast=forecast, condition=condition, news=news)
