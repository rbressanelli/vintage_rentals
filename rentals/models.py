import uuid

from django.db import models


class Rental(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rental_date = models.DateField(auto_now_add=True)
    planned_return_date = models.DateField()
    return_date = models.DateField(default=None)
    
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='rentals', null=True
    )
    
    media = models.ForeignKey(
        'medias.Media', on_delete=models.CASCADE, related_name='rentals', null=True
    )    
    