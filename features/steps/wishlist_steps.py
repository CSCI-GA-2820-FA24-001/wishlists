"""
Wishlist Steps
Steps file for wishlist.feature
"""

import requests
from compare3 import expect
from behave import given
import logging

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
WAIT_TIMEOUT = 60


@given("the following wishlists")
def step_impl(context):
    """Delete all Wishlists and load new ones"""
    # List all wishlists
    rest_endpoint = f"{context.base_url}/wishlists"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    expect(context.resp.status_code).equal_to(HTTP_200_OK)

    # Delete them all
    for wishlist in context.resp.json():
        context.resp = requests.delete(
            f"{rest_endpoint}/{wishlist['id']}", timeout=WAIT_TIMEOUT
        )
        expect(context.resp.status_code).equal_to(HTTP_204_NO_CONTENT)

    # Create new ones from our table
    for row in context.table:
        payload = {
            "name": row["name"],
            "userid": row["userid"],
            "date_created": row["date_created"],
            "items": [],
        }
        context.resp = requests.post(rest_endpoint, json=payload, timeout=WAIT_TIMEOUT)
        expect(context.resp.status_code).equal_to(HTTP_201_CREATED)

        # Store the id of the wishlist if we need to reference it
        wishlist = context.resp.json()
        context.wishlist_id = wishlist["id"]
        logging.info("Created wishlist with ID: %s", context.wishlist_id)
