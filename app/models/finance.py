import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions.db import db


class Finance(db.Model):
    """Модель для хранения финансовых данных.

    Данные загружаются администратором в личные кабинеты пользователей
    через админ-панель.

    Атрибуты:
        id (int): Уникальный идентификатор записи.
        area_number (int): Номер участка (уникальный для каждой записи).
        member_fee (int): Баланс участка по членским взносам.
        targeted_fee (int): Баланс участка по целевым взносам.
        electricity_payments (int): Баланс участка за электроэнергию.
        published (date): Дата публикации данных.
    """

    __tablename__ = 'finance'
    __table_args__ = {'comment': 'Общая финансовая таблица, загружаемая извне в ЛК пользователей в админ-панели'}

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        nullable=False,
        primary_key=True,
        comment="Уникальный идентификатор записи",
    )
    area_number: Mapped[int] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
        comment="Идентификатор участка",
    )
    member_fee: Mapped[int] = mapped_column(
        nullable=True,
        default=0,
        comment="Баланс участка по членским взносам",
    )
    targeted_fee: Mapped[int] = mapped_column(
        nullable=True,
        default=0,
        comment="Баланс участка по целевым взносам",
    )
    electricity_payments: Mapped[int] = mapped_column(
        nullable=True,
        default=0,
        comment="Баланс участка за электроэнергию",
    )
    published: Mapped[datetime.date] = mapped_column(
        nullable=False,
        comment="Дата публикации финансовых данных",
    )
