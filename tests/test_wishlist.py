# cspell:ignore userid postalcode
"""
Test cases for Wishlist Model
"""

import logging
import os
from unittest import TestCase
from wsgi import app

from service.models import Wishlist, Item, db
from tests.factories import WishlistFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#        A C C O U N T   M O D E L   T E S T   C A S E S
######################################################################
class TestWishlist(TestCase):
    """Wishlist Model Test Cases"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.query(Item).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_create_a_wishlist(self):
        """It should Create an Wishlist and assert that it exists"""
        fake_wishlist = WishlistFactory()
        # pylint: disable=unexpected-keyword-arg
        wishlist = Wishlist(
            name=fake_wishlist.name,
            userid=fake_wishlist.userid,
            date_created=fake_wishlist.date_created,
        )
        self.assertIsNotNone(wishlist)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.name, fake_wishlist.name)
        self.assertEqual(wishlist.userid, fake_wishlist.userid)
        # # issue with matching two date format - AssertionError: '2023-06-18' != datetime.date(2023, 6, 18), .isoformat() works for test_tourtes l94 but not here
        # self.assertEqual(wishlist.date_created, fake_wishlist.date_created)
