from flask import Flask
import os
from app.extensions import init_extensions

from app.blueprints.auth import blueprint as auth
from app.blueprints.control_panels.user_panel.views import blueprint as user_panel
from app.blueprints.control_panels.admin_panel.views import blueprint as admin_panel
from app.blueprints.contacts.views import blueprint as contacts
from app.blueprints.main_page.views import blueprint as main_page


def create_app():
    """ Основная функция проекта. Содержит в себе инициацию Flask-приложения, функции эндпоинты,
        команды инициализации БД, и логин-менеджера в контексте основного приложения."""
    app = Flask(__name__)
    # Конфигурацию конфига в зависимости от окружения
    env = os.getenv("FLASK_ENV", "dev")
    if env == "prod":
        app.config.from_object('app.config.prod')
    elif env == "test":
        app.config.from_object('app.config.test')
    else:
        app.config.from_object('app.config.dev')

    app.register_blueprint(contacts)
    app.register_blueprint(user_panel)
    app.register_blueprint(admin_panel)
    app.register_blueprint(main_page)
    app.register_blueprint(auth)

    init_extensions(app)

    return app
