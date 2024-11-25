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
from flask_restx import fields
from service.models import Item, Wishlist, ItemStatus
from service.common import status  # HTTP Status Codes
from . import api

# Define the model so that the docs reflect what can be sent
create_wishlist_model = api.model(
    "Wishlist",
    {
        "name": fields.String(required=True, description="The name of the Wishlist"),
        "userid": fields.String(required=True, description="The User ID of the Wishlist"),
        "date_created": fields.Date(required=True, description="The day the wishlist was created"),
        "items": fields.List(fields.Raw, description="List of items in the wishlist", default=[])
    },
)

wishlist_model = api.inherit(
    "WishlistModel",
    create_wishlist_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique wishlist id assigned internally by service"
        ),
    },
)

create_item_model = api.model(
    "Item",
    {
        "wishlist_id": fields.Integer(required=True, description="The ID of the wishlist this item belongs to"),
        "name": fields.String(required=True, description="The name of the item"),
        "description": fields.String(required=True, description="The description of the item"),
        "price": fields.Float(required=True, description="The price of the item (must be positive)"),
        "status": fields.String(required=True, enum=["PENDING", "PURCHASED", "OUT_OF_STOCK", "EXPIRED", "FAVORITE"],
                                description="The status of the item")
    }
)

item_model = api.inherit(
    "ItemModel",
    create_item_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique item id assigned internally by service"
        ),
    }
)


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


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
            description=f"Wishlist with id '{wishlist_id}' could not be found.",
        )

    return jsonify(wishlist.serialize()), status.HTTP_200_OK


######################################################################
# LIST ALL WISHLISTS
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """Returns all wishlists, if GET request contains name, return wishlist by name, same for userid"""
    wishlists = []

    name = request.args.get("name")
    userid = request.args.get("userid")
    date_created = request.args.get("date_created")
    since_date = request.args.get("since_date")

    if name:
        app.logger.info("Request for listing wishlists by name: %s", name)
        wishlists = Wishlist.find_by_name(name)
    elif userid:
        app.logger.info("Request for listing wishlists by userid: %s", userid)
        wishlists = Wishlist.find_by_userid(userid)
    elif date_created:
        app.logger.info(
            "Request for listing wishlists created on date: %s", date_created
        )
        wishlists = Wishlist.find_by_date_created(date_created)
    elif since_date:
        app.logger.info("Request for listing wishlists since date: %s", since_date)
        wishlists = Wishlist.find_since_date(since_date)
    else:
        app.logger.info("Request for listing all Wishlists")
        wishlists = Wishlist.all()
    results = [wishlist.serialize() for wishlist in wishlists]
    return jsonify(results), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING WISHLIST
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
            description=f"Wishlist with id '{wishlist_id}' was not found.",
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
# LIST ALL ITEMS IN AN EXISTING WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items", methods=["GET"])
def list_items(wishlist_id):
    """Returns all items"""
    app.logger.info("Request to list all items from wishlist with id: %s", wishlist_id)
    # check_content_type("application/json")

    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            description=f"Wishlist with id '{wishlist_id}' was not found.",
        )
    myitems = wishlist.items
    results = [item.serialize() for item in myitems]
    return jsonify(results), status.HTTP_200_OK


######################################################################
# ADD A NEW ITEM TO A SPECIFIC WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items", methods=["POST"])
def add_item_to_wishlist(wishlist_id):
    """
    Add a new item to a specific Wishlist

    This endpoint will add a new item to the wishlist specified by wishlist_id
    based on the data provided in the request body.
    """
    app.logger.info(f"Request to add a new item to wishlist with id: {wishlist_id}")

    # Ensure the request content type is application/json
    check_content_type("application/json")

    # Find the wishlist by ID
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        app.logger.error(f"Wishlist with id '{wishlist_id}' not found.")
        abort(
            status.HTTP_404_NOT_FOUND,
            description=f"Wishlist with id '{wishlist_id}' not found.",
        )

    # Create a new Item instance and deserialize the data
    new_item = Item()
    item_data = request.get_json()
    item_data["wishlist_id"] = wishlist_id
    new_item.deserialize(item_data)

    # Check if an item with the same name already exists in the wishlist
    existing_item = Item.query.filter_by(
        wishlist_id=wishlist_id, name=new_item.name
    ).first()
    if existing_item:
        app.logger.error(
            f"Item with name '{new_item.name}' already exists in wishlist '{wishlist_id}'."
        )
        abort(
            status.HTTP_409_CONFLICT,
            description=f"Item with name '{new_item.name}' already exists in wishlist '{wishlist_id}'.",
        )

    # Add the new item to the database
    new_item.create()
    # Serialize the new item for the response
    serialized_item = new_item.serialize()

    # Generate the Location URL for the newly created item
    location_url = url_for(
        "get_item",  # Ensure that this endpoint is defined
        wishlist_id=wishlist_id,
        item_id=new_item.id,
        _external=True,
    )

    # Return the response with 201 Created and Location header
    return jsonify(serialized_item), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# UPDATE AN EXISTING ITEM IN A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["PUT"])
def update_item_in_wishlist(wishlist_id, item_id):
    """
    Update the details of an existing Item in a specific Wishlist

    This endpoint will update the Item specified by item_id in the Wishlist specified by wishlist_id
    based on the data provided in the request body.
    """
    app.logger.info(
        f"Request to update item with id: {item_id} in wishlist with id: {wishlist_id}"
    )

    # Ensure the request content type is application/json
    check_content_type("application/json")

    # Parse the JSON request body
    item_data = request.get_json()

    # Find the wishlist and item
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        app.logger.error(f"Wishlist with id '{wishlist_id}' not found.")
        abort(
            status.HTTP_404_NOT_FOUND,
            description=f"Wishlist with id '{wishlist_id}' not found.",
        )
    item = find_item_in_wishlist(wishlist_id, item_id)

    # Check for duplicate item name within the same wishlist
    check_for_duplicate_item(wishlist_id, item_data["name"], item_id)

    # Update the item's details
    update_item_details(item, item_data)

    # Commit the changes to the database
    save_updated_item(item)

    # Serialize the updated item and return the response
    return generate_update_response(wishlist_id, item)


def find_item_in_wishlist(wishlist_id, item_id):
    """Find an item in the wishlist by its ID"""
    item = Item.query.filter_by(wishlist_id=wishlist_id, id=item_id).first()
    if not item:
        app.logger.error(
            f"Item with id '{item_id}' not found in wishlist '{wishlist_id}'."
        )
        abort(
            status.HTTP_404_NOT_FOUND,
            description=f"Item with id '{item_id}' not found in wishlist '{wishlist_id}'.",
        )
    return item


def check_for_duplicate_item(wishlist_id, item_name, item_id):
    """Check if an item with the same name already exists in the wishlist"""
    existing_item = Item.query.filter_by(
        wishlist_id=wishlist_id, name=item_name
    ).first()
    if existing_item and existing_item.id != item_id:
        app.logger.error(
            f"Item with name '{item_name}' already exists in wishlist '{wishlist_id}'."
        )
        abort(
            status.HTTP_409_CONFLICT,
            description=f"Item with name '{item_name}' already exists in wishlist '{wishlist_id}'.",
        )


def update_item_details(item, item_data):
    """Update the item details"""
    item.name = item_data["name"]
    item.description = item_data["description"]
    item.price = float(item_data["price"])


def save_updated_item(item):
    """Save the updated item to the database"""
    item.update()


def generate_update_response(wishlist_id, item):
    """Generate the response for a successful item update"""
    serialized_item = item.serialize()
    location_url = url_for(
        "get_item",  # Ensure that this endpoint is defined
        wishlist_id=wishlist_id,
        item_id=item.id,
        _external=True,
    )
    return jsonify(serialized_item), status.HTTP_200_OK, {"Location": location_url}


######################################################################
# RETRIEVE A SPECIFIC ITEM FROM A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["GET"])
def get_item(wishlist_id, item_id):
    """
    Retrieve a specific Item from a Wishlist

    This endpoint will return an Item based on its id within the specified wishlist
    """
    app.logger.info(f"Request for item with id: {item_id} in wishlist {wishlist_id}")

    # Find the wishlist
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        app.logger.error(f"Wishlist with id '{wishlist_id}' not found.")
        abort(
            status.HTTP_404_NOT_FOUND,
            description=f"Wishlist with id '{wishlist_id}' not found.",
        )

    # Find the item within the wishlist
    item = Item.query.filter_by(wishlist_id=wishlist_id, id=item_id).first()
    if not item:
        app.logger.error(
            f"Item with id '{item_id}' not found in wishlist '{wishlist_id}'."
        )
        abort(
            status.HTTP_404_NOT_FOUND,
            description=f"Item with id '{item_id}' not found in wishlist '{wishlist_id}'.",
        )

    return jsonify(item.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A SPECIFIC ITEM FROM A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["DELETE"])
def delete_item_from_wishlist(wishlist_id, item_id):
    """
    Delete a specific Item from a Wishlist

    This endpoint will delete an Item based on its id within the specified wishlist
    """
    app.logger.info(
        f"Request to delete item with id: {item_id} from wishlist with id: {wishlist_id}"
    )

    # Find the wishlist
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        app.logger.error(f"Wishlist with id '{wishlist_id}' not found.")
        abort(
            status.HTTP_404_NOT_FOUND,
            description=f"Wishlist with id '{wishlist_id}' not found.",
        )

    # Find the item within the wishlist
    item = Item.query.filter_by(wishlist_id=wishlist_id, id=item_id).first()
    if item:
        item.delete()
    else:
        app.logger.error(
            f"Item with id '{item_id}' not found in wishlist '{wishlist_id}'."
        )

    app.logger.info(
        f"Item with id '{item_id}' not found in wishlist '{wishlist_id}', returning 204."
    )
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# ACTION: Purchased an item.
######################################################################
def purchase_item_from_wishlist(item):
    """Action of purchasing an item from a wishlist."""
    item.status = ItemStatus.PURCHASED
    item.update()

    # After purchasing, delete the item from the wishlist.
    item.delete()


@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>/purchase", methods=["PUT"])
def purchase_item(wishlist_id, item_id):
    """Purchase an item from a wishlist."""
    app.logger.info(f"Request for item with id: {item_id} in wishlist {wishlist_id}")

    # Find the wishlist and item
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        app.logger.error(f"Wishlist with id '{wishlist_id}' not found.")
        abort(
            status.HTTP_404_NOT_FOUND,
            description=f"Wishlist with id '{wishlist_id}' not found.",
        )
    item = find_item_in_wishlist(wishlist_id, item_id)

    app.logger.info(f"Purchase item id: {item_id} from Wishlist {wishlist_id}...")
    purchase_item_from_wishlist(item)

    # Return the updated order
    return jsonify(item.serialize()), status.HTTP_200_OK


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
            description=f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        description=f"Content-Type must be {content_type}",
    )
