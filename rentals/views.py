import datetime

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from medias.models import Media
from payments.models import Payment
from payments.serializers import PaymentSerializer
from rentals.models import Rental
from rentals.permissions import IsAdminUser
from rentals.serializers import (CloseRentalSerializer, ListRentalSerializer,
                                 RentalSerializer)
from users.models import User

from .services import dateTransform, verify_uuid


class RentalView(ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Rental.objects.all()
    serializer_class = ListRentalSerializer

    def list(self, _, *args, **kwargs):

        rental = Rental.objects.all()
        serializer = ListRentalSerializer(rental, many=True)

        return Response({"rental_history": serializer.data})


class CloseRentalView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        if not verify_uuid(pk):
            return Response(
                {"error": "UUID must be a valid uuid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        close_rental_serializer = CloseRentalSerializer(data=request.data)
        close_rental_serializer.is_valid(raise_exception=True)

        rental = Rental.objects.filter(pk=pk).first()
        returned_date = request.data.pop("return_date")

        if not rental:
            return Response(
                {"error": "Rental not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        media = Media.objects.filter(pk=rental.media_id).first()
        user = User.objects.filter(pk=rental.user_id).first()

        returned_date = datetime.datetime.strptime(returned_date, "%d/%m/%Y")
        rental.return_date = returned_date.replace(tzinfo=datetime.timezone.utc)
        returned_date = returned_date.date()
        planned_return_date = dateTransform(rental.planned_return_date)
        rental_date = dateTransform(rental.rental_date)
        
        if planned_return_date >= returned_date:
            number_days_no_fee = returned_date - rental_date
            amount = number_days_no_fee.days * media.rental_price_per_day
        else:
            number_days_no_fee = planned_return_date - rental_date
            fee = (returned_date - planned_return_date).days * request.data[
            "late_fee_per_day"]
            amount = number_days_no_fee.days * media.rental_price_per_day
            amount = amount + fee       

        user.rental_active = False
        user.save()
        media.available = True
        media.save()

        request.data["amount"] = f"{amount:.2f}"
        request.data["payment_date"] = returned_date

        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        payment = Payment.objects.create(**serializer.validated_data, user=user)
        serializer = PaymentSerializer(payment)

        rental.payment = payment
        rental.save()

        rental_serializer = RentalSerializer(rental)

        return Response(rental_serializer.data, status=status.HTTP_200_OK)
