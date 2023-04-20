from urllib.parse import urljoin

from flask import abort, flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id, is_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница с формой для получения короткой ссылки."""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    if custom_id is None or custom_id == 'None':
        custom_id = get_unique_short_id()
    elif not is_unique_short_id(custom_id):
        flash(f'Имя {custom_id} уже занято!')
        return render_template('index.html', form=form)
    urlmap = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(urlmap)
    db.session.commit()
    flash('Ваша новая ссылка готова!', 'link-ready')
    return render_template('index.html', form=form,
                           link=urljoin(request.url_root, custom_id))


@app.route('/<short_id>', methods=['GET'])
def redirect_view(short_id):
    """Переадресует на исходный адрес при обращении к коротким ссылкам."""
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)
