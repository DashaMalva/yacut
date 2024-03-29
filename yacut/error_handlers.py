from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    """Класс исключения для API.

    Attributes:
    status_code: статус-код для ответа API
    message: текст сообщения об ошибки, передается при вызове исключения
    """

    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Возвращает словарь с текстом сообщения об ошибке."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def api_usage(error):
    """Обработчик исключения для API.
    Возвращает в ответе текст ошибки в формате JSON и статус-код.
    """
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    """Обработчик ошибки 404."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработчик ошибки 500."""
    db.session.rollback()
    return render_template('500.html'), 500
