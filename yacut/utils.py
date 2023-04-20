from random import choices

from settings import ALLOWED_CHARACTERS, DEFAULT_SHORT_ID_LENGTH
from .models import URLMap


def is_unique_short_id(short_id: str) -> bool:
    """Проверяет, что объекта с таким идентификатором не существует в БД."""
    return URLMap.query.filter_by(short=short_id).first() is None


def get_unique_short_id() -> str:
    """Возвращает уникальную последовательность из латинских букв и цифр."""
    sequence = ''.join(choices(ALLOWED_CHARACTERS, k=DEFAULT_SHORT_ID_LENGTH))
    if is_unique_short_id(sequence):
        return sequence
    return get_unique_short_id()
