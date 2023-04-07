from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TimeField, URLField
from wtforms.validators import InputRequired


def generate_rating(symbol: str) -> list[tuple[int, str]]:
    return [(0, '❌'), *((num, symbol * num) for num in range(1, 6))]


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[InputRequired()])
    cafe_location = URLField(
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
