from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Apartment(models.Model):
    """
    Represents an apartment available for rent.
    """

    name = models.CharField(max_length=100, db_index=True, verbose_name=_("Name"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    description = models.TextField(verbose_name=_("Description"))
    price = models.DecimalField(
        max_digits=8, decimal_places=2, db_index=True, verbose_name=_("Price")
    )
    number_of_rooms = models.PositiveIntegerField(
        db_index=True, verbose_name=_("Number of rooms")
    )
    square = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name=_("Square")
    )
    availability = models.BooleanField(
        default=True, db_index=True, verbose_name=_("Availability")
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="apartments",
        verbose_name=_("Owner"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        indexes = [
            models.Index(
                fields=["price", "availability"], name="price_availability_idx"
            ),
            models.Index(fields=["slug"], name="slug_idx"),
        ]
        ordering = ["-created_at"]
        verbose_name = _("Apartment")
        verbose_name_plural = _("Apartments")

    def clean(self):
        """
        Performs validation checks on the apartment's fields.

        Raises a ValidationError if any of the fields are invalid.
        """
        super().clean()
        errors = {}

        if self.number_of_rooms == 0:
            errors["number_of_rooms"] = ValidationError(
                _("Number of rooms must be greater than zero."),
                code="invalid_number_of_rooms",
            )
        if self.square <= 0:
            errors["square"] = ValidationError(
                _("Square must be greater than zero."), code="invalid_square"
            )
        if self.price < 0:
            errors["price"] = ValidationError(
                _("Price must be greater than or equal to zero."), code="invalid_price"
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Saves the apartment instance to the database.

        Automatically generates a slug from the name if one is not provided.
        Performs full validation before saving.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        try:
            self.full_clean()
        except ValidationError as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Validation error: {e.messages}")
            raise e
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the apartment.

        Returns:
            str: The name of the apartment.
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the absolute URL for the apartment's detail view.
        """
        from django.urls import reverse

        return reverse("apartment_detail", kwargs={"slug": self.slug})
