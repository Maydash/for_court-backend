from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .views import IpThrottle
from .serializers import *
from .models import *
from .models import *
import django_filters

class FilterRecipients(django_filters.FilterSet):
    name_and_lastname = django_filters.CharFilter(lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Recipient
        fields = [
            'name_and_lastname',
            'birthday',
            'phone_number',
            'address'
        ]

class FilterMustPays(django_filters.FilterSet):
    name_and_lastname = django_filters.CharFilter(lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = MustPay
        fields = [
            'name_and_lastname',
            'birthday',
            'phone_number',
            'address'
        ]

class FilterAlimonies(django_filters.FilterSet):
    Category = django_filters.CharFilter(field_name='Category__name')

    class Meta:
        model = Alimony
        fields = [
            'Category',
            'ruling',
            'ruling_date',
            'began_paying',
            'executor',
            'executor_register',
            'executor_date',
            'must_pay',
            'recipient',
            'created_at'
        ]

class FilteringAlimony(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]

    def get(self, request):
        queryset = Alimony.objects.filter(status=False).order_by('-id')
        filterset = FilterAlimonies(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        serializer = AlimonySerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

class FilteringRecipient(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]

    def get(self, request):
        queryset = Recipient.objects.filter(alimonies__status=False).order_by('-id')
        filterset = FilterRecipients(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        serializer = RecipientSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

class FilteringMustPay(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]

    def get(self, request):
        queryset = MustPay.objects.filter(alimonies__status=False).order_by('-id')
        filterset = FilterMustPays(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        serializer = MustPaySerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)