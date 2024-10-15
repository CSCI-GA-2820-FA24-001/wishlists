######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
TestWishlist API Service Test Suite
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Item, Wishlist
from .factories import WishlistFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/wishlists"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestWishlistService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_wishlists(self, count):
        """Factory method to create wishlists in bulk"""
        wishlists = []
        for _ in range(count):
            wishlist = WishlistFactory()
            resp = self.client.post(BASE_URL, json=wishlist.serialize())
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Wishlist",
            )
            new_wishlist = resp.get_json()
            wishlist.id = new_wishlist["id"]
            wishlists.append(wishlist)
        return wishlists

    ######################################################################
    #  W I S H L I S T   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # Todo: Add your test cases here...
    def test_get_wishlist(self):
        """It should Read a single Wishlist"""
        # get the id of an wishlist
        wishlist = self._create_wishlists(1)[0]
        resp = self.client.get(
            f"{BASE_URL}/{wishlist.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], wishlist.name)

    def test_get_wishlist_not_found(self):
        """It should not Read an Wishlist that is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_wishlist(self):
        """It should Create a new Wishlist"""
        test_wishlist = WishlistFactory()
        logging.debug("Test Wishlist: %s", test_wishlist.serialize())

        response = self.client.post(
            BASE_URL, json=test_wishlist.serialize(), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_wishlist = response.get_json()
        self.assertEqual(
            new_wishlist["name"], test_wishlist.name, "Name does not match"
        )
        self.assertEqual(
            new_wishlist["userid"], test_wishlist.userid, "User ID does not match"
        )
        self.assertEqual(
            new_wishlist["date_created"],
            (test_wishlist.date_created).isoformat(),
            "Date Created does not match",
        )

        # Check that the location header was correct
        response = self.client.get(location, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_wishlist = response.get_json()
        self.assertEqual(
            new_wishlist["name"], test_wishlist.name, "Name does not match"
        )
        self.assertEqual(
            new_wishlist["userid"], test_wishlist.userid, "User ID does not match"
        )
        self.assertEqual(
            new_wishlist["date_created"],
            str(test_wishlist.date_created),
            "Date Created does not match",
        )

    def test_update_wishlist(self):
        """It should Update an existing Wishlist"""
        # create an Wishlist to update
        test_wishlist = WishlistFactory()
        resp = self.client.post(BASE_URL, json=test_wishlist.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the pet
        new_wishlist = resp.get_json()
        new_wishlist["name"] = "new new new Name"
        new_wishlist_id = new_wishlist["id"]
        resp = self.client.put(f"{BASE_URL}/{new_wishlist_id}", json=new_wishlist)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_wishlist = resp.get_json()
        self.assertEqual(updated_wishlist["name"], "new new new Name")

    def test_update_wishlist_not_found(self):
        """Test the behavior of UPDATE with wishlist not found"""
        test_wishlist = WishlistFactory()
        resp = self.client.put(f"{BASE_URL}/0", json=test_wishlist.serialize())
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_wishlists(self):
        """Test the ability to GET all wishlists"""
        self._create_wishlists(10)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 10)

    def test_get_wishlists_by_name(self):
        """Test the ability to GET wishlists by names"""
        wishlists = self._create_wishlists(3)
        # test for all three created wishlists
        for wishlist in wishlists:
            resp = self.client.get(BASE_URL, query_string=f"name={wishlist.name}")
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            data = resp.get_json()
            self.assertGreater(len(data), 0)
            for returned_wishlist in data:
                self.assertEqual(returned_wishlist["name"], wishlist.name)

    def test_get_empty_wishlist(self):
        """Test the behavior of GET with empty database"""
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 0)

    def test_delete_wishlist(self):
        """Test to delete a wishlist"""
        wishlist = self._create_wishlists(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{wishlist.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        # Verify deletion
        resp = self.client.get(f"{BASE_URL}/{wishlist.id}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_wishlist_not_found(self):
        """Test the behavior of DELETE with wishlist not found"""
        resp = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    ######################################################################
    #  I T E M   E N D P O I N T   T E S T   C A S E S
    ######################################################################

    def test_add_item_missing_fields(self):
        """It should return 400 when required fields are missing"""
        # create a wishlist
        wishlist = self._create_wishlists(1)[0]

        # define am object data without 'price' field
        incomplete_item_data = {
            "name": "Smartphone",
            "description": "Latest model smartphone",
            # 'price' is missing
        }

        # Send a POST request to add this item
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=incomplete_item_data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertIn("missing fields", data["message"].lower())
        self.assertIn("price", data["message"].lower())

    def test_add_item_invalid_price_string(self):
        """It should return 400 when the price is invalid as a string"""
        # create a wishlist
        wishlist = self._create_wishlists(1)[0]

        # define an invalid item data
        invalid_price_item_data = {
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": "invalid_price",
        }
        # Send a POST request to add this item
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=invalid_price_item_data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertIn("must be a positive number", data["message"].lower())

    def test_add_item_invalid_price_nonpositive(self):
        """It should return 400 when the price is invalid as a non-positive number"""
        # create a wishlist
        wishlist = self._create_wishlists(1)[0]

        # define an invalid item data
        invalid_price_item_data = {
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": -3.1415926,
        }
        # Send a POST request to add this item
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=invalid_price_item_data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertIn("must be a positive number", data["message"].lower())

    def test_add_item_nonexistent_wishlist(self):
        """It should return 404 when adding an item to a non-existent wishlist"""
        # define valid item data
        valid_item_data = {
            "name": "Tablet",
            "description": "Latest model tablet",
            "price": 499.99,
        }

        # send POST request to a non-existent wishlist id
        response = self.client.post(
            "/wishlists/999/items",
            json=valid_item_data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("wishlist with id '999' not found", data["message"].lower())

    def test_add_item_duplicate_name(self):
        """It should return 409 when adding an item with a duplicate name in the wishlist"""
        # create a wishlist
        wishlist = self._create_wishlists(1)[0]

        # create an item
        item_data = {
            "name": "Headphones",
            "description": "Noise-cancelling headphones",
            "price": 199.99,
        }
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # attempt to add an item with duplicated name
        duplicate_item_data = {
            "name": "Headphones",  # duplicated name of "Headphone"
            "description": "Wireless headphones",
            "price": 249.99,
        }
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=duplicate_item_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        data = response.get_json()
        self.assertIn("already exists", data["message"].lower())

    def test_get_item_success(self):
        """It should retrieve an existing item from a wishlist"""
        # create a wishlist
        wishlist = self._create_wishlists(1)[0]
        # create an item
        item = ItemFactory(wishlist_id=wishlist.id)
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_item = response.get_json()

        # Access the item by GET request
        get_response = self.client.get(
            f"{BASE_URL}/{wishlist.id}/items/{created_item['id']}",
            content_type="application/json",
        )
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        fetched_item = get_response.get_json()
        self.assertEqual(fetched_item["name"], item.name)
        self.assertEqual(fetched_item["description"], item.description)
        self.assertEqual(float(fetched_item["price"]), float(item.price))

    def test_get_item_nonexistent_wishlist(self):
        """It should return 404 when retrieving an item from a non-existent wishlist"""
        response = self.client.get(
            "/wishlists/999/items/1", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("not found", data["message"].lower())

    def test_get_nonexistent_item(self):
        """It should return 404 when retrieving a non-existent item from a wishlist"""
        # create a wishlist
        wishlist = self._create_wishlists(1)[0]
        response = self.client.get(
            f"{BASE_URL}/{wishlist.id}/items/999", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("not found", data["message"].lower())

    def test_delete_item_success(self):
        """It should delete an existing item from a wishlist"""
        # create a wishlist
        wishlist = self._create_wishlists(1)[0]
        # create an item
        item = ItemFactory(wishlist_id=wishlist.id)
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_item = response.get_json()

        # Request deleting that item by sending a DELETE request
        delete_response = self.client.delete(
            f"{BASE_URL}/{wishlist.id}/items/{created_item['id']}",
            content_type="application/json",
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        # verify that the item is deleted successfully
        get_response = self.client.get(
            f"{BASE_URL}/{wishlist.id}/items/{created_item['id']}",
            content_type="application/json",
        )
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item_nonexistent_wishlist(self):
        """It should return 404 when deleting an item from a non-existent wishlist"""
        response = self.client.delete(
            "/wishlists/999/items/1", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("not found", data["message"].lower())

    def test_delete_nonexistent_item(self):
        """It should return 404 when deleting a non-existent item from a wishlist"""
        # create a wishlist
        wishlist = self._create_wishlists(1)[0]
        response = self.client.delete(
            f"{BASE_URL}/{wishlist.id}/items/999", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("not found", data["message"].lower())

    def test_bad_request(self):
        """It should not Create when sending the wrong data"""
        resp = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should not Create when sending wrong media type"""
        account = WishlistFactory()
        resp = self.client.post(
            BASE_URL, json=account.serialize(), content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        resp = self.client.put(BASE_URL, json={"not": "today"})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
