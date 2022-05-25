from rest_framework import serializers


class Address_Serializer(serializers.Address_Serializer):
    id =  serializers.UUIDField(read_only=True)
    street =  serializers.CharField(required=True)
    complement =  serializers.CharField(required=True)
    city =  serializers.CharField(required=True)
    state =  serializers.CharField(required=True)
    zip_code =  serializers.CharField(required=True)
    country =  serializers.CharField(required=True)