from views import db
from datetime import datetime

class Family(db.Model):
    __tablename__ = "family"

    family_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    members = db.relationship("User", backref="family")
    fridge = db.relationship("Fridge", uselist=False, backref="family")
    grocery = db.relationship("Grocery", backref="family")


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    family_id = db.Column(db.Integer, ForeignKey('family.family_id'))



class Items(db.Model):
    __tablename__ = "items"

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_bought = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, name, quantity, date_bought):
        self.name = name
        self.quantity = quantity
        self.date_bought = date_bought


class Fridge(db.Model):
    __tablename__ = "fridge"

    fridge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    family_id = db.Column(db.Integer, ForeignKey('family.family_id'))



class Grocery(db.Model):
    __tablename__ = "grocery"

    grocery_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    family_id = db.Column(db.Integer, ForeignKey('family.family_id'))

    def __init__(self, name):
        self.name = name
