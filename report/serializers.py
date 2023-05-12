from rest_framework import serializers
from .models import *

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logos
        fields = '__all__'
    
class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'

class RecipientChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipientChild
        fields = '__all__'