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


class Item(db.Model):
    __tablename__ = "item"

    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer)
    date_bought = db.Column(db.Date)
    family_pk = db.Column(db.Integer, db.ForeignKey('family.pk'), nullable=False)

    discriminator = db.Column(db.String)
    parent_id = db.Column(db.Integer)

    __table_args__ = (
        db.UniqueConstraint('name', 'family_pk', name='_name_family_pk'),
    )

    @property
    def parent(self):
        """Provides in-Python access to the "parent" by choosing
        the appropriate relationship. """
        return getattr(self, "parent_%s" % self.discriminator)


class HasItems(object):
    """IsInList mixin, creates a relationship to
    the items_association table for each parent.
    http://docs.sqlalchemy.org/en/rel_1_0/_modules/examples/generic_associations/generic_fk.html
     """


@db.event.listens_for(HasItems, "mapper_configured", propagate=True)
def setup_listener(mapper, class_):
    name = class_.__name__
    discriminator = name.lower()
    class_.items = db.relationship(Item,
        primaryjoin=db.and_(
            class_.pk == db.foreign(db.remote(Item.parent_id)),
            Item.discriminator == discriminator
        ),
        backref=db.backref(
                "parent_%s" % discriminator,
                primaryjoin=db.remote(class_.pk) == db.foreign(Item.parent_id)
                )
        )
    @db.event.listens_for(class_.items, "append")
    def append_address(target, value, initiator):
        value.discriminator = discriminator


class Fridge(HasItems, db.Model):
    __tablename__ = "fridge"

    pk = db.Column(db.Integer, primary_key=True)
    family_pk = db.Column(db.Integer, db.ForeignKey('family.pk'))


class GroceryList(HasItems, db.Model):
    __tablename__ = "grocery_list"

    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    family_pk = db.Column(db.Integer, db.ForeignKey('family.pk'))

    __table_args__ = (
        db.UniqueConstraint('name', 'family_pk', name='_name_family_pk'),
    )
