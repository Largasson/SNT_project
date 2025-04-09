from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions.db import db


class Finance(db.Model):
    __tablename__ = 'financial_data'
    __table_args__ = {'comment': 'Общая финансовая таблица, загружаемая извне в ЛК у админа'}
    id: Mapped[int] = mapped_column(autoincrement=True, nullable=False)
    area_number: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    member_fee: Mapped[int] = mapped_column(nullable=True)
    targeted_fee: Mapped[int] = mapped_column(nullable=True)
    electricity_payments: Mapped[int] = mapped_column(nullable=True)
    published: Mapped[date] = mapped_column(nullable=False)
