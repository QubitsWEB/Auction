from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, DateTimeField
from wtforms.validators import InputRequired

class CreateAuctionLotForm(FlaskForm):
    name = StringField('Name of lot', validators=[InputRequired()])
    description = TextAreaField('Description.')
    start_price = FloatField('Start price', validators=[InputRequired()])
    auction_end_time = DateTimeField('Auction end date and time', format='%Y-%m-%d %H:%M:%S', validators=[InputRequired()], default=datetime.now)
