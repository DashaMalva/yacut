import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional, URL,
                                ValidationError)

from settings import (CUSTOM_ID_PATTERN, MAX_CUSTOM_ID_LENGTH,
                      MAX_ORIGINAL_LINK_LENGHT)


class URLMapForm(FlaskForm):
    """Класс формы для добавления длинных и коротких ссылок в БД.

    Fields:
    original_link (обязательное поле): оригинальная длинная ссылка
    custom_id (необязательное поле): пользовательский вариант короткой ссылки
    submit: кнопка для отправки формы

    Methods:
    validate_custom_id(): проверяет содержимое короткой ссылки
    """

    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, MAX_ORIGINAL_LINK_LENGHT),
                    URL(message='Некорректная ссылка')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, MAX_CUSTOM_ID_LENGTH,
                   message=f'Максимальная длина: {MAX_CUSTOM_ID_LENGTH}'),
            Optional()]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, field):
        if re.fullmatch(CUSTOM_ID_PATTERN, field.data) is None:
            raise ValidationError(
                'Указано недопустимое имя для короткой ссылки')
