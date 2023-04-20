from urllib.parse import urljoin

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validators import (check_short_id, check_required_field,
                         check_short_id_length, is_custom_id_received)
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """API-функция, обрабатывающая POST-запрос на создание короткой ссылки."""
    data = request.get_json()
    check_required_field(data, 'url')
    if not is_custom_id_received(data):
        short_id = get_unique_short_id()
    else:
        short_id = data['custom_id']
        check_short_id(short_id)
    urlmap = URLMap(
        original=data['url'],
        short=short_id
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(
        dict(url=data['url'], short_link=urljoin(request.url_root, short_id))
    ), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """API-функция, обрабатывающая GET-запрос на получение оригинальной ссылки
    по указанному короткому идентификатору.
    """
    check_short_id_length(short_id)
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': urlmap.original}), 200
