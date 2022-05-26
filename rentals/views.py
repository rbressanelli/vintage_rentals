from django.shortcuts import render
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from rentals.models import Rental
from rentals.serializers import RentalSerializer, CloseRentalSerializer
from rentals.permissions import IsAdminUser


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

    def update(self, request, *args, **kwargs):
        
        
        return super().update(request, *args, **kwargs)
