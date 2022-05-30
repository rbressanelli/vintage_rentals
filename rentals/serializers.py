from rest_framework import serializers
from payments.serializers import PaymentSerializer

from users.serializers import CreateUserByClientSerializer, MediaForRentalListSerializer


class RentalSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    rental_date = serializers.DateTimeField()
    planned_return_date = serializers.DateTimeField()
    return_date = serializers.DateTimeField()    
    
    payment = PaymentSerializer()
    
    media = MediaForRentalListSerializer() 
    
    user = CreateUserByClientSerializer() 
