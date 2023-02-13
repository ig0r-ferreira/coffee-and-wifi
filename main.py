import csv

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_prefixed_env()
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating,
# power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add')
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print('True')
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('data/cafes.csv', newline='', encoding='utf-8') as csv_file:
        rows = list(csv.reader(csv_file, delimiter=','))

    return render_template('cafes.html', cafes=rows)


if __name__ == '__main__':
    app.run(debug=True)
