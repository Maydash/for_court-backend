from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes, throttle_classes, APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from datetime import date
from .serializers import *
from .paginators import *
from .models import *

class IpThrottle(SimpleRateThrottle):
    rate = '100/min'
    
    def get_cache_key(self, request, view):
        return self.get_ident(request)

class LogoAPI(APIView):
    throttle_classes = [IpThrottle]

    def get(self, request):
        data = Logos.objects.all()
        serializer = LogoSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)

class CategoryList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, context={'request': request}, many=True)
        return Response(serializer.data)

class LoginAPI(APIView):
    throttle_classes = [IpThrottle]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'Error': 'User is unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        if check_password(password, user.password):
            try:
                token = Token.objects.create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            except:
                token = Token.objects.get(user=user)
                # Token.objects.filter(user=user).delete()
                # token = Token.objects.create(user=user)
                # return Response({'token': token.key}, status=status.HTTP_201_CREATED)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)

        else:
            return Response({'ERROR': 'Invalid password'}, status=status.HTTP_417_EXPECTATION_FAILED)

class RecipientDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    lookup_field = 'id'

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

@api_view(['GET', 'PATCH', 'DELETE'])
@throttle_classes([IpThrottle])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_recipient_child_by_id_update_delete(request, recipient_id, child_id):
    try:
        recipient = Recipient.objects.get(id=recipient_id)
    except Recipient.DoesNotExist:
        return Response({'ERROR': 'Recipient does NOT exists'}, status=status.HTTP_204_NO_CONTENT)
    try:
        child = recipient.children.get(id=child_id)
    except RecipientChild.DoesNotExist:
        return Response({'ERROR': 'Child does NOT exists'}, status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
        serializer = RecipientChildSerializer(child, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = RecipientChildSerializer(instance=child, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'SUCCESS': 'Child updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        if child.child_adder == request.user:
            child.delete()
            return Response({'SUCCESS': 'Child deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'ERROR': 'User can delete only he\'s added children'}, status=status.HTTP_400_BAD_REQUEST)

class MustPayList(ListAPIView):
    queryset = MustPay.objects.all().order_by('-id')
    serializer_class = MustPaySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]
    pagination_class = PaginatorConfig

class MustPayDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]
    queryset = MustPay.objects.all()
    serializer_class = MustPaySerializer
    lookup_field = 'id'

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([IpThrottle])
def get_mustpay_receipts(request, id):
    try:    
        mustpay = MustPay.objects.get(id=id)
    except MustPay.DoesNotExist:
        return Response({'ERROR': 'Must pay does not exists'}, status=status.HTTP_204_NO_CONTENT)
    receipts = mustpay.receipts.all()
    serializer = MustPayReceiptSerializer(receipts, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PATCH', 'DELETE'])
@throttle_classes([IpThrottle])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_receipt__by_id_update_delete(request, mustpay_id, receipt_id):
    try:
        mustpay = MustPay.objects.get(id=mustpay_id)
    except MustPay.DoesNotExist:
        return Response({'ERROR': 'Must pay does NOT exists'}, status=status.HTTP_204_NO_CONTENT)
    try:
        receipt = mustpay.receipts.get(id=receipt_id)
    except MustPayReceipt.DoesNotExist:
        return Response({'ERROR': 'Receipt does NOT exists'}, status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
        serializer = MustPayReceiptSerializer(receipt, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = MustPayReceiptSerializer(instance=receipt, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'SUCCESS': 'Receipt updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        receipt.delete()
        return Response({'SUCCESS': 'Child deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'ERROR': 'User can delete only he\'s added children'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def InsolventsSinceThreeMonths(request):
    if request.method == 'GET':
        insolvents = []
        for alimony in Alimony.objects.filter(status=False):
            try:
                if(date.today() - alimony.must_pay.receipts.latest().payment_date).days > 90:
                    insolvents.append(alimony.must_pay)
            except MustPayReceipt.DoesNotExist:
                pass
            serializer = MustPaySerializer(insolvents, context={'request':request}, many=True)
            return Response(serializer.data)


class AlimonyList(ListAPIView):
    queryset = Alimony.objects.filter(status=False).order_by('-id')
    serializer_class = AlimonySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]
    pagination_class = PaginatorConfig

class AlimonyDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]
    queryset = Alimony.objects.all()
    serializer_class = AlimonySerializer
    lookup_field = 'id'

class ArchiveList(ListAPIView):
    queryset = Alimony.objects.filter(status=True).order_by('-id')
    serializer_class = AlimonySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]
    pagination_class = PaginatorConfig

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def create_alimony(request):
    if request.method == 'POST':
        recipient = request.data.get('recipient')
        mustpay = request.data.get('mustpay')
        alimony = request.data.get('alimony')
        serializerRecipient = RecipientSerializer(data=recipient)
        if serializerRecipient.is_valid():
            completedRecipient = serializerRecipient.save(recipient_adder=request.user)
        else:
            return Response(serializerRecipient.errors, status=status.HTTP_400_BAD_REQUEST)
        serializerMustpay = MustPaySerializer(data=mustpay)
        if serializerMustpay.is_valid():
            completedMustpay = serializerMustpay.save(mustpay_adder=request.user)
        else:
            completedRecipient.delete()
            return Response(serializerMustpay.errors, status=status.HTTP_400_BAD_REQUEST)
        serializerAlimony = AlimonySerializer(data=alimony)
        if serializerAlimony.is_valid():
            serializerAlimony.save(user=request.user, must_pay=completedMustpay, recipient=completedRecipient)
            return Response({'SUCCESS': 'Alimony created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            completedRecipient.delete()
            completedMustpay.delete()
            return Response(serializerAlimony.errors, status=status.HTTP_400_BAD_REQUEST)
