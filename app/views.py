"""Add to app routes and errorhandlers."""
from flask import render_template, session

import addresses
import cards
import contact
import errors
import orders
import vk_auth
from app import app, models
from config import APP_ID, REDIRECT_URL, user_loggined


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Reder index page."""
    loggined = False

    user = prep_cards = prep_adr = u_orders = None

    if user_loggined():
        user = models.User.query.get(session['user_id'])
        loggined = True

        u_cards = user.cards.all()
        prep_cards = []
        for card in u_cards:
            prep_cards.append(card.type + ' **** ' + card.cnb[-9:])

        u_addresses = user.addresses.all()
        prep_adr = []
        for adr in u_addresses:
            prep_adr.append(adr.address)

        u_orders = user.orders.all()

    error = session.get('error')
    error_msg = session.get('error_msg')
    session.pop('error', None)
    session.pop('error_msg', None)

    return render_template('index.html',
                           app_id=APP_ID,
                           redir_url=REDIRECT_URL,
                           loggined=loggined,
                           cards=prep_cards,
                           adrs=prep_adr,
                           orders=u_orders,
                           user=user,
                           error=error,
                           error_msg=error_msg)

