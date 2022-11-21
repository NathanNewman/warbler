"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        self.user1 = User.signup("abc", "test1@test.com", "password", None)
        self.user1_id = 1
        self.user1.id = self.user1_id
        self.user2 = User.signup("efg", "test2@test.com", "password", None)
        self.user2_id = 2
        self.user2.id = self.user2_id
        self.user3 = User.signup("hij", "test3@test.com", "password", None)
        self.user4 = User.signup("testing", "test4@test.com", "password", None)
        self.message1 = Message(
            id = 1,
            text = "test",
            user_id = 1
        )
        self.message2 = Message(
            id = 2,
            text = "test2",
            user_id = 2
        )
        self.follows1 = Follows(
            user_being_followed_id = 2,
            user_following_id = 1
        )
        self.follows2 = Follows(
            user_being_followed_id = 2,
            user_following_id = self.testuser.id
        )
        self.likes = Likes(
            id = 1,
            user_id = 2,
            message_id = 1
        )

        db.session.add(self.follows1)
        db.session.add(self.follows2)
        db.session.add(self.message1)
        db.session.add(self.message2)
        db.session.commit()
        db.session.add(self.likes)
        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_list_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>@testuser</p>', html)

    def test_users_show(self):
        with app.test_client() as client:
            res = client.get('/users/1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p class="small">Messages</p>', html)

    def test_signup(self):
        with app.test_client() as client:
            res = client.get('/signup')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2 class="join-message">Join Warbler today.</h2>', html)

    def test_show_following(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            res = client.get('users/1/following')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>@efg</p>', html)

    def test_users_followers(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            res = client.get('/users/2/followers')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>@abc</p>', html)

    def test_users_likes(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            res = client.get('/users/2/likes')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>test</p>', html)

    def test_add_follow(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            res = client.post('/users/follow/1')

            self.assertEqual(res.status_code, 200)

    def test_stop_following(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            res = client.post('/users/stop-following/2')

            self.assertEqual(res.status_code, 200)

    def test_profile(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            res = client.get('/users/profile')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>To confirm changes, enter your password:</p>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            res = client.post('/users/delete')

            self.assertEqual(res.status_code, 200)

    def test_add_like(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            res = client.post('/users/add_like/2')

            self.assertEqual(res.status_code, 200)


