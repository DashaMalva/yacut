from datetime import datetime

from yacut import db


class URLMap(db.Model):
    """Класс для связи длинных и коротких ссылок.

    Fields:
    id (добавляется автоматически): первичный ключ
    original (обязательное поле): оригинальная длинная ссылка
    short (обязательное поле): относительная короткая ссылка / идентификатор
    timestamp (добавляется автоматически): временная метка
    """

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
