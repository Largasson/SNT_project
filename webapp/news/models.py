from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from webapp.db import db


class News(db.Model):
    __tablename__ = 'news_table'
    __table_args__ = {'comment': 'Таблица с новостями на главной странице'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    published = Column(DateTime, nullable=False, default=datetime.utcnow)
    title = Column(String, nullable=True)
    text = Column(String, nullable=True)

    def __repr__(self):
        return '<News {} {}>'.format(self.id, self.published)
