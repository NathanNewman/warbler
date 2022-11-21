"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_signup(self):
        user = User.signup("testuser", "123@email.com", "password", "image")
        self.assertEqual(user.username,"testuser")
        self.assertEqual(user.email,"123@email.com")
        self.assertEqual(user.image_url,"image")

    def test_authenticate(self):
        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=""
        )

        db.session.add(u)
        db.session.commit()
        user = User.authenticate("testuser","HASHED_PASSWORD")
        wrong_user = User.authenticate("wronguser","HASHED_PASSWORD")
        wrong_password = User.authenticate("testuser","WRONG_PASSWORD")

        self.assertTrue(user)
        self.assertFalse(wrong_user)
        self.assertFalse(wrong_password)
