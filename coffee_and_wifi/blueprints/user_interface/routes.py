from flask import Blueprint, flash, render_template, request
from flask.typing import ResponseReturnValue

from coffee_and_wifi.extensions.database import IntegrityError, db_wrapper
from coffee_and_wifi.extensions.database.models import Cafe
from coffee_and_wifi.extensions.forms import AddCafeForm

ui = Blueprint('ui', __name__)


@ui.route('/')
def index() -> str:
    return render_template('index.html')


@ui.route('/add', methods=['GET', 'POST'])
def add_cafe() -> ResponseReturnValue:
    form = AddCafeForm()

    if form.validate_on_submit():
        cafe_data = request.form.to_dict()
        cafe_data['name'] = cafe_data.pop('cafe_name')
        cafe_data['location'] = cafe_data.pop('cafe_location')

        try:
            with db_wrapper.database.atomic():
                Cafe.create(**cafe_data)
        except IntegrityError as exception:
            error_msg = str(exception)

            if error_msg == 'UNIQUE constraint failed: cafe.name':
                error_msg = 'Cafe with the given name already exists.'

            flash(error_msg, 'danger')

        else:
            form = AddCafeForm(formdata=None)
            flash('Cafe created successfully.', 'success')

    return render_template('add.html', form=form)


@ui.route('/cafes')
def cafes() -> str:
    cafes = list(Cafe.select().dicts())
    return render_template('cafes.html', cafes=cafes)
