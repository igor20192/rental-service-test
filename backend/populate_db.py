import os
import django
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.contrib.auth import get_user_model
from apps.apartments.models import Apartment
from factory import Factory, Faker, SubFactory
from factory.django import DjangoModelFactory


User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        """
        Factory for creating User instances.
        """

        model = User

    email = Faker("email")
    is_verified = Faker("boolean")
    last_name = Faker("last_name")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Custom create method for UserFactory.

        Handles setting the password for the user and ensures that first_name
        and last_name do not exceed the maximum allowed length.
        """

        # Ensure first_name and last_name do not exceed the maximum length
        password = kwargs.pop("password", None)
        kwargs["first_name"] = kwargs.get("first_name", "")[:50]
        kwargs["last_name"] = kwargs.get("last_name", "")[:50]
        kwargs["slug"] = kwargs.get("slug", "")[:50]
        obj = model_class(*args, **kwargs)
        if password:
            obj.set_password(password)
        obj.save()
        return obj


class ApartmentFactory(DjangoModelFactory):
    class Meta:
        """
        Factory for creating Apartment instances.
        """

        model = Apartment

    name = Faker("sentence", nb_words=6)
    description = Faker("text", max_nb_chars=200)
    price = Faker(
        "pydecimal", left_digits=5, right_digits=2, min_value=100, max_value=10000
    )
    number_of_rooms = Faker("random_int", min=1, max=5)
    square = Faker(
        "pydecimal", left_digits=3, right_digits=2, min_value=20, max_value=150
    )
    availability = Faker("boolean")
    owner = SubFactory(UserFactory)


def create_users_and_apartments(
    num_users: int = 5, apartments_per_user: int = 3
) -> None:
    """
    Creates users and associated apartments.

    Args:
        num_users: The number of users to create. Defaults to 5.
        apartments_per_user: The number of apartments to create for each user. Defaults to 3.

    Returns:
        None
    """
    try:
        for _ in range(num_users):
            user = UserFactory(password="testpassword")
            logger.info(f"Created user: {user.email}")

            for _ in range(apartments_per_user):
                apartment = ApartmentFactory(owner=user)
                logger.info(
                    f"  Created apartment: {apartment.name} for user: {user.email}"
                )
    except Exception as e:
        logger.error(f"Error creating users and apartments: {e}")


if __name__ == "__main__":
    create_users_and_apartments()
    logger.info("Successfully created users and apartments.")
