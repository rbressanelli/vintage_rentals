from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
import datetime


from rentals.models import Rental
from rentals.serializers import RentalSerializer, CloseRentalSerializer
from rentals.permissions import IsAdminUser
from payments.models import Payment
from medias.models import Media
from users.models import User
from payments.serializers import PaymentSerializer
from .services import dateTransform

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
        
        returned_date = datetime.datetime.strptime(returned_date, '%d/%m/%Y').date()                              
        
        planned_return_date = dateTransform(rental.planned_return_date)       
        rental_date = dateTransform(rental.rental_date)
        
        returned_date_no_fee = returned_date - rental_date 
        
        fee = (returned_date - planned_return_date).days * request.data['late_fee_per_day'] 
        
        amount = returned_date_no_fee.days * media.rental_price_per_day          
               
        amount = amount + fee
        print(f'{amount:.2f}')
        # user.rental_active = False        
        # user.save()
        # media.available = False
        # media.save()        
        
        request.data['amount'] = f'{amount:.2f}'
        request.data['late_fee_per_day'] = request.data['late_fee_per_day']
        request.data['payment_date'] = returned_date
        
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # if not serializer.is_valid():
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # print(serializer.data)
        # payment = Payment.objects.create(**serializer.validated_data)
        
        
        return Response({}, status=status.HTTP_200_OK)
