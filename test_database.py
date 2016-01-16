import unittest
from flask.ext.testing import TestCase

from models import User, Family, Fridge, GroceryList, Item
from views import app, db

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://test.db"
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
        db.session.add_all([user, user2, user3])
        # Adding Families
        family = Family(name='Family-name-1', members=[user, user2])
        family2 = Family(name='Family-name-2', members=[user, user3])
        db.session.add_all([family, family2, user3])
        # Adding Fridges
        fridge = Fridge()
        fridge2 = Fridge()
        db.session.add_all([fridge, fridge2])
        family.fridge = fridge
        family2.fridge = fridge2
        # Adding Grocery Lists
        grocery_list = GroceryList(name="listname1")
        grocery_list2 = GroceryList(name="listname2")
        grocery_list3 = GroceryList(name="listname3")
        db.session.add_all([grocery_list, grocery_list2, grocery_list3])
        family.grocery_lists.append(grocery_list)
        family.grocery_lists.append(grocery_list2)
        family2.grocery_lists.append(grocery_list3)
        db.session.commit()
        # Adding items
        item1 = Item(name="item1", family_pk=family.pk)
        item2 = Item(name="item2", family_pk=family.pk)
        item3 = Item(name="item3", family_pk=family.pk)
        item4 = Item(name="item4", family_pk=family2.pk)
        item5 = Item(name="item5", family_pk=family2.pk)
        db.session.add_all([item1, item2, item3, item4, item5])
        # Adding items to fridge
        fridge.items.append(item1)
        fridge2.items.append(item2)
        # Adding items to grocery lists
        grocery_list.items.append(item3)
        grocery_list3.items.append(item4)
        grocery_list3.items.append(item5)
        db.session.commit()


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

    def test_can_access_fridge_via_family(self):
        """ Check that the fridge can be access via the family model """
        family = db.session.query(Family).filter(Family.name=="Family-name-1").one()
        fridge = db.session.query(Fridge).filter(Fridge.family_pk==family.pk).one()
        self.assertEqual(family.fridge, fridge)

    def test_grocery_list_access_via_family(self):
        """ Check that the grocery_list can be access via the family model """
        family = db.session.query(Family).filter(Family.name=="Family-name-1").one()
        g_lists = db.session.query(Fridge).filter(GroceryList.family_pk==family.pk).all()
        self.assertEqual(len(family.grocery_lists), 2)

    def test_items_in_fridge(self):
        """ Check that the fridge contains items """
        family = db.session.query(Family).filter(Family.name=="Family-name-2").one()
        self.assertEqual(len(family.fridge.items), 1)

    def test_items_in_grocery_list(self):
        """ Check that the fridge contains items """
        family = db.session.query(Family).filter(Family.name=="Family-name-2").one()
        self.assertEqual(len(family.grocery_lists[0].items), 2)

    def test_that_item_can_only_be_in_fridge_or_glist(self):
        """ Test that an item can only be either in the fridge or a grocery list """
        family = db.session.query(Family).filter(Family.name=="Family-name-2").one()
        # Check number of items in fridge and glist
        self.assertEqual(len(family.fridge.items), 1)
        self.assertEqual(len(family.grocery_lists[0].items), 2)
        # Switch the item to glist
        family.fridge.items.append(family.grocery_lists[0].items[0])
        db.session.commit()
        # Check that the item moved over
        self.assertEqual(len(family.fridge.items), 2)
        self.assertEqual(len(family.grocery_lists[0].items), 1)


if __name__ == "__main__":
    unittest.main()
