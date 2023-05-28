from rest_framework import serializers
from .models import *

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logos
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'

        extra_kwargs = {'recipient_adder': {
            'required': False
        }}

class RecipientChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipientChild
        fields = '__all__'

        extra_kwargs = {'recipient': {
            'required': False
        }}

class MustPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MustPay
        fields = '__all__'

        extra_kwargs = {'mustpay_adder': {
            'required': False
        }}

class MustPayReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = MustPayReceipt
        fields = '__all__'

class AlimonySerializer(serializers.ModelSerializer):
    class Meta:
        model = Alimony
        fields = '__all__'

        extra_kwargs = {
            'user': {
                'required': False
        },
            'must_pay': {
                'required': False
            },
            'recipient': {
                'required': False
            }
        }
