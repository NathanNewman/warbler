"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

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

class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        Likes.query.delete()

        self.client = app.test_client()

    def test_Message_model(self):
        """Does basic model work?"""

        testuser = User(
            id = 1,
            email = "test@test.com",
            username = "testuser",
            image_url = None,
            password = "password"
        )
        
        message = Message(
            id = 1,
            text="test",
            user_id=1
        )

        db.session.add(testuser)
        db.session.commit()
        db.session.add(message)
        db.session.commit()

        self.assertEqual(message.user.username, "testuser")
        self.assertEqual(message.user.email, "test@test.com")