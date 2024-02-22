from rest_framework import serializers
from ihr_api import models


class ClientProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'
