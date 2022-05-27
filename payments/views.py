from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request, Response
from payments.serializers import PaymentSerializer
from payments.permissions import (IsClient, IsAdmin)
from .models import Payment
from .serializers import PaymentSerializer
from users.models import User
from rentals.models import Rental
from rentals.serializers import RentalSerializer
import datetime 

class paymentCreate(ListCreateAPIView):

    authentication_classes = [TokenAuthentication] 

    permission_classes = [IsAuthenticated, IsClient]
    
    serializer_class = RentalSerializer
    
    def get_serializer_class(self, request: Request):
     if self.request.method == "POST":
        if not self.request.user.is_authenticated :
            return Response({"error":"not loged"},status.HTTP_401_UNAUTHORIZED)
  
        payment_date = request.data
            
        findUser = get_object_or_404(User, pk = self.request.user.id)
            
        findRental = get_object_or_404(Rental, user = findUser)
           
        findRentalSerializer = RentalSerializer(findRental)

        date_rental_inital = datetime.date(findRentalSerializer.planned_return_date,'%d-%m-%')

        date_rental_finish = datetime.date(datetime.now(),'%d-%m-%Y')
 
        days = (date_rental_finish - date_rental_inital).days

        creat_payment_info = {
                "amount": request.data.amount
                "payment_date": Payment.dateTransform(payment_date)
                "late_fee_per_day": request.data.late_fee_per_day
                "user": ListUserSerializer(findUser)
                "rental": findRentalSerializer
            }
        new_payment =Payment.payment_creation(**creat_payment_info)

        return Response({"menssage":"payment created",
        "total to pay":(new_payment.late_fee_per_day*days)+new_payment.amount},
        status.HTTP_201_CREATED)
            


class paymentGet(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated, IsClient | IsAdmin]
  
   def get(self,request:Request, payment_id = ''):
       
       
       if self.request.IsAdmin:
           if payment_id:
                try:
                   payment_object = Payment.get_object_or_404(id=payment_id)
                   serializer_payment = PaymentSerializer(payment_object)
                   return Response({'mensage':'your payment selected:',serializer_payment.data},status=status.HTTP_200_OK)
                except ObjectDoesNotExist:                    
                    return Response({'errors': 'invalid payment id'}, 
                                     status=status.HTTP_404_NOT_FOUND)
            else:
                payment_list = get_object_or_404(Payment,user = request.user)
                payment_list_serialyzer = PaymentSerializer(payment_list)
                return Response(payment_list_serialyzer)
        