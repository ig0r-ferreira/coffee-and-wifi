from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug import Response

from coffee_and_wifi.extensions.database import get_database
from coffee_and_wifi.forms import CafeForm
from coffee_and_wifi.models import Cafe

ui = Blueprint('ui', __name__)


@ui.route('/')
def index() -> str:
    return render_template('index.html')


@ui.route('/add', methods=['GET', 'POST'])
def add_cafe() -> str | Response:
    form = CafeForm()
    if form.validate_on_submit():
        cafe = Cafe.parse_obj(request.form.copy())
        get_database().insert(cafe.dict())

        return redirect(url_for('.cafes'))

    return render_template('add.html', form=form)


@ui.route('/cafes')
def cafes() -> str:
    cafes = get_database().all()
    return render_template('cafes.html', cafes=cafes)
