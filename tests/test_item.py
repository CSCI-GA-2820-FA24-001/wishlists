# cspell:ignore userid postalcode
"""
Test cases for Item Model
"""

import os

from service.models import Item, DataValidationError
from tests.factories import ItemFactory, WishlistFactory
from tests.test_base import BaseTestCase


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#        I T E M   M O D E L   T E S T   C A S E S
######################################################################
class TestItem(BaseTestCase):
    """Item Model Test Cases"""

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
        self.assertIn(
            "invalid item: 'price' must be a positive number.",
            str(context.exception).lower(),
        )

    def test_serialize_an_item(self):
        """It should serialize an Item"""
        item = ItemFactory()
        serial_item = item.serialize()
        self.assertEqual(serial_item["id"], item.id)
        self.assertEqual(serial_item["wishlist_id"], item.wishlist_id)
        self.assertEqual(serial_item["name"], item.name)
        self.assertEqual(serial_item["description"], item.description)
        self.assertEqual(serial_item["price"], item.price)

    def test_deserialize_an_item(self):
        """It should deserialize an Item"""
        item = ItemFactory()
        item.create()
        new_item = Item()
        new_item.deserialize(item.serialize())
        self.assertEqual(new_item.wishlist_id, item.wishlist_id)
        self.assertEqual(new_item.name, item.name)
        self.assertEqual(new_item.description, item.description)
        self.assertEqual(new_item.price, item.price)

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
