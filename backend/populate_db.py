import os
import django

# Настройка Django окружения (если скрипт запускается вне Django)
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "config.settings.dev"
)  # Замените your_project_name
django.setup()

from django.contrib.auth import get_user_model
from apps.apartments.models import Apartment
from factory import Factory, Faker, SubFactory
from factory.django import DjangoModelFactory
from django.utils.text import slugify


User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = Faker("email")
    # password не устанавливаем здесь, чтобы использовать set_password
    is_verified = Faker("boolean")
    last_name = Faker("last_name")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Переопределяем метод `_create`, чтобы вызывать `set_password`."""
        password = kwargs.pop("password", None)  # Извлекаем password
        kwargs["first_name"] = kwargs.get("first_name", "")[:50]
        kwargs["last_name"] = kwargs.get("last_name", "")[:50]
        obj = model_class(*args, **kwargs)  # Создаем экземпляр пользователя
        if password:
            obj.set_password(password)  # Устанавливаем пароль
        obj.save()
        return obj


class ApartmentFactory(DjangoModelFactory):
    class Meta:
        model = Apartment

    name = Faker("sentence", nb_words=6)
    # slug генерируется в модели, поэтому не генерируем его здесь
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


def create_users_and_apartments(num_users=5, apartments_per_user=3):
    """
    Creates a specified number of users and apartments.

    Args:
        num_users: Количество пользователей для создания.
        apartments_per_user: Количество квартир для создания для каждого пользователя.
    """
    for i in range(num_users):
        # Создаем пользователя с явно указанным паролем
        user = UserFactory(
            password="testpassword"
        )  # Пароль 'testpassword' для всех пользователей
        print(f"Создан пользователь: {user.email}")

        for _ in range(apartments_per_user):
            apartment = ApartmentFactory(owner=user)
            print(
                f"  Создана квартира: {apartment.name} для пользователя: {user.email}"
            )


if __name__ == "__main__":
    create_users_and_apartments()
    print("Успешно созданы пользователи и квартиры.")
