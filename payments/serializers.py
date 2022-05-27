from rest_framework import serializers
from users.models import User
from users.serializers import serializers
from Payment.model import Payment
from rentals.serializers import Rental

class PaymentSerializer(serializers.ModelSerializer):
    user = User()
    rental = Rental()
  #  rental = rentals()
    class Meta:
        model = Payment
        fields =  [
    "id",
    "amount",
    "late_fee_per_day",
    "payment_date"
    ]
     extra_kwargs = { 
    "id"{"read_only": True},
    "amount"{"required":True,},
    "late_fee_per_day"{"required":True,"default":1,99},
    "payment_date":{"required":True}
    }
    def dateTransform(data):
        temp = datetime.datetime.strftime(data, '%Y-%m-%d')
        return datetime.datetime.strptime(temp, '%Y-%m-%d').date()

    def payment_creation(self, validated_data):
        user_requested = validated_data["user"]
        rental_requested = validated_data["rental"]
        validated_data.pop("user")
        validated_data.pop("rental")
        payment_crated = Payment.objects.create(user=user_requested,rental=rental_requested, **validated_data)
        return payment_crated