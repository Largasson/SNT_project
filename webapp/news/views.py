from flask import Blueprint, render_template

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    """ Функция, отвечающая за главную страницу. Передает в функцию
            рендеринга макет главной страницы """
    title = 'Главная страница'
    return render_template('news/index.html', page_title=title)
