from rest_framework import serializers

from rentals.models import Rental


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'
    
    extra_kwargs ={
            'payment': {'read_only': True},                    
        }      
   

class CloseRentalSerializer(serializers.Serializer):
    return_date = serializers.DateField()
    late_fee_per_day = serializers.FloatField()
