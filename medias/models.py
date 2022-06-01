import uuid
from django.db import models

class CleanModel(models.Model):
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save()


class Media(CleanModel):
    
    MEDIA_TYPES = (
        ('LP', 'Long Play'), 
        ('K7', 'Fita Cassete'), 
        ('VHS', 'Fita de Vídeo'),
        )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, unique=True, null=False)
    release_year = models.CharField(max_length=4, null=False)
    genre = models.CharField(max_length=100, null=False)
    media_type = models.CharField(max_length=3, choices=MEDIA_TYPES)
    director = models.CharField(max_length=255, null=True, blank=True, default="")
    artist = models.CharField(max_length=255, null=True, blank=True, default="")
    rental_price_per_day = models.FloatField(null=False)
    condition = models.CharField(max_length=255, default='good')
    available = models.BooleanField(null=False, default=True)
