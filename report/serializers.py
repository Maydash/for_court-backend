from rest_framework import serializers
from .models import *

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logos
        fields = '__all__'
    
class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ('id',
                  'name_and_lastname',
                  'phone_number',
                  'birthday',
                  'address',
                  'document_scan',
                  'recipient_adder')

        extra_kwargs = {'recipient_adder':{
            'required': False
        }}

class RecipientChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipientChild
        fields = '__all__'

        extra_kwargs = {'recipient':{
            'required': False
        }}

class MustPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MustPay
        fields = '__all__'