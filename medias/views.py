from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.views import Request, Response

from rentals.models import Rental
from rentals.serializers import CreateRentalSerializer
from rentals.services import dateTransform
from users.models import User

from .models import Media
from .permissions import IsAdmin, IsAdminGetMediaRental, IsCustomer
from .serializers import FullMediaSerializer, HistoryRentals, MediaSerializer


class MediaView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["title", "artist", "director"]
    filterset_fields = ["title", "artist", "director"]

    def create(self, request: Request, *args, **kwargs):
        valid = [key for key in request.data.keys()]
        if "artist" in valid and "director" in valid:
            return Response(
                {
                    "error": {
                        "media_type VHS": "Inform only the director",
                        "media_type LP or K7": "Inform only the artist",
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif not "artist" in valid and not "director" in valid:
            return Response(
                {"error": "You must inform an artist or a director"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.data.get("director") and request.data.get("media_type") != "VHS":
            return Response(
                {"error": "Use artist field for LP or K7 media types."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.data.get("artist") and request.data.get("media_type") == "VHS":
            return Response(
                {"error": "Use director field for VHS media types."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def get(self, request: Request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"message": "Unauthorized."}, status.HTTP_401_UNAUTHORIZED)
        if not self.request.user.is_admin:
            medias = Media.objects.filter(available=True).all()
            return super().get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return FullMediaSerializer
        return super().get_serializer_class()


class MediaRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin, IsCustomer]
    queryset = Media.objects.all()
    serializer_class = FullMediaSerializer
    lookup_url_kwarg = "media_id"

    def delete(self, request: Request, *args, **kwargs):
        media = Media.objects.filter(id=kwargs["media_id"]).first()

        if media.available == False:
            return Response(
                {"error": "Cannot delete media rented."}, status.HTTP_400_BAD_REQUEST
            )

        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous or not self.request.user.is_admin:
            return Response({"message": "Unauthorized."}, status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)


class MediaRentalsView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminGetMediaRental]
    queryset = Media.objects.all()
    serializer_class = HistoryRentals
    lookup_url_kwarg = "media_id"


class MediaRentalsCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCustomer]
    queryset = Media.objects.all()
    serializer_class = CreateRentalSerializer

    def create(self, request: Request, *args, **kwargs):
        user = User.objects.filter(email=request.user).first()
        media = Media.objects.filter(id=kwargs["media_id"]).first()
        if media.available == False:
            return Response({"error": "This media is already rented."})
        if user.rental_active == True:
            return Response(
                {
                    "error": "user already has rented media, return media for new rentals."
                },
                status.HTTP_409_CONFLICT,
            )
        request.data["rental_date"] = datetime.now()

        if not request.data.get("planned_return_date"):
            return Response(
                {
                    "error": "User must inform planned_return_date field with a valid date DD/MM/YYYY"
                },
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            first_date = datetime.strptime(
                request.data["planned_return_date"], "%d/%m/%Y"
            ).date()
            second_date = dateTransform(datetime.now())
            if first_date <= second_date:
                return Response(
                    {"error": "Invalid date, return date must be after current date."}, status.HTTP_400_BAD_REQUEST
                )
        except ValueError as err:
            return Response({"error": err.args}, status.HTTP_400_BAD_REQUEST)
        
        media.available = False
        media.save()
        user.rental_active = True
        user.save()
        serializer = CreateRentalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["media"] = media
        serializer.validated_data["user"] = user
        rental = Rental.objects.create(**serializer.validated_data)
        serializer = CreateRentalSerializer(rental)
        return Response(serializer.data, status.HTTP_201_CREATED)
