from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    amount = serializers.CharField()
    late_fee_per_day = serializers.FloatField()
    payment_date = serializers.DateField()
    
    rental_id = serializers.UUIDField()
    user_id = serializers.UUIDField()

