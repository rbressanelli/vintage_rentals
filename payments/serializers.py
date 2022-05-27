from rest_framework import serializers
from users.models import User
from users.serializers import serializers
from Payment.model import Payment
from rentals.serializers import 
class PaymentSerializer(serializers.ModelSerializer):
    user = User()
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