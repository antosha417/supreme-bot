import sys
from app import db
import app.models as models

order_id = int(sys.argv[1])

card = models.Card.query.get(order_id)

db.session.delete(card)
db.session.commit()
