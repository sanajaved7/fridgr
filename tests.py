import unittest
from flask.ext.testing import TestCase

from models import User, Family
from views import app, db

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def setUp(self):
        db.create_all()
        user = User(name='user1', password='test')
        user2 = User(name='user2', password='test')
        family = Family(name='Family-name', members=[user, user2])
        db.session.add(user)
        db.session.add(user2)
        db.session.add(family)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_db_store(self):
        """ Check that base database items were stored """
        users = db.session.query(User).all()
        self.assertEqual(len(users), 2)

if __name__ == "__main__":
    unittest.main()
