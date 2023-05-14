from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes, throttle_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import *
from .models import *

class IpThrottle(SimpleRateThrottle):
    rate = '100/min'
    
    def get_cache_key(self, request, view):
        return self.get_ident(request)

@api_view(['GET'])
@throttle_classes([IpThrottle])
def logo_api(request):
    if request.method == 'GET':
        data = Logos.objects.all()
        serializer = LogoSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@throttle_classes([IpThrottle])
def login_api(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            try:
                token = Token.objects.create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            except:
                Token.objects.filter(user=user).delete()
                token = Token.objects.create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response({'ERROR': 'Invalid password'}, status=status.HTTP_417_EXPECTATION_FAILED)

@api_view(['GET'])
@throttle_classes([IpThrottle])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_recipient_by_id(request, id):
    try:
        data = Recipient.objects.get(id=id)
    except Recipient.DoesNotExist:
        return Response({'ERROR': 'Recipient does NOT exists'}, status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
        serializer = RecipientSerializer(data, context={'request':request})
        return Response(serializer.data)

@api_view(['POST'])
@throttle_classes([IpThrottle])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def add_recipient(request):
    if request.method == 'POST':
        serializer = RecipientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'SUCCESS': 'recipient added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@throttle_classes([IpThrottle])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_recipient_children(request, id):
    try:
        recipient = Recipient.objects.get(id=id)
    except Recipient.DoesNotExist:
        return Response({'ERROR': 'Recipient does NOT exists'}, status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
        child = recipient.children.all()
        serializer = RecipientChildSerializer(child, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@throttle_classes([IpThrottle])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_recipient_child_by_id(request, recipient_id, child_id):
    if request.method == 'GET':
        try:
            recipient = Recipient.objects.get(id=recipient_id)
        except Recipient.DoesNotExist:
            return Response({'ERROR': 'Recipient does NOT exists'}, status=status.HTTP_204_NO_CONTENT)
        if request.method == 'GET':
            try:
                child = recipient.children.get(id=child_id)
            except RecipientChild.DoesNotExist:
                return Response({'ERROR': 'Child does NOT exists'}, status=status.HTTP_204_NO_CONTENT)
            serializer = RecipientChildSerializer(child, context={'request': request})
            return Response(serializer.data)

@api_view(['POST'])
@throttle_classes([IpThrottle])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_recipient_child(request):
    if request.method == 'POST':
        serializer = RecipientChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'SUCCESS': 'recipient added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



