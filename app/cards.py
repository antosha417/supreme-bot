"""Cards page."""
from flask import redirect, request, url_for

import models
from app import app, db
from config import check_int, session, user_loggined


# TODO: add ability to delete cards
@app.route('/delete_card/<card>')
def delete_card(card):
    """Delete card from database."""
    print 'delete!', user_loggined()
    if user_loggined():
        user = models.User.query.get(session['user_id'])
        u_cards = user.cards.all()
        print u_cards
        for _card in u_cards:
            if _card.type[:4] == card[:4] and _card.cnb[-9:] == card[-9:]:
                db.session.delete(_card)
                db.session.commit()
                break
    return redirect(url_for('index'))


@app.route('/add_card', methods=['GET', 'POST'])
def add_card():
    """Add card to database."""
    if request.method == 'POST':
        data = request.form.to_dict()
        if user_loggined():
            uid = session.get('user_id')
            cnb1 = data.get('cnb1')
            cnb2 = data.get('cnb2')
            cnb3 = data.get('cnb3')
            cnb4 = data.get('cnb4')
            c_type = data.get('type')
            vval = data.get('vval')
            month = data.get('month')
            year = data.get('year')

            if c_type in ['visa', 'master'] and \
                    check_int(cnb1, 4) and      \
                    check_int(cnb2, 4) and      \
                    check_int(cnb3, 4) and      \
                    check_int(cnb4, 4) and      \
                    check_int(vval, 3) and      \
                    check_int(month, 2) and     \
                    check_int(year, 2):
                card = models.Card(type=c_type,
                                   cnb=' '.join([cnb1, cnb2, cnb3, cnb4]),
                                   month=month,
                                   year='20' + year,
                                   vval=vval,
                                   user_id=uid)
                db.session.add(card)
                db.session.commit()
            else:
                session['error'] = {}
                session['error']['card'] = True
                if c_type not in ['visa', 'master']:
                    session['error_msg'] = 'Unknown card type.'
                elif not (check_int(cnb1, 4) and check_int(cnb2, 4) and
                          check_int(cnb3, 4) and check_int(cnb4, 4)):
                    session['error_msg'] = 'Invalid card number.'
                elif not check_int(month, 2):
                    session['error_msg'] = 'Invalid expiry month.'
                elif not check_int(year, 2):
                    session['error_msg'] = 'Invalid expiry year.'
                else:
                    session['error_msg'] = 'Something went wrong.'
                return redirect(url_for('index') + '#card')

    return redirect(url_for('index') + '#order')


# TODO: add ability to view cards
@app.route('/cards')
def cards():
    """Render cards view page."""
    if user_loggined():
        user = models.User.query.get(session['user_id'])
        u_cards = user.cards.all()
        prep_cards = []
        for card in u_cards:
            prep_cards.append(card.type + ' **** '+card.cnb[-9:])
    else:
        return redirect(url_for('index'))
    return redirect(url_for('index'))
