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
# cspell:ignore userid postalcode
"""
YourResourceModel Service

This service implements a REST API that allows you to Create, Read, Update
and Delete YourResourceModel
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Item, Wishlist, DataValidationError
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Wishlist REST API Service",
            version="1.0",
            paths=url_for("list_wishlists", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Todo: Place your REST API code here ...


######################################################################
# CREATE A NEW WISHLIST
######################################################################
@app.route("/wishlists", methods=["POST"])
def create_wishlists():
    """
    Create a Wishlist
    This endpoint will create a Wishlist based the data in the body that is posted
    """
    app.logger.info("Request to create an Wishlist")
    check_content_type("application/json")

    # Create the wishlist
    wishlist = Wishlist()
    wishlist.deserialize(request.get_json())
    wishlist.create()

    # Create a message to return
    message = wishlist.serialize()
    location_url = url_for("get_wishlists", wishlist_id=wishlist.id, _external=True)

    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# RETRIEVE A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["GET"])
def get_wishlists(wishlist_id):
    """
    Retrieve a single Wishlist

    This endpoint will return an Wishlist based on it's id
    """
    app.logger.info("Request for Wishlist with id: %s", wishlist_id)

    # See if the wishlist exists and abort if it doesn't
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' could not be found.",
        )

    return jsonify(wishlist.serialize()), status.HTTP_200_OK


######################################################################
# LIST ALL WISHLISTS
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """Returns all wishlists, if GET request contains name, return wishlist by name"""
    wishlists = []
    name = request.args.get("name")
    if name:
        app.logger.info("Request for listing specific Wishlists")
        wishlists = Wishlist.find_by_name(name)
    else:
        app.logger.info("Request for listing all Wishlists")
        wishlists = Wishlist.all()
    results = [wishlist.serialize() for wishlist in wishlists]
    return jsonify(results), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["PUT"])
def update_wishlists(wishlist_id):
    """
    Update an Wishlist

    This endpoint will update an Wishlist based the body that is posted
    """
    app.logger.info("Request to update wishlist with id: %s", wishlist_id)
    check_content_type("application/json")

    # See if the wishlist exists and abort if it doesn't
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' was not found.",
        )

    # Update from the json in the body of the request
    wishlist.deserialize(request.get_json())
    wishlist.id = wishlist_id
    wishlist.update()
    app.logger.info("Wishlist with ID: %d updated.", wishlist.id)

    return jsonify(wishlist.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
    """Delete a wishlist based on id specified in the path"""
    app.logger.info("Request to delete wishlist with id: %s", wishlist_id)
    wishlist = Wishlist.find(wishlist_id)
    if wishlist:
        wishlist.delete()
        app.logger.info("Wishlist with id: %s deleted", wishlist_id)
    else:
        app.logger.info("Wishlist with id: %s not found", wishlist_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# ADD A NEW ITEM TO A SPECIFIC WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlistId>/items", methods=["POST"])
def add_item_to_wishlist(wishlistId):
    """
    Add a new item to a specific Wishlist

    This endpoint will add a new item to the wishlist specified by wishlistId
    based on the data provided in the request body.
    """
    app.logger.info(f"Request to add a new item to wishlist with id: {wishlistId}")
    # Ensure the request content type is application/json
    check_content_type("application/json")
    # Parse the JSON request body
    item_data = request.get_json()
    # Validate required fields
    required_fields = ["name", "description", "price"]
    missing_fields = [field for field in required_fields if field not in item_data]
    if missing_fields:
        app.logger.error(f"Missing fields in request body: {missing_fields}")
        abort(
            status.HTTP_400_BAD_REQUEST,
            f"Missing fields in request body: {', '.join(missing_fields)}",
        )
    # Inject wishlist_id from the URL path into the item data
    item_data["wishlist_id"] = wishlistId

    # Create a new Item instance and deserialize the data
    new_item = Item()
    try:
        new_item.deserialize(item_data)
    except DataValidationError as e:
        app.logger.error(f"Data validation error: {e}")
        abort(
            status.HTTP_400_BAD_REQUEST,
            f"Data validation error: {e}",
        )

    # Find the wishlist by ID
    wishlist = Wishlist.find(wishlistId)
    if not wishlist:
        app.logger.error(f"Wishlist with id '{wishlistId}' not found.")
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlistId}' not found.",
        )

    # Check if an item with the same name already exists in the wishlist
    existing_item = Item.query.filter_by(
        wishlist_id=wishlistId, name=new_item.name
    ).first()
    if existing_item:
        app.logger.error(
            f"Item with name '{new_item.name}' already exists in wishlist '{wishlistId}'."
        )
        abort(
            status.HTTP_409_CONFLICT,
            f"Item with name '{new_item.name}' already exists in wishlist '{wishlistId}'.",
        )

    # Add the new item to the database
    try:
        new_item.create()
    except Exception as e:
        app.logger.error(f"Unexpected error when creating item: {e}")
        abort(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred while creating the item.",
        )
    # Serialize the new item for the response
    serialized_item = new_item.serialize()

    # Generate the Location URL for the newly created item
    location_url = url_for(
        "get_item",  # Ensure that this endpoint is defined
        wishlistId=wishlistId,
        itemId=new_item.id,
        _external=True,
    )

    # Return the response with 201 Created and Location header
    return jsonify(serialized_item), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
