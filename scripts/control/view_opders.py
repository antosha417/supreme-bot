import app.models as models
import pickle

orders = models.Order.query.all()

for order in orders:

    user = models.User.query.get(order.user_id)

    _type = None
    cnb = None
    month = None
    year = None
    vval = None

    city = None
    address = None
    _zip = None
    country = None

    name = order.name
    email = order.email

    card = order.card
    u_cards = user.cards.all()
    for _card in u_cards:
        if _card.type[:4] == card[:4] and _card.cnb[-9:] == card[-9:]:
            _type = _card.type
            cnb = _card.cnb
            month = _card.month
            year = _card.year
            vval = _card.vval

    adr = order.adr
    u_addresses = user.addresses.all()
    for _adr in u_addresses:
        if adr == _adr.address:
            address = _adr.address
            city = _adr.city
            _zip = _adr.zip
            country = _adr.country
    clothes_name = order.clothes_name
    clothes_name = '.*'.join(clothes_name.split(' '))
    clothes_colors = str(pickle.loads(order.clothes_colors))
    size = order.size
    tel = order.tel

    with open('order_data.py', 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('clothes_name = "' + clothes_name + '"\n')
        f.write('clothes_colors = ' + clothes_colors + '\n')
        f.write('order_size = "' + size + '"\n')

        f.write('billing_name = "' + name.encode('utf8') + '"\n')
        f.write('email = "' + email + '"\n')
        f.write('tel = "' + tel + '"\n')
        f.write('billing_address = "' + address + '"\n')
        f.write('billing_city = "' + city + '"\n')
        f.write('billing_zip = "' + _zip + '"\n')
        f.write('billing_country = "' + country + '"\n')
        f.write('credit_card_type = "' + _type + '"\n')
        f.write('credit_card_cnb = "' + cnb + '"\n')
        f.write('credit_card_month = "' + month + '"\n')
        f.write('credit_card_year = "' + year + '"\n')
        f.write('credit_card_vval = "' + vval + '"\n')

    print 'order: |', order.order_id, '|'
    with open('order_data.py', 'r') as f:
        print f.read()
        print '*' + '='*65 + '*'

print 'Total amount is', len(orders)
