from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    amount = serializers.CharField()
    late_fee_per_day = serializers.FloatField()
    payment_date = serializers.DateField()
