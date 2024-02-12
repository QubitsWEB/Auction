# Flask modules
from app.extensions import db

# Other modules
from datetime import datetime

# Local modules
from app.utils.models import generate_uuid


class Lot(db.Model):
    id = db.Column(
        db.String, primary_key=True, default=generate_uuid, unique=True, nullable=False
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    initial_price = db.Column(db.Float, nullable=False)
    minimum_bid = db.Column(db.Float, nullable=False)
    photo_url = db.Column(db.String(2048), nullable=True)  # URL of the lot photo
    auction_start_date = db.Column(db.DateTime, nullable=False, default=datetime)
    auction_end_date = db.Column(db.DateTime, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    owner = db.relationship('User', backref='lots')
