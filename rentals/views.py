from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from rentals.models import Rental
from rentals.serializers import RentalSerializer, CloseRentalSerializer
from rentals.permissions import IsAdminUser
from payments.models import Payment
from medias.models import Media
from users.models import User
# from payments.serializers import PaymentSerializer


class RentalView(ListAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]    
    
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer


class CloseRentalView(UpdateAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    
    queryset = Rental.objects.all()
    serializer_class = CloseRentalSerializer

    def update(self, request, pk, *args, **kwargs):
        
        rental = Rental.objects.filter(pk=pk).first()        
        rental.return_date = request.data['return_date']
        returned_date = request.data.pop('return_date')        
        
        media = Media.objects.filter(pk=rental.media_id).first()
        user = User.objects.filter(pk=rental.user_id).first()
        
        rent_days_predicted = returned_date - rental.planned_return_date
        
        
        # serializer = PaymentSerializer(data=request.data['late_fee_per_day'])
        
        # # payment = Payment.objects.filter(rental_id=pk).first()
        
        # rentals.save()
        
        return Response({}, status=status.HTTP_200_OK)
