import unittest
from flask.ext.testing import TestCase

from models import User, Family, Fridge, GroceryList, Item
from views import app, db

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def setUp(self):
        db.create_all()
        # Adding Users
        user = User(name='user1', email="test@gmail.com")
        user2 = User(name='user2',  email="test2@gmail.com")
        user3 = User(name='user3',  email="test3@gmail.com")
        db.session.add(user)
        db.session.add(user2)
        db.session.add(user3)
        # Adding Families
        family = Family(name='Family-name-1', members=[user, user2])
        family2 = Family(name='Family-name-2', members=[user, user3])
        db.session.add(family)
        db.session.add(family2)
        # Adding Fridges
        fridge = Fridge()
        fridge2 = Fridge()
        db.session.add(fridge)
        db.session.add(fridge2)
        family.fridge = fridge
        family2.fridge = fridge2
        db.session.add(fridge)
        db.session.add(fridge2)
        # Adding Grocery Lists
        grocery_list = GroceryList(name="listname1")
        grocery_list2 = GroceryList(name="listname2")
        db.session.add(grocery_list)
        db.session.add(grocery_list2)
        family.grocery_lists.append(grocery_list)
        family2.grocery_lists.append(grocery_list2)
        db.session.commit()
        """
        # Adding items
        item1 = Item(name="item1", family_pk=family.pk)
        item2 = Item(name="item2", family_pk=family.pk)
        item3 = Item(name="item3", family_pk=family.pk)
        item4 = Item(name="item4", family_pk=family2.pk)
        item5 = Item(name="item5", family_pk=family2.pk)
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.add(item4)
        db.session.add(item5)
        # Adding items to grocery lists  
        grocery_list.items.append(item1)
        grocery_list.items.append(item2)
        grocery_list.items.append(item3)
        grocery_list2.items.append(item4)
        grocery_list2.items.append(item5)
        # Adding items to fridge
        fridge.items.append(item1)
        fridge2.items.append(item2)
        db.session.commit()
        """

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_users_added(self):
        """ Check that users were stored """
        users = db.session.query(User).all()
        self.assertEqual(len(users), 3)

    def test_families_added(self):
        """ Check that familes were stored """
        users = db.session.query(Family).all()
        self.assertEqual(len(users), 2)

    def test_familes_have_members(self):
        """ Check that you can access members via family """
        family1 = db.session.query(Family).filter(Family.name=="Family-name-1").one()
        family2 = db.session.query(Family).filter(Family.name=="Family-name-2").one()
        self.assertEqual(len(family1.members), 2)
        self.assertEqual(len(family2.members), 2)

    def test_can_access_family_via_member(self):
        """ Check that user have families that can be accessed """
        user = db.session.query(User).filter(User.name=="user1").one()
        self.assertEqual(len(user.family), 2)


if __name__ == "__main__":
    unittest.main()
