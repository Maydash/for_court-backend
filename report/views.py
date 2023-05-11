from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import *
from .models import *

@api_view(['GET'])
def logo_api(request):
    if request.method == 'GET':
        data = Logos.objects.all()
        serializer = LogoSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['POST'])
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

