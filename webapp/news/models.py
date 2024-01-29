from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from webapp.db import db


class News(db.Model):
    __tablename__ = 'news_table'
    __table_args__ = {'comment': 'Таблица с новостями на главной странице'}
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    published: Mapped[datetime] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return '<News {} {}>'.format(self.id, self.published)
