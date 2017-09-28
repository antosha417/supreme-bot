"""Orders page."""
import pickle

from flask import redirect, request, url_for

import models
from app import app, db
from config import session, user_loggined


# TODO: add ability to delete orders
@app.route('/delete_order/<order_id>')
def delete_order(order_id):
    """Delete order from data base."""
    if user_loggined():
        user = models.User.query.get(session['user_id'])
        u_orders = user.orders.all()
        for _order in u_orders:
            if str(_order.order_id) == order_id:
                db.session.delete(_order)
                db.session.commit()
                break
    return redirect(url_for('index'))


# TODO: add ability to view orders


@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    """Add order to data base."""
    if request.method == 'POST':
        type_ = None
        country = None
        zip_ = None
        city = None
        address = None
        vval = None
        year = None
        month = None
        cnb = None
        data = request.form.to_dict()
        if user_loggined():
            uid = session.get('user_id')
            user = models.User.query.get(uid)
            name = data.get('name')
            email = data.get('email')

            card = data.get('card')
            u_cards = user.cards.all()
            for _card in u_cards:
                if _card.type[:4] == card[:4] and _card.cnb[-9:] == card[-9:]:
                    type_ = _card.type
                    cnb = _card.cnb
                    month = _card.month
                    year = _card.year
                    vval = _card.vval

            adr = data.get('adr')
            u_addresses = user.addresses.all()
            for _adr in u_addresses:
                if adr == _adr.address:
                    address = _adr.address
                    city = _adr.city
                    zip_ = _adr.zip
                    country = _adr.country
            clothes_name = data.get('clothes_name')
            clothes_colors = data.get('clothes_colors')
            size = data.get('size')
            tel = data.get('tel')
            if name is not None and                 \
                    email is not None and           \
                    type_ is not None and           \
                    cnb is not None and             \
                    month is not None and           \
                    year is not None and            \
                    vval is not None and            \
                    address is not None and         \
                    city is not None and            \
                    zip_ is not None and            \
                    country is not None and         \
                    clothes_name is not None and    \
                    clothes_colors is not None and  \
                    size is not None and            \
                    tel is not None:

                _max = 1
                for _order in models.Order.query.all():
                    _max = max(_max, _order.order_id)
                colors = pickle.dumps(clothes_colors.split(' '))
                order = models.Order(order_id=_max + 1,
                                     user_id=uid,
                                     name=name,
                                     email=email,
                                     clothes_name=clothes_name,
                                     size=size,
                                     tel=tel,
                                     card=card,
                                     adr=adr,
                                     clothes_colors=colors)
                db.session.add(order)
                db.session.commit()
    return redirect(url_for('index'))

