import app.models as models

cards = models.Card.query.all()

for card in cards:
    print 'user_id: |', card.user_id, '|'
    print 'cnb -', card.cnb
    print 'date -', card.month, card.year
    print 'type -', card.type
    print 'vval -', card.vval
    print '*' + '='*65 + '*'
    print
print 'Total amount is', len(cards)
