# cspell:ignore userid postalcode
"""
Test cases for Item Model
"""

import logging
import os
from unittest import TestCase
from wsgi import app

from service.models import Wishlist, Item, db, DataValidationError
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

    ######################################################################
    #  I T E M   M O D E L   T E S T   C A S E S
    ######################################################################

    def test_deserialize_item_success(self):
        """It should deserialize a valid item dictionary"""
        fake_item = ItemFactory()
        item = Item()
        item_data = {
            "wishlist_id": fake_item.wishlist_id,
            "name": fake_item.name,
            "description": fake_item.description,
            "price": fake_item.price,
        }
        item.deserialize(item_data)
        self.assertEqual(item.wishlist_id, fake_item.wishlist_id)
        self.assertEqual(item.name, fake_item.name)
        self.assertEqual(item.description, fake_item.description)
        self.assertEqual(float(item.price), float(fake_item.price))

    def test_deserialize_item_missing_fields(self):
        """It should raise DataValidationError when required fields are missing"""
        item = Item()
        item_data = {
            "name": "Laptop",
            # Missing 'wishlist_id', 'description', 'price'
        }
        with self.assertRaises(DataValidationError) as context:
            item.deserialize(item_data)
        self.assertIn("missing", str(context.exception).lower())

    def test_deserialize_item_invalid_price(self):
        """It should raise DataValidationError when price is invalid"""
        item = Item()
        item_data = {
            "wishlist_id": 1,
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": "invalid_price",
        }
        with self.assertRaises(DataValidationError) as context:
            item.deserialize(item_data)
        self.assertIn("bad or no data", str(context.exception).lower())

    def test_serialize_item(self):
        """It should serialize an item to a dictionary"""
        wishlist = WishlistFactory()
        item = Item(
            wishlist_id=wishlist.id,
            name="Laptop",
            description="Gaming Laptop",
            price=1500.00,
        )
        item.create()
        serialized = item.serialize()
        self.assertIsInstance(serialized, dict)
        self.assertEqual(serialized["id"], item.id)
        self.assertEqual(serialized["wishlist_id"], item.wishlist_id)
        self.assertEqual(serialized["name"], item.name)
        self.assertEqual(serialized["description"], item.description)
        self.assertEqual(float(serialized["price"]), float(item.price))

    def test_update_item_model_success(self):
        """It should update an item's attributes and commit to the database"""
        wishlist = WishlistFactory()
        item = ItemFactory(wishlist_id=wishlist.id)
        item.create()
        # original_name = item.name
        # original_description = item.description
        # original_price = item.price

        # Update item attributes
        item.name = "Updated Laptop"
        item.description = "Updated Gaming Laptop"
        item.price = 1600.00
        item.update()

        # Fetch the updated item from the database
        updated_item = Item.find(item.id)
        self.assertEqual(updated_item.name, "Updated Laptop")
        self.assertEqual(updated_item.description, "Updated Gaming Laptop")
        self.assertEqual(float(updated_item.price), 1600.00)

    def test_update_item_model_duplicate_name(self):
        """It should not allow updating an item to have a name that already exists in the wishlist"""
        wishlist = WishlistFactory()
        item1 = ItemFactory(wishlist_id=wishlist.id, name="Laptop")
        item1.create()
        item2 = ItemFactory(wishlist_id=wishlist.id, name="Headphones")
        item2.create()

        # Attempt to update item2's name to "Laptop", which already exists
        item2.name = "Laptop"
        with self.assertRaises(Exception) as context:
            item2.update()
        # Depending on the database constraints, the exception message may vary
        self.assertTrue(
            "duplicate" in str(context.exception).lower()
            or "unique" in str(context.exception).lower()
        )
