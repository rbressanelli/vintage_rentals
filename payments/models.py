import uuid

from django.db import models


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField(null=False)
    late_fee_per_day = models.FloatField(default=0)
    payment_date = models.DateField(null=False)    
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='payments')
