from rest_framework import serializers
from .models import *

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logos
        fields = '__all__'