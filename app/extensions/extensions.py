from flask import Flask
from flask_migrate import Migrate

from . import logger
from .db import db
from .login_manager import login_manager
from app.models import User

migrate = Migrate()


def init_extensions(app: Flask) -> None:
    """Инициирует расширения приложения Flask.

    Эта функция добавляет в приложение поддержку базы данных,
    миграций и управления сеансами пользователей.

    :param app: Экземпляр Flask-приложения, в который добавляются расширения.
    :type app: Flask
    :return: None
    :rtype: None

    Функция выполняет следующие действия:
    1. Инициализирует подключение базы данных (Flask-SQLAlchemy) к приложению.
    2. Настраивает миграции базы данных (Flask-Migrate).
    3. Настраивает менеджер сеансов пользователей (Flask-Login), включая указание
       маршрута для входа по умолчанию и загрузку данных пользователя по его ID.
    """

    # Инициализация базы данных с приложением
    db.init_app(app)

    # Инициализация миграций
    migrate.init_app(app, db)

    # Инициализация менеджера входа в систему
    login_manager.init_app(app)
    login_manager.login_view = "auth.login.login"

    # Загрузка данных пользователя
    @login_manager.user_loader
    def load_user(user_id):
        """Загружает пользователя.

        Загружает объект пользователя из базы данных по его уникальному идентификатору.

        :param user_id: Уникальный идентификатор пользователя в базе данных.
        :type user_id: str
        :return: Объект пользователя или None, если пользователь не найден или произошла ошибка.
        :rtype: User | None

        Обработчик используется Flask-Login для автоматической загрузки данных о текущем
        пользователе на основе его сессии. В случае возникновения ошибки логируется сообщение
        об ошибке с использованием стандартного механизма логирования приложения.
        """

        try:
            return User.query.get(user_id)
        except Exception as e:
            logger.error(f"Ошибка загрузки пользователя: {e}")
            return None
