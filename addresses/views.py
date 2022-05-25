from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
# Create your views here.
class addresses(APIView):
    def get(self, request: Request):
        ...
    def post(self, request: Request):
        ...
    def patch(self, request: Request):
        ...
