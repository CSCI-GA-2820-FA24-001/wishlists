# cspell:ignore userid postalcode
"""
Models for YourResourceModel

All of the models are stored in this module
"""

from abc import abstractmethod
import logging
from datetime import date
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class ItemStatus(Enum):
    """
    Class that represents the status of a wishlist item
    """

    PENDING = "pending"
    PURCHASED = "purchased"
    OUT_OF_STOCK = "out_of_stock"
    EXPIRED = "expired"
    FAVORITE = "favorite"


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase:
    """Base class added persistent methods"""

    def __init__(self):
        self.id = None  # pylint: disable=invalid-name

    @abstractmethod
    def serialize(self) -> dict:
        """Convert an object into a dictionary"""

    @abstractmethod
    def deserialize(self, data: dict) -> None:
        """Convert a dictionary into an object"""

    def create(self) -> None:
        """
        Creates a Wishlist to the database
        """
        logger.info("Creating %s", self)
        # id must be none to generate next primary key
        self.id = None
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self) -> None:
        """
        Updates a Wishlist to the database
        """
        logger.info("Updating %s", self)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self) -> None:
        """Removes a Wishlist from the data store"""
        logger.info("Deleting %s", self)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    @classmethod
    def all(cls):
        """Returns all of the records in the database"""
        logger.info("Processing all records")
        # pylint: disable=no-member
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a record by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        # pylint: disable=no-member
        return cls.query.session.get(cls, by_id)


######################################################################
#  W I S H L I S T  M O D E L
######################################################################
class Wishlist(db.Model, PersistentBase):
    """
    Class that represents an Wishlist
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    userid = db.Column(db.String(16), nullable=False)
    date_created = db.Column(db.Date(), nullable=False, default=date.today())
    items = db.relationship("Item", backref="wishlist", passive_deletes=True)

    def __repr__(self):
        return f"<Wishlist {self.name} id=[{self.id}]>"

    def serialize(self):
        """Converts an Wishlist into a dictionary"""
        wishlist = {
            "id": self.id,
            "name": self.name,
            "userid": self.userid,
            "date_created": self.date_created.isoformat(),
            "items": [],
        }
        for item in self.items:
            wishlist["items"].append(item.serialize())
        return wishlist

    def deserialize(self, data):
        """
        Populates an Wishlist from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.userid = data["userid"]
            self.date_created = date.fromisoformat(data["date_created"])
            # handle inner list of items
            item_list = data.get("items")
            for json_item in item_list:
                item = Item()
                item.deserialize(json_item)
                self.items.append(item)
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Wishlist: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlist: body of request contained bad or no data "
                + str(error)
            ) from error

        return self

    ######################################################################
    #  C L A S S  M E T H O D S
    ######################################################################
    @classmethod
    def find_by_name(cls, name):
        """Returns all Wishlists with the given name

        Args:
            name (string): the name of the Wishlists you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_userid(cls, userid):
        """Returns all Wishlists with the given userid"""
        logger.info("Processing userid query for %s ...", userid)
        return cls.query.filter(cls.userid == userid)

    @classmethod
    def find_by_date_created(cls, date_created):
        """Returns all Wishlists with the given date created"""
        logger.info("Processing date_created query for %s ...", date_created)
        try:
            search_date = date.fromisoformat(date_created)
            return cls.query.filter(cls.date_created == search_date)
        except ValueError as error:
            raise DataValidationError(
                "Invalid date format. Use YYYY-MM-DD format."
            ) from error

    @classmethod
    def find_since_date(cls, target_date):
        """Returns all Wishlists created since the given date"""
        logger.info("Processing since date query for %s ...", target_date)
        try:
            search_date = date.fromisoformat(target_date)
            return cls.query.filter(cls.date_created >= search_date)
        except ValueError as error:
            raise DataValidationError(
                "Invalid date format. Use YYYY-MM-DD format."
            ) from error


######################################################################
#  I T E M   M O D E L
######################################################################
class Item(db.Model, PersistentBase):
    """
    Class that represents an Item
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(
        db.Integer, db.ForeignKey("wishlist.id", ondelete="CASCADE"), nullable=False
    )
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    status = db.Column(db.Enum(ItemStatus), nullable=True, server_default="PENDING")

    def __repr__(self):
        return f"<Item {self.name} id=[{self.id}] wishlist[{self.wishlist_id}]>"

    def __str__(self):
        return f"{self.id} - {self.name}"

    def serialize(self) -> dict:
        """Converts an Item into a dictionary"""
        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "status": self.status.value,
        }

    def deserialize(self, data: dict) -> None:
        """
        Populates an Item from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.wishlist_id = data["wishlist_id"]
            self.name = data["name"]
            self.description = data["description"]

            # Verify and transform the type of price
            self.price = float(data["price"])
            if self.price <= 0:
                raise ValueError("Price must be a positive number.")
            self.status = ItemStatus(data["status"])

        except (KeyError, AttributeError) as error:
            raise DataValidationError(
                f"Invalid Item: missing or invalid field {error.args[0]}"
            ) from error
        except (ValueError, TypeError) as error:
            raise DataValidationError(
                "Invalid Item: 'price' must be a positive number."
            ) from error

        return self
