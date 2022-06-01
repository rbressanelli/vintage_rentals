from pkg_resources import require
from rest_framework import serializers
from payments.serializers import PaymentSerializer
from rentals.models import Rental

from users.serializers import CreateUserByClientSerializer, MediaForRentalListSerializer


class RentalSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    rental_date = serializers.DateTimeField()
    planned_return_date = serializers.DateTimeField()
    return_date = serializers.DateTimeField()    
    
    payment = PaymentSerializer()
    
    media = MediaForRentalListSerializer() 
    
    user = CreateUserByClientSerializer() 


class ListRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = [
            'id', 'rental_date', 'planned_return_date', 'return_date', 'user_id', 'media_id',        
            ]


class CloseRentalSerializer(serializers.Serializer):
    return_date = serializers.CharField()
    late_fee_per_day = serializers.FloatField()
