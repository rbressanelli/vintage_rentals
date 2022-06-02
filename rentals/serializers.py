from rest_framework import serializers

from medias.serializers import MediaRentalSerializer
from payments.serializers import PaymentSerializer
from rentals.models import Rental
from users.serializers import CreateUserByClientSerializer


class RentalSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    rental_date = serializers.DateTimeField(required=False)
    planned_return_date = serializers.DateTimeField(
        format="%d/%m/%Y", input_formats=["%d/%m/%Y", "iso-8601"], required=False
    )
    return_date = serializers.DateTimeField(required=False)

    payment = PaymentSerializer(required=False)

    media = MediaRentalSerializer(required=False)

    user = CreateUserByClientSerializer(required=False)


class ListRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = [
            "id",
            "rental_date",
            "planned_return_date",
            "return_date",
            "user_id",
            "media_id",
        ]


class CloseRentalSerializer(serializers.Serializer):
    return_date = serializers.CharField()
    late_fee_per_day = serializers.FloatField()


class CreateRentalSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    rental_date = serializers.DateTimeField(required=False)
    planned_return_date = serializers.DateTimeField(
        format="%d/%m/%Y", input_formats=["%d/%m/%Y", "iso-8601"], required=False
    )
    return_date = serializers.DateTimeField(required=False)

    media = MediaRentalSerializer(required=False)
