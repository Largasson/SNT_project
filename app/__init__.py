from flask import Flask
from flask_login import LoginManager

from app.db import db

from app.blueprints.auth.models import User
from app.blueprints.auth.forms import LoginForm







from app.blueprints.control_panels.admin_panel.models import FinancialData

from app.blueprints.auth import blueprint as auth
from app.blueprints.control_panels.user_panel.views import blueprint as user_panel
from app.blueprints.control_panels.admin_panel.views import blueprint as admin_panel
from app.blueprints.contacts.views import blueprint as contacts
from app.blueprints.news.views import blueprint as news


def create_app():
    """ Основная функция проекта. Содержит в себе инициацию Flask-приложения, функции эндпоинты,
        команды инициализации БД, и логин-менеджера в контексте основного приложения."""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(contacts)
    app.register_blueprint(user_panel)
    app.register_blueprint(admin_panel)
    app.register_blueprint(news)
    app.register_blueprint(auth)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
