from views import db
from datetime import datetime


user_pkentifier = db.Table(
    'user_pkentifier',
    db.Column('family_pk', db.Integer, db.ForeignKey('family.pk')),
    db.Column('user_pk', db.Integer, db.ForeignKey('users.pk')),
)


class User(db.Model):
    __tablename__ = "users"

    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    family_pk = db.Column(db.Integer, db.ForeignKey('family.pk'),  nullable=True)


class Family(db.Model):
    __tablename__ = "family"

    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    members = db.relationship("User", secondary=user_pkentifier, backref="family")
    fridge = db.relationship("Fridge", uselist=False, backref="family")
    grocery_lists = db.relationship("GroceryList", backref="family")


class Fridge(db.Model):
    __tablename__ = "fridge"

    pk = db.Column(db.Integer, primary_key=True)
    items = db.relationship("Item", backref="fridge")
    family_pk = db.Column(db.Integer, db.ForeignKey('family.pk'))


class GroceryList(db.Model):
    __tablename__ = "grocery_list"

    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    items = db.relationship("Item", backref="grocery_list")
    family_pk = db.Column(db.Integer, db.ForeignKey('family.pk'))

    __table_args__ = (
        db.UniqueConstraint('name', 'family_pk', name='_name_family_pk'),
    )

class Item(db.Model):
    __tablename__ = "item"

    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    date_bought = db.Column(db.Date)
    family_pk = db.Column(db.Integer, db.ForeignKey('family.pk'), nullable=False)
    fridge_pk = db.Column(db.Integer, db.ForeignKey('fridge.pk'))
    grocery_pk = db.Column(db.Integer, db.ForeignKey('grocery_list.pk'))

    __table_args__ = (
        db.UniqueConstraint('name', 'family_pk', name='_name_family_pk'),
    )
