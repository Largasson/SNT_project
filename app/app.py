import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
# Иначе запуск из ЭТОГО файла не будет работать
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.extensions.logger import logger
from app.extensions import init_extensions
from app.blueprints.auth import blueprint as auth
from app.blueprints.control_panels.user_panel.views import blueprint as user_panel
from app.blueprints.control_panels.admin_panel.views import blueprint as admin_panel
from app.blueprints.contacts.views import blueprint as contacts
from app.blueprints.main_page.views import blueprint as main_page
from flask import Flask


def create_app() -> Flask:
    """Инициализирует Flask-приложение и его компоненты.

    Главная функция настраивает Flask-приложение, определяя конфигурацию на основе
    окружения, регистрирует blueprints и инициализирует расширения. Она считывает
    переменную окружения ``FLASK_ENV``, чтобы определить, какую конфигурацию загрузить
    (для разработки, тестирования или продакшена). Если переменная окружения не
    установлена, используется конфигурация по умолчанию для разработки.
    В процессе настройки также инициализируются blueprints и расширения Flask.

    :raises Exception: Если возникает ошибка при загрузке конфигурации, регистрации blueprints
                       или инициализации расширений Flask.

    :return: Инициализированный экземпляр приложения Flask
    :rtype: Flask
    """

    logger.info("Инициализация Flask-приложения...")

    app = Flask(__name__)

    # Чтение окружения
    env = os.getenv("FLASK_ENV", "dev")
    logger.info(f"Запуск в среде: {env}")

    try:
        if env == "prod":
            app.config.from_object('app.config.prod')
            logger.info("Загружена конфигурация: Production")
        elif env == "test":
            app.config.from_object('app.config.test')
            logger.info("Загружена конфигурация: Testing")
        else:
            app.config.from_object('app.config.dev')
            logger.info("Загружена конфигурация: Development")
    except Exception as e:
        logger.error(f"Ошибка загрузки конфигурации: {str(e)}")
        app.config.from_object('app.config.dev')

    # Регистрация blueprints
    try:
        app.register_blueprint(contacts)
        logger.debug("Blueprint `contacts` успешно зарегистрирован.")

        app.register_blueprint(user_panel)
        logger.debug("Blueprint `user_panel` успешно зарегистрирован.")

        app.register_blueprint(admin_panel)
        logger.debug("Blueprint `admin_panel` успешно зарегистрирован.")

        app.register_blueprint(main_page)
        logger.debug("Blueprint `main_page` успешно зарегистрирован.")

        app.register_blueprint(auth)
        logger.debug("Blueprint `auth` успешно зарегистрирован.")
    except Exception as e:
        logger.error(f"Ошибка при регистрации blueprints: {str(e)}")
        raise

    # Инициализация расширений
    try:
        init_extensions(app)
        logger.info("Расширения Flask успешно инициализированы.")
    except Exception as e:
        logger.error(f"Ошибка при инициализации расширений: {str(e)}")
        raise

    logger.info("Flask-приложение готово к запуску.")
    return app


if __name__ == "__main__":
    flask_app = create_app()
    port = 8000
    logger.info(f"Запуск приложения на http://localhost:{port}")
    flask_app.run(debug=flask_app.config.get("FLASK_DEBUG", False), port=port)
