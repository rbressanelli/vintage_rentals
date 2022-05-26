from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView, RetrieveUpdateAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request, Response

from users.models import User
from users.permissions import IsAdmin
from users.serializers import (CreateUserByAdminSerializer,
                               CreateUserByClientSerializer,
                               ListUserSerializer, LoginSerializer,
                               UpdateOrRetrieveUserProfileSerializer)


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


class DeactivateUserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
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
