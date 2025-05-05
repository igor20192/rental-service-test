from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _  # Для интернационализации


class Apartment(models.Model):
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
        super().clean()
        if self.number_of_rooms == 0:
            raise ValidationError(_("Number of rooms must be greater than zero."))
        if self.square <= 0:
            raise ValidationError(_("Square must be greater than zero."))
        if self.price < 0:
            raise ValidationError(_("Price must be greater than or equal to zero."))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("apartment_detail", kwargs={"slug": self.slug})
