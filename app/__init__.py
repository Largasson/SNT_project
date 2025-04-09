from flask import Flask
from flask_login import LoginManager

from app.db import db

from app.user.models import User
from app.user.forms import LoginForm
from app.user.views import blueprint as user_blueprint

from app.lk.models import FinancialData
from app.lk.views import blueprint as lk_blueprint

from app.blueprints.contacts.views import blueprint as contacts_blueprint

from app.blueprints.news.views import blueprint as news_blueprint


def create_app():
    """ Основная функция проекта. Содержит в себе инициацию Flask-приложения, функции эндпоинты,
        команды инициализации БД, и логин-менеджера в контексте основного приложения."""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(contacts_blueprint)
    app.register_blueprint(lk_blueprint)
    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
