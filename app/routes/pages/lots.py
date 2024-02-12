from flask import Blueprint, render_template, request, redirect, url_for
from app.models.lot import db, Lot
from app.forms.lots import CreateAuctionLotForm
from datetime import datetime

lots_bp = Blueprint("lots", __name__, url_prefix="/lots")

@lots_bp.route('/create_lot', methods=['GET', 'POST'])
def create_lot():
    form = CreateAuctionLotForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        width = form.width.data
        height = form.height.data
        weight = form.weight.data
        initial_price = form.initial_price.data
        minimum_bid = form.minimum_bid.data
        photo_url = form.photo_url.data
        auction_start_date = form.auction_start_date.data
        auction_end_date = form.auction_end_date.data
        # Збереження лоту в базі даних
        new_lot = Lot(title=title, description=description, width=width, height=height, weight=weight,
                      initial_price=initial_price, minimum_bid=minimum_bid, photo_url=photo_url,
                      auction_start_date=auction_start_date, auction_end_date=auction_end_date)
        db.session.add(new_lot)
        db.session.commit()
        return redirect(url_for('pages.core.home_route'))  # Replace 'core' with the actual module name, if necessary

    return render_template('pages/create_lot.html', form=form)
