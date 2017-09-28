"""Addressses page."""
from flask import redirect, request, url_for

import models
from app import app, db
from config import KNOWN_COUNTRIES, check_int, session, user_loggined


# TODO: add ability to delete addresses
@app.route('/delete_adr/<adr>')
def delete_adr(adr):
    """Delete address from database."""
    if user_loggined():
        user = models.User.query.get(session['user_id'])
        u_addresses = user.addresses.all()
        for _adr in u_addresses:
            if adr == _adr.address:
                db.session.delete(_adr)
                db.session.commit()
                break
    return redirect(url_for('index'))


@app.route('/add_addres', methods=['GET', 'POST'])
def add_address():
    """Add address to database."""
    if request.method == 'POST':
        data = request.form.to_dict()
        if user_loggined():
            uid = session.get('user_id')
            country = data.get('country')
            address = data.get('address')
            city = data.get('city')
            zip_ = data.get('zip')
            if country is not None and              \
                    country in KNOWN_COUNTRIES and  \
                    city is not None and            \
                    address is not None and         \
                    len(address) < 30 and           \
                    len(city) < 15 and              \
                    check_int(zip_, 6):
                adr = models.Address(country=country,
                                     city=city,
                                     address=address,
                                     zip=zip_,
                                     user_id=uid)
                db.session.add(adr)
                db.session.commit()
            else:
                session['error'] = {}
                session['error']['address'] = True
                if country is None:
                    session['error_msg'] = 'Country is not specified.'
                elif country not in KNOWN_COUNTRIES:
                    session['error_msg'] = 'Unknown country.'
                elif city is None:
                    session['error_msg'] = 'City is not specified.'
                elif address is None:
                    session['error_msg'] = 'Address is not specified.'
                elif not check_int(zip_, 6):
                    session['error_msg'] = 'Zip must be a six digit number.'
                elif len(address) >= 30:
                    error = 'Address must be less than 30 characters length.'
                    session['error_msg'] = error
                elif len(city) >= 15:
                    error = 'City must be less than 15 characters length.'
                    session['error_msg'] = error
                else:
                    session['error_msg'] = 'Something went wrong.'
                return redirect(url_for('index') + '#address')
    return redirect(url_for('index') + '#card')


# TODO: add ability to view addresses
@app.route('/addresses')
def addresses():
    """Render page to view addresses."""
    if user_loggined():
        user = models.User.query.get(session['user_id'])
        u_addresses = user.addresses.all()
        prep_adr = []
        for adr in u_addresses:
            prep_adr.append(adr.address)
    else:
        return redirect(url_for('index'))
    return redirect(url_for('index'))
