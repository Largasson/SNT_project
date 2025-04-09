from datetime import datetime
from app.extensions.db import db


class News(db.Model):
    __tablename__ = 'news_table'
    __table_args__ = {'comment': 'Таблица с новостями на главной странице'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    published = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<News {} {}>'.format(self.id, self.published)
