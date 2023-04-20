from settings import ALLOWED_CHARACTERS, MAX_CUSTOM_ID_LENGTH
from .error_handlers import InvalidAPIUsage
from .utils import is_unique_short_id


def check_required_field(api_data: dict, required_field: str):
    """Вызывает исключение если в запросе отсутствует обязательное поле."""
    if api_data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if required_field not in api_data:
        raise InvalidAPIUsage(
            f'"{required_field}" является обязательным полем!')


def is_custom_id_received(data: dict) -> bool:
    """Проверяет, передан ли в запросе идентификатор."""
    blank_values = ['None', '']
    custom_id = data.get('custom_id')
    return custom_id is not None and custom_id not in blank_values


def check_short_id_length(short_id: str):
    """Вызывает исключение, если идентификатор недопустимой длины."""
    if len(short_id) < 0 or len(short_id) > MAX_CUSTOM_ID_LENGTH:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки')


def check_short_id_characters(short_id: str):
    """Вызывает исключение, если в идентификаторе есть недопустимые символы."""
    for character in short_id:
        if character not in ALLOWED_CHARACTERS:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')


def check_short_id_uniqueness(short_id: str):
    """Вызывает исключение, если идентификатор неуникален."""
    if not is_unique_short_id(short_id):
        raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')


def check_short_id(short_id: str):
    """Запускает проверки переданного пользователем идентификатора."""
    check_short_id_length(short_id)
    check_short_id_characters(short_id)
    check_short_id_uniqueness(short_id)
