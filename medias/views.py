from django.shortcuts import render
from rest_framework.views import APIView, Response, Request
from rest_framework import status
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from datetime import datetime
from .serializers import FullMediaSerializer, MediaSerializer, HistoryRentals
from .models import Media
from rentals.models import Rental
from rentals.serializers import CreateRentalSerializer, RentalSerializer
from users.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .permissions import IsAdmin, IsCustomer
from rest_framework.exceptions import PermissionDenied
from rentals.services import dateTransform
# Create your views here.
class MediaView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'artist', 'director']
    filterset_fields = ['title', 'artist', 'director']
    def create(self, request, *args, **kwargs):
        valid = [ key for key in request.data.keys() ]
        if 'artist' in valid and 'director' in valid:
            return Response({'error': {
                'media_type VHS': 'Inform only the director',
                'media_type LP or K7': 'Inform only the artist'
            }}, status=status.HTTP_400_BAD_REQUEST)
        elif not 'artist' in valid and not 'director' in valid:
            return Response({'error': 'You must inform an artist or a director'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('director') and request.data.get('media_type').upper() != 'VHS':
            return Response({'error': 'Use artist field for LP or K7 media types.'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('artist') and request.data.get('media_type').upper() == 'VHS':
            return Response({'error': 'Use director field for VHS media types.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
  
    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"message": "Unauthorized."},status.HTTP_401_UNAUTHORIZED)
        if not self.request.user.is_admin:
            medias = Media.objects.filter(available=True).all()
            serializer = MediaSerializer(medias, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        return super().get(request, *args, **kwargs)
    def get_serializer_class(self):
        if self.request.user.is_admin:
            return FullMediaSerializer
        return super().get_serializer_class()
    
   

class MediaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Media.objects.all()
    serializer_class = FullMediaSerializer
    lookup_url_kwarg = "media_id" 


class MediaRentalsView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Media.objects.all()
    serializer_class = HistoryRentals
    lookup_url_kwarg = "media_id" 
    
class MediaRentalsCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCustomer]
    queryset = Media.objects.all()
    serializer_class = CreateRentalSerializer
    def create(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.user).first()
        media = Media.objects.filter(id=kwargs['media_id']).first()
        if media.available == False:
            return Response({"error": "This media is already rented."})
        request.data['rental_date'] = datetime.now()
        first_date = datetime.strptime(request.data['planned_return_date'], '%d/%m/%Y').date()
        second_date = dateTransform(datetime.now())
        if first_date < second_date:
            return Response({"error":"Invalid date, return date less than current date."})
   
        media.available = False
        media.save()
        user.rental_active = True
        user.save()
        serializer = CreateRentalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['media'] = media
        serializer.validated_data['user'] = user
        rental = Rental.objects.create(**serializer.validated_data)
        serializer = CreateRentalSerializer(rental)
        return Response(serializer.data, status.HTTP_201_CREATED)
