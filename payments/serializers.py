from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    model = Payment
    fields = '__all__'

