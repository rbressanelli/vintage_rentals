from django.shortcuts import get_object_or_404
from rest_framework import serializers

from addresses.models import Address
from addresses.serializers import AddressSerializer
from users.models import User


class CreateUserByClientSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "cpf",
            "phone",
            "address",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "is_admin": {"required": False, "default": False},
        }

    def create(self, validated_data):
        address_requested = validated_data["address"]
        validated_data.pop("address")
        address = Address.objects.create(**address_requested)
        user = User.objects.create_user(address=address, **validated_data)
        return user


class CreateUserByAdminSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_admin",
            "password",
            "cpf",
            "phone",
            "address",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "is_admin": {"required": True},
        }

    def create(self, validated_data):
        address_requested = validated_data["address"]
        validated_data.pop("address")
        address = Address.objects.create(**address_requested)
        user = User.objects.create_user(address=address, **validated_data)
        return user


class ListUserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_admin",
            "is_active",
            "cpf",
            "phone",
            "address",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UpdateOrRetrieveUserProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_admin",
            "cpf",
            "phone",
            "address",
        ]
        optional_fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "cpf",
            "phone",
            "address",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "is_admin": {"required": False, "read_only": True},
        }

    def update(self, instance, validated_data):
        request = self.context["request"]

        address_data_to_update = validated_data.get("address", None)

        if address_data_to_update != None:
            address_searched = Address.objects.filter(pk=request.user.address.id)

            address_searched.update(**address_data_to_update)

            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.last_name = validated_data.get("last_name", instance.last_name)
            instance.email = validated_data.get("email", instance.email)
            instance.cpf = validated_data.get("cpf", instance.cpf)
            instance.phone = validated_data.get("phone", instance.phone)

            instance.save()

            return instance

        else:
            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.last_name = validated_data.get("last_name", instance.last_name)
            instance.email = validated_data.get("email", instance.email)
            instance.cpf = validated_data.get("cpf", instance.cpf)
            instance.phone = validated_data.get("phone", instance.phone)

            instance.save()
            return instance