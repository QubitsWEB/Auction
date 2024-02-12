from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from app.models.lot import Lot, Message, Bid
from app.extensions import db
from app.forms.lots import CreateAuctionLotForm, EditLotForm
from flask_paginate import get_page_args
from flask_login import current_user, login_required
from flask_socketio import SocketIO, emit
from app.extensions import socketio




lots_bp = Blueprint("lots", __name__, url_prefix="/lots")

@lots_bp.route('/create_lot', methods=['GET', 'POST'])
@login_required  # Assuming you're using Flask-Login
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
        owner_id = current_user.id  # Assuming current_user has id attribute

        new_lot = Lot(title=title, description=description, width=width, height=height,
                      weight=weight, initial_price=initial_price, minimum_bid=minimum_bid,
                      photo_url=photo_url, auction_start_date=auction_start_date,
                      auction_end_date=auction_end_date, owner_id=owner_id)
        db.session.add(new_lot)
        db.session.commit()

        return redirect(url_for('pages.core.home_route'))

    return render_template('pages/create_lot.html', form=form)


@lots_bp.route('/<lot_id>')
def view_lot(lot_id):
    lot = Lot.query.get_or_404(lot_id)
    chat_messages = Message.query.filter_by(lot_id=lot_id).all()
    return render_template('pages/lot.html', lot=lot, chat_messages=chat_messages)


@lots_bp.route('/edit/<lot_id>', methods=['GET', 'POST'])
@login_required
def edit_lot(lot_id):
    # Retrieve the lot from the database
    lot = Lot.query.get_or_404(lot_id)

    # Check if the current user is the owner of the lot
    if lot.owner_id != current_user.id:
        flash('You are not the owner of this lot.', 'danger')
        return redirect(url_for('pages.lots.view_lot', lot_id=lot_id))

    # Create the edit form and populate it with the current lot data
    form = EditLotForm(obj=lot)

    # Handle form submission
    if form.validate_on_submit():
        # Update the lot data with the form data
        form.populate_obj(lot)

        # Commit the changes to the database
        db.session.commit()

        # Flash a success message
        flash('Lot updated successfully.', 'success')

        # Redirect the user back to the view page of the lot
        return redirect(url_for('pages.lots.view_lot', lot_id=lot_id))

    # Render the edit lot template with the form and lot data
    return render_template('pages/edit_lot.html', form=form, lot=lot)

@lots_bp.route('/chat_history/<lot_id>')
def get_chat_history(lot_id):
    # Retrieve the chat history for the specified lot from the database
    messages = Message.query.filter_by(lot_id=lot_id).all()

    # Serialize the messages to JSON
    chat_history = [{'text': message.text, 'lot_id': message.lot_id} for message in messages]

    # Return the chat history as JSON
    return jsonify(chat_history)


@lots_bp.route('/')
def view_all_lots():
    # Pagination configuration
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 10  # Number of lots per page

    # Query database for all lots
    all_lots = Lot.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('pages/all_lots.html', all_lots=all_lots)


# WebSocket route
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('chat_message')
def handle_chat_message(data):
    message_text = data['message']
    message_text = f'Message from {str(current_user.name)}: {message_text}'
    lot_id = data['lot_id']

    # Find the lot associated with the message
    lot = Lot.query.get_or_404(lot_id)

    # Create a new message object and associate it with the lot ID
    message = Message(text=message_text, lot_id=lot_id)

    # Save the message to the database
    db.session.add(message)
    db.session.commit()

    # Fetch the updated chat history for the specific lot
    chat_history = Message.query.filter_by(lot_id=lot_id).all()

    # Broadcast the message and updated chat history to all clients in the chat
    emit('chat_message', {'message': message_text, 'lot_id': lot_id})

@socketio.on('place_bid')
def handle_place_bid(data):
    lot_id = data['lot_id']
    bid_amount = data['bid']
    message_text = f'Bid from {str(current_user.name)}: {str(bid_amount)}'
    lot = Lot.query.get_or_404(lot_id)
    bid = Bid(amount=bid_amount, lot_id=lot_id)

    db.session.add(bid)
    db.session.commit()

    emit('bid_placed', {'message': message_text, 'lot_id': lot_id}, broadcast=True)


