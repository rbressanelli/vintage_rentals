import uuid

from django.db import models


class Rental(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_date = models.DateTimeField(auto_now_add=True)
    planned_return_date = models.DateTimeField()
    return_date = models.DateTimeField(default=None, blank=True, null=True)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rentals",
        null=True,
        unique=False,
    )

    media = models.ForeignKey(
        "medias.Media",
        on_delete=models.CASCADE,
        related_name="rentals",
        null=True,
        unique=False,
    )

    payment = models.OneToOneField(
        "payments.Payment", on_delete=models.CASCADE, null=True, unique=True
    )
