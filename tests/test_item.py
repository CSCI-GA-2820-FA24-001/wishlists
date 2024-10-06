# cspell:ignore userid postalcode
"""
Test cases for Item Model
"""

import logging
import os
from unittest import TestCase
from wsgi import app

from service.models import Wishlist, Item, db
from tests.factories import ItemFactory, WishlistFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#        A D D R E S S   M O D E L   T E S T   C A S E S
######################################################################
class TestWishlist(TestCase):
    """Item Model Test Cases"""

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
    def test_create_an_item(self):
        """It should create an Item"""
        fake_item = ItemFactory()
        item = Item(
            wishlist_id=fake_item.wishlist_id,
            name=fake_item.name,
            description=fake_item.description,
            price=fake_item.price,
        )
        self.assertIsNotNone(item)
