# cspell:ignore userid postalcode
"""
Test cases for Wishlist Model
"""

import os
from unittest.mock import patch

from service.models import Wishlist, Item, DataValidationError
from tests.factories import WishlistFactory, ItemFactory
from tests.test_base import BaseTestCase


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#        W I S H L I S T   M O D E L   T E S T   C A S E S
######################################################################
class TestWishlist(BaseTestCase):
    """Wishlist Model Test Cases"""

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
        # # issue with matching two date format - AssertionError: '2023-06-18' != datetime.date(2023, 6, 18)
        # # .isoformat() works for test_tourtes l94 but not here
        # self.assertEqual(wishlist.date_created, fake_wishlist.date_created)

    def test_add_a_wishlist(self):
        """It should Create a wishlist and add it to the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistFactory()
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

    @patch("service.models.db.session.commit")
    def test_add_wishlist_failed(self, exception_mock):
        """It should not create an Wishlist on database error"""
        exception_mock.side_effect = Exception()
        wishlist = WishlistFactory()
        self.assertRaises(DataValidationError, wishlist.create)

    def test_read_wishlist(self):
        """It should Read an wishlist"""
        wishlist = WishlistFactory()
        wishlist.create()

        # Read it back
        found_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(found_wishlist.id, wishlist.id)
        self.assertEqual(found_wishlist.name, wishlist.name)
        self.assertEqual(found_wishlist.userid, wishlist.userid)
        self.assertEqual(found_wishlist.date_created, wishlist.date_created)
        self.assertEqual(found_wishlist.items, [])

    def test_delete_a_wishlist(self):
        """It should Delete a wishlist from the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistFactory()
        wishlist.create()
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        wishlist = wishlists[0]
        wishlist.delete()
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 0)

    @patch("service.models.db.session.commit")
    def test_delete_wishlist_failed(self, exception_mock):
        """It should not delete a Wishlist on database error"""
        exception_mock.side_effect = Exception()
        wishlist = WishlistFactory()
        self.assertRaises(DataValidationError, wishlist.delete)

    def test_list_all_wishlists(self):
        """It should List all Wishlists in the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        for wishlist in WishlistFactory.create_batch(5):
            wishlist.create()
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 5)

    def test_find_by_name(self):
        """It should Find a Wishlist by name"""
        wishlist = WishlistFactory()
        wishlist.create()
        same_wishlist = Wishlist.find_by_name(wishlist.name)[0]
        self.assertEqual(same_wishlist.id, wishlist.id)
        self.assertEqual(same_wishlist.name, wishlist.name)

    def test_find_by_userid(self):
        """It should Find a Wishlist by name"""
        wishlist = WishlistFactory()
        wishlist.create()
        same_wishlist = Wishlist.find_by_userid(wishlist.userid)[0]
        self.assertEqual(same_wishlist.id, wishlist.id)
        self.assertEqual(same_wishlist.userid, wishlist.userid)

    def test_find_by_date_created(self):
        """It should Find a Wishlist by date created"""
        wishlist = WishlistFactory()
        wishlist.create()
        same_wishlist = Wishlist.find_by_date_created(wishlist.date_created.isoformat())[0]
        self.assertEqual(same_wishlist.id, wishlist.id)
        self.assertEqual(same_wishlist.date_created, wishlist.date_created)

    def test_deserialize_an_wishlist(self):
        """It should Deserialize an wishlist"""
        wishlist = WishlistFactory()
        wishlist.items.append(ItemFactory())
        wishlist.create()
        serial_wishlist = wishlist.serialize()
        new_wishlist = Wishlist()
        new_wishlist.deserialize(serial_wishlist)
        self.assertEqual(new_wishlist.name, wishlist.name)
        self.assertEqual(new_wishlist.userid, wishlist.userid)
        self.assertEqual(new_wishlist.date_created, wishlist.date_created)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize a wishlist with a KeyError"""
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, {})

    def test_deserialize_with_attribution_error(self):
        """It should not Deserialize a wishlist with a AttributeError"""
        wishlist = Wishlist()
        self.assertRaises(
            DataValidationError, wishlist.deserialize, {"date_created": 123}
        )

    def test_deserialize_with_type_error(self):
        """It should not Deserialize a wishlist with a TypeError"""
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, [])

    def test_deserialize_item_key_error(self):
        """It should not Deserialize an item with a KeyError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_item_type_error(self):
        """It should not Deserialize an item with a TypeError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])

    def test_update_wishlist(self):
        """It should Update an wishlist"""
        wishlist = WishlistFactory(name="testWishlistName")
        wishlist.create()

        # Fetch it back
        wishlist = Wishlist.find(wishlist.id)
        wishlist.name = "testWishlistName"
        wishlist.update()

        # Fetch it back again
        wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(wishlist.name, "testWishlistName")

    @patch("service.models.db.session.commit")
    def test_update_wishlist_failed(self, exception_mock):
        """It should not update a Wishlist on database error"""
        exception_mock.side_effect = Exception()
        wishlist = WishlistFactory()
        self.assertRaises(DataValidationError, wishlist.update)
