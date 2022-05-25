import uuid

from django.db import models


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street = models.CharField(max_length=255,null=False)
    complement = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    zip_code = models.CharField(max_length=25, null=False)
    country = models.CharField(max_length=100, null=False)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
      model = Address
      fields = '__all__'
      extra_kawargs = {
        "id" :  {"read_only"=True}
        "street" :{'required':True}
        "complement" :  {'required':True}
        "city" :{'required':True}
        "state" :  {'required':True}
        "zip_code" : {'required':True}
        "country" : {'required':True}
            }
