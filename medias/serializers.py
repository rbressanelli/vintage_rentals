from rest_framework import serializers
from medias.models import Media
from rentals.models import Rental
from users.models import User
# from rentals.serializers import RentalSerializer
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['title', 'release_year',
                 'genre', 'director', 'artist',
                 'rental_price_per_day']
        extra_kwargs = {
            'id': {'read_only':True},
            'available': {'read_only':True, 'required':False},
            'condition': {'required':False},
            'director': {'required':False},
            'artist':{'required':False},
        }

class FullMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
        extra_kwargs = {
            'artist': {'default': ''}
        }

# class UserUUIDSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id']

class RentalListSerializer(serializers.ModelSerializer):
    # user_id = UserUUIDSerializer()
    class Meta:
        model = Rental
        fields = ['id', 'rental_date', 'planned_return_date', 'return_date', 'user']


class HistoryRentals(serializers.ModelSerializer):
    rentals = RentalListSerializer(read_only=True, many=True)
    class Meta:
        model = Media
        fields = ['id', 'title', 'director', 'artist', 'condition', 'available', 'rentals']
