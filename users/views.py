from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView, RetrieveUpdateAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request, Response

from rentals.models import Rental
from users.models import User
from users.permissions import IsAdmin, IsClient
from users.serializers import (CreateUserByAdminSerializer,
                               CreateUserByClientSerializer,
                               ListUserSerializer, LoginSerializer,
                               RentalForRentalListSerializer,
                               UpdateOrRetrieveUserProfileSerializer,
                               UserUUIDSerializer)


class RegisterAndListUsersView(ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]
    serializer_class = UpdateOrRetrieveUserProfileSerializer

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            if self.request.user.is_authenticated and self.request.user.is_admin:
                return CreateUserByAdminSerializer
            return CreateUserByClientSerializer
        return ListUserSerializer


class LoginUserView(APIView):
    def post(self, request: Request):

        user_login_serializer = LoginSerializer(data=request.data)
        user_login_serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=user_login_serializer.validated_data["email"],
            password=user_login_serializer.validated_data["password"],
        )

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class GetUserProfileOrUpdateUserProfileView(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UpdateOrRetrieveUserProfileSerializer

    def get_object(self):
        queryset = get_object_or_404(User, pk=self.request.user.id)
        return queryset

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class DeactivateUserProfileView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        userLogged = User.objects.filter(email=request.user.email).first()
        userLogged.is_active = False
        userLogged.save()
        return Response(
            {"message": "User has been deactivated."}, status=status.HTTP_200_OK
        )


class FilterUserByUserIdView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    serializer_class = ListUserSerializer

    lookup_field = "user_id"

    def get_object(self):
        user_param = self.kwargs["user_id"]
        queryset = get_object_or_404(User, pk=user_param)
        return queryset


class FilterUserRentalHistoryByUserIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, user_id=""):
        uuid_serializer = UserUUIDSerializer(data={"uuid": user_id})

        if not uuid_serializer.is_valid():
            return Response(
                {"message": "URL parameter must be a valid UUID"},
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_filtered = get_object_or_404(User, pk=user_id)
            user_serializer = ListUserSerializer(user_filtered)
            rental_filtered = Rental.objects.filter(user=user_filtered)
            rental_serializer = RentalForRentalListSerializer(
                rental_filtered, many=True
            )

            return Response(
                {
                    "user": user_serializer.data,
                    "rental_history": rental_serializer.data,
                },
                status.HTTP_200_OK,
            )

        except Http404:
            return Response(
                {"message": "User does not exist"}, status.HTTP_404_NOT_FOUND
            )


class GetLoggedUserRentalHistoryView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsClient]

    serializer_class = RentalForRentalListSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            {"rental_history": self.list(request, *args, **kwargs).data},
            status.HTTP_200_OK,
        )

    def get_queryset(self):
        queryset_user = get_object_or_404(User, pk=self.request.user.id)
        return Rental.objects.filter(user=queryset_user)
