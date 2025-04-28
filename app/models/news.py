import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions.db import db


class News(db.Model):
    """Класс для представления модели новостей.

    Модель используется для хранения и отображения новостей,
    которые видны пользователям на главной странице приложения.
    Новости добавляются в админ-панели.

    Атрибуты:
        id (int): Уникальный идентификатор новости.
        published (datetime): Дата и время публикации.
        title (str): Заголовок новости.
        text (str): Полный текст новости.
    """

    __tablename__ = 'news'
    __table_args__ = {'comment': 'Таблица с новостями на главной странице'}

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="Уникальный идентификатор записи новости",
    )
    published: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.UTC),
        comment="Дата и время публикации",
    )
    title: Mapped[str] = mapped_column(
        nullable=False,
        comment="Заголовок новости",
    )
    text: Mapped[str] = mapped_column(
        nullable=True,
        comment="Полный текст новости",
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта News."""
        return f"<News id={self.id}, title={self.title}, published={self.published}>"
