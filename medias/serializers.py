from rest_framework import serializers
from medias.models import Media
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


class HistoryRentals(serializers.ModelSerializer):
    # rental_history = RentalSerializer()
    class Meta:
        model = Media
        fields = ['id', 'title', 'director', 'artist', 'condition', 'available', 'rental_history']

