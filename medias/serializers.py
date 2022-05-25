from rest_framework import serializers
from medias.models import Media
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only':True},
            'available': {'read_only':True, 'required':False},
            'condition': {'required':False},
            'director': {'required':False},
            'artist':{'required':False},
        }