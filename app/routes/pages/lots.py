# Flask modules
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.lot import db, AuctionLot
from app.forms.lots import CreateAuctionLotForm
from datetime import datetime

lots_bp = Blueprint("lots", __name__, url_prefix="/lots")


@lots_bp.route('/create_lot', methods=['GET', 'POST'])
def create_lot():
    form = CreateAuctionLotForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        start_price = form.start_price.data
        auction_end_time = form.auction_end_time.data
        # Збереження лоту в базі даних
        new_lot = AuctionLot(name=name, description=description, start_price=start_price,
                             auction_end_time=auction_end_time)
        db.session.add(new_lot)
        db.session.commit()
        return redirect(url_for('index'))  # Перенаправлення на головну сторінку після успішного створення лоту
    return render_template('create_lot.html', form=form)
