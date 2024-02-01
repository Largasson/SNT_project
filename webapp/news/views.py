from flask import Blueprint, render_template

from webapp.news.models import News
from webapp.weather import get_weather, translate_weather_condition

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    """ Функция, отвечающая за главную страницу. Передает в функцию
            рендеринга макет главной страницы, информацию по погоде """
    title = 'Главная страница'
    news = News.query.all()
    print(news)
    # try:
    #     news = News.query.all()
    # except ValueError:
    #     print('нет новостей')
    #     news = []

    today_forecast, tomorrow_forecast, weekend_forecast = get_weather()
    today_condition = translate_weather_condition(today_forecast['condition']).capitalize()
    tomorrow_condition = translate_weather_condition(tomorrow_forecast['condition']).capitalize()
    weekend_condition = translate_weather_condition(weekend_forecast['condition']).capitalize()


    return render_template('news/index.html', page_title=title, today_forecast=today_forecast,
                           tomorrow_forecast=tomorrow_forecast, weekend_forecast=weekend_forecast,
                           today_condition=today_condition, tomorrow_condition=tomorrow_condition,
                           weekend_condition=weekend_condition, news=news)
