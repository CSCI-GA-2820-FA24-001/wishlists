# cspell:ignore userid postalcode
"""
Test Factory to make fake objects for testing
"""
from datetime import date
from factory import Factory, SubFactory, Sequence, Faker, post_generation
from factory.fuzzy import FuzzyChoice, FuzzyDate
from service.models import Wishlist, Item, ItemStatus


class WishlistFactory(Factory):
    """Creates fake Wishlists"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""

        model = Wishlist

    id = Sequence(lambda n: n)
    name = Faker("name")
    userid = Sequence(lambda n: f"User{n:04d}")
    date_created = FuzzyDate(date(2008, 1, 1))
    # the many side of relationships can be a little wonky in factory boy:
    # https://factoryboy.readthedocs.io/en/latest/recipes.html#simple-many-to-many-relationship

    @post_generation
    def items(
        self, create, extracted, **kwargs
    ):  # pylint: disable=method-hidden, unused-argument
        """Creates the items list"""
        if not create:
            return

        if extracted:
            self.items = extracted


class ItemFactory(Factory):
    """Creates fake Items"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""

        model = Item

    id = Sequence(lambda n: n)
    wishlist_id = FuzzyChoice(choices=[0, 1, 2, 3, 4])
    name = FuzzyChoice(choices=["phone", "computer", "watch"])
    description = "description"
    price = 100.00
    status = ItemStatus.PENDING
    wishlist = SubFactory(WishlistFactory)
