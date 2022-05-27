from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request, Response
from payments.serializers import PaymentSerializer
from payments.permissions import (IsClient, IsAdmin)
import ipdb
from .models import Payment
from .serializers import PaymentSerializer
from users.models import User
from datetime import date
class paymentCreate(ListCreateAPIView):

    dete_rental_inital = date()
    date_rental_finish = date()
    days = (date_rental_finish - date_rental_inital).days

    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated, IsClient]
    def post(self, request: Request):
        self.request.data


class paymentGet(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated, IsClient|| IsAdmin]
   def get(self,request:Request, payment_id = ''):
       
       ipdb.set_trace() 
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
                payment_list = Payment.objects.all()
                payment_list_serialyzer = PaymentSerializer(payment_list,many = True)
                return Response(payment_list_serialyzer)
        