from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db


class User(db.Model, UserMixin):
    """Класс модели пользователя.

    Хранит данные о пользователе, его идентификаторе, номере участка,
    адресе электронной почты, номере телефона, пароле и роли.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        area_number (int): Номер участка пользователя, уникальное значение.
        email (str): Адрес электронной почты пользователя.
        phone (str | None): Номер телефона пользователя (опционально).
        password (str): Хэшированный пароль пользователя.
        role (str | None): Роль пользователя в системе, например, "admin" или "user".
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        nullable=False,
        primary_key=True,
        comment="Уникальный идентификатор пользователя",
    )
    area_number: Mapped[int] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
        comment="Уникальный номер участка",
    )
    email: Mapped[str] = mapped_column(
        nullable=False,
        comment="Адрес электронной почты пользователя",
    )
    password: Mapped[str] = mapped_column(
        nullable=False,
        comment="Хэшированный пароль пользователя",
    )
    role: Mapped[str | None] = mapped_column(
        nullable=True,
        comment="Роль пользователя (например, 'admin' или 'user')",
    )

    def set_password(self, password: str) -> None:
        """Устанавливает хэшированный пароль пользователя."""
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Проверяет, соответствует ли переданный пароль его хэшу."""
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта User."""
        return f"Пользователь с участка {self.area_number} с id={self.id}"

    @property
    def is_admin(self) -> bool:
        """Проверяет, является ли пользователь администратором."""
        return self.role == "admin"
