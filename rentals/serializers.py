from rest_framework import serializers


class RentalSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    rental_date = serializers.DateField()
    planned_return_date = serializers.DateField()
    return_date = serializers.DateField()
    media_id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    payment = PaymentSerializer(read_only=True)
    

class CloseRentalSerializer(serializers.Serializer):
    return_date = serializers.DateField()
    late_fee_per_day = serializers.FloatField()
