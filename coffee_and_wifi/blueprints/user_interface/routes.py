from flask import Blueprint, redirect, render_template, request, url_for

from coffee_and_wifi.forms import CafeForm
from coffee_and_wifi.storage import read_csv, save_to_csv

ui = Blueprint('ui', __name__)


@ui.route('/')
def index():
    return render_template('index.html')


@ui.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        form_data = request.form.copy()
        form_data.pop('csrf_token', None)

        save_to_csv(form_data)

        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@ui.route('/cafes')
def cafes():
    table = read_csv()
    return render_template(
        'cafes.html', cafes=table['rows'], headers=table['headers']
    )
