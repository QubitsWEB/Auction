from flask_sqlalchemy import SQLAlchemy

# Model for a lot at a web auction
db = SQLAlchemy()

# Model for a lot at a web auction
class AuctionLot(db.Model):
    __tablename__ = 'auction_lots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False, default=0.0)
    auction_end_time = db.Column(db.DateTime, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)  # Image path may be empty

    def __repr__(self):
        return f'<AuctionLot {self.name}>'
