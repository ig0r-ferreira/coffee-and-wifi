import csv

from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TimeField, URLField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config.from_prefixed_env()
bootstrap = Bootstrap5(app)


def generate_rating(symbol: str):
    return ['❌', *(symbol * num for num in range(1, 6))]


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[InputRequired()])
    cafe_location_url = URLField(
        'Cafe Location on Google Maps (URL)', validators=[InputRequired()]
    )
    opening_time = TimeField('Opening Time', validators=[InputRequired()])
    closing_time = TimeField('Closing Time', validators=[InputRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=generate_rating('☕️'))
    wifi_rating = SelectField(
        'Wi-Fi Strength Rating', choices=generate_rating('💪')
    )
    power_rating = SelectField(
        'Power Socket Available', choices=generate_rating('🔌')
    )
    submit = SubmitField('Submit')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('data/cafes.csv', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        rows = list(reader)
    return render_template('cafes.html', cafes=rows, headers=reader.fieldnames)
