from rest_framework import serializers

from medias.models import Media
from rentals.models import Rental


class MediaSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret["artist"]:
            del ret["director"]
        elif ret["director"]:
            del ret["artist"]
        return ret

    class Meta:
        model = Media
        fields = [
            "id",
            "title",
            "release_year",
            "media_type",
            "genre",
            "director",
            "artist",
            "rental_price_per_day",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "available": {"read_only": True, "required": False},
            "condition": {"required": False},
            "director": {"required": False},
            "artist": {"required": False},
        }


class FullMediaSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret["artist"]:
            del ret["director"]
        elif ret["director"]:
            del ret["artist"]
        return ret

    class Meta:
        model = Media
        fields = "__all__"
        extra_kwargs = {"artist": {"default": ""}}


class RentalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ["id", "rental_date", "planned_return_date", "return_date", "user"]


class HistoryRentals(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret["artist"]:
            del ret["director"]
        elif ret["director"]:
            del ret["artist"]
        return ret

    rentals = RentalListSerializer(read_only=True, many=True)

    class Meta:
        model = Media
        fields = [
            "id",
            "title",
            "director",
            "artist",
            "condition",
            "available",
            "rentals",
        ]


class MediaRentalSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret["artist"]:
            del ret["director"]
        elif ret["director"]:
            del ret["artist"]
        return ret

    class Meta:
        model = Media
        fields = ["id", "title", "artist", "director", "available"]
        extra_kwargs = {
            "id": {"read_only": True},
            "available": {"read_only": True, "required": False},
            "director": {"required": False},
            "artist": {"read_only": True, "required": False},
        }
