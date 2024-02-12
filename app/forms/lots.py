from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, DateTimeField
from wtforms.validators import InputRequired, URL, DataRequired


class CreateAuctionLotForm(FlaskForm):
    title = StringField('Lot Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    width = FloatField('Width', validators=[InputRequired()])
    height = FloatField('Height', validators=[InputRequired()])
    weight = FloatField('Weight', validators=[InputRequired()])
    initial_price = FloatField('Initial Price', validators=[InputRequired()])
    minimum_bid = FloatField('Minimum Bid', validators=[InputRequired()])
    photo_url = StringField('Photo URL')
    auction_start_date = DateTimeField('Auction Start Date and Time', format='%Y-%m-%d %H:%M:%S', validators=[InputRequired()], default=datetime.now)
    auction_end_date = DateTimeField('Auction End Date and Time', format='%Y-%m-%d %H:%M:%S', validators=[InputRequired()])


class EditLotForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    width = FloatField('Width', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    initial_price = FloatField('Initial Price', validators=[DataRequired()])
    minimum_bid = FloatField('Minimum Bid', validators=[DataRequired()])
    photo_url = StringField('Photo URL')
    auction_start_date = DateTimeField('Auction Start Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    auction_end_date = DateTimeField('Auction End Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
