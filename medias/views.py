from django.shortcuts import render
from rest_framework.views import APIView, Response, Request
from rest_framework import status
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import FullMediaSerializer, MediaSerializer, HistoryRentals
from .models import Media
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .permissions import IsAdmin
# Create your views here.
class MediaView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'artist', 'director']

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'artist', 'director']
    # def get_queryset(self):
        
    #     route_parameter = self.request.GET.get('title', None)
    #     if route_parameter is not None:
    #         queryset = Media.objects.filter(
    #             title__icontains = route_parameter)
    #         return queryset
    #     return super().get_queryset()
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            medias = Media.objects.filter(available=True).all()
            serializer = MediaSerializer(medias, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        return super().get(request, *args, **kwargs)
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return FullMediaSerializer
        return super().get_serializer_class()
    
   

class MediaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Media.objects.all()
    serializer_class = FullMediaSerializer
    lookup_url_kwarg = "media_id" 


class MediaRentalsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Media.objects.all()
    serializer_class = HistoryRentals
    
    
