from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug import Response

from coffee_and_wifi.extensions.database.models import Cafe
from coffee_and_wifi.forms import CafeForm

ui = Blueprint('ui', __name__)


@ui.route('/')
def index() -> str:
    return render_template('index.html')


@ui.route('/add', methods=['GET', 'POST'])
def add_cafe() -> str | Response:
    form = CafeForm()

    if form.validate_on_submit():
        cafe_data = request.form.to_dict()
        cafe_data['name'] = cafe_data.pop('cafe_name')
        cafe_data['location'] = cafe_data.pop('cafe_location')
        Cafe.create(**cafe_data)

        return redirect(url_for('.cafes'))

    return render_template('add.html', form=form)


@ui.route('/cafes')
def cafes() -> str:
    cafes = list(Cafe.select().dicts())
    return render_template('cafes.html', cafes=cafes)
