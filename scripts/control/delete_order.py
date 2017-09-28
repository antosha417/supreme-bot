from app import db
import app.models as models

order_id = int(input('Enter order_id:'))

order = models.Order.query.get(order_id)
if order is not None:
    db.session.delete(order)
    db.session.commit()
    print 'Order', order_id, 'was deleted.'
else:
    print 'Could not find order', order_id
