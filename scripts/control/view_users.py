import app.models as models

users = models.User.query.all()

for user in users:
    print 'user: |', user.id, '|'
    print 'name -', user.name
    print '*' + '='*65 + '*'
    print
print 'Total amount is', len(users)
