from views import db
from datetime import datetime


user_identifier = db.Table(
    'user_identifier',
    db.Column('family_id', db.Integer, db.ForeignKey('family.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'),  nullable=True)


class Family(db.Model):
    __tablename__ = "family"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    members = db.relationship("User", secondary=user_identifier, backref="family")
    fridge = db.relationship("Fridge", uselist=False, backref="family")
    grocery = db.relationship("Grocery", backref="family")
    

class Fridge(db.Model):
    __tablename__ = "fridge"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    items = db.relationship("Items", backref="fridge")
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))


class Grocery(db.Model):
    __tablename__ = "grocery"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    items = db.relationship("Items", backref="grocery")
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))


class Items(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_bought = db.Column(db.Date, nullable=False)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'))
    grocery_id = db.Column(db.Integer, db.ForeignKey('grocery.id'))


