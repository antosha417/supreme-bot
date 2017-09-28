import app.models as models

addresses = models.Address.query.all()

for address in addresses:
    print 'address_id: |', address.address_id, '|'
    print 'address -', address.address
    print 'user_id -', address.user_id
    print '*' + '='*65 + '*'
    print
print 'Total amount is', len(addresses)
