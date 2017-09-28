"""Discription of data base models."""
from app import db


class User(db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=False)
    cards = db.relationship('Card', backref='owner', lazy='dynamic')
    addresses = db.relationship('Address', backref='owner', lazy='dynamic')
    orders = db.relationship('Order', backref='owner', lazy='dynamic')

    def __repr__(self):
        """User repr function."""
        return '<User: ' + self.name + '>'


class Card(db.Model):
    """Card model."""

    type = db.Column(db.String(10), index=True, unique=False)
    cnb = db.Column(db.String(25), index=True, unique=True, primary_key=True)
    month = db.Column(db.String(2), index=True, unique=False)
    year = db.Column(db.String(4), index=True, unique=False)
    vval = db.Column(db.String(5), index=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Card repr function."""
        return '<Card: ' + self.cnb + '>'


class Address(db.Model):
    """Address model."""

    address_id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(30), index=True, unique=False)
    city = db.Column(db.String(15), index=True, unique=False)
    zip = db.Column(db.String(15), index=True, unique=False)
    country = db.Column(db.String(2), index=True, unique=False)

    def __repr__(self):
        """Address repr function."""
        return '<Address: ' + self.address + '>'


class Order(db.Model):
    """Order model."""

    order_id = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    name = db.Column(db.String(100), index=True, unique=False)
    email = db.Column(db.String(100), index=True, unique=False)
    clothes_name = db.Column(db.String(1000), index=True, unique=False)
    clothes_colors = db.Column(db.String(2000), index=True, unique=False)
    size = db.Column(db.String(20), index=True, unique=False)
    tel = db.Column(db.String(20), index=True, unique=False)

    card = db.Column(db.String(100), index=True, unique=False)
    adr = db.Column(db.String(100), index=True, unique=False)

