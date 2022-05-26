from django.shortcuts import render
from rest_framework.views import APIView, Response, Request
from rest_framework import status
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import FullMediaSerializer, MediaSerializer
from .models import Media

# Create your views here.
class MediaView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def get_queryset(self):
        
        route_parameter = self.request.GET.get('title', None)
        if route_parameter is not None:
            queryset = Media.objects.filter(
                title__icontains = route_parameter)
            return queryset
        return super().get_queryset()
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullMediaSerializer
        return super().get_serializer_class()

class MediaRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    lookup_url_kwarg = "media_id" 

    
    
