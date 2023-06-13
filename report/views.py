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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([IpThrottle])
def recipient_detail(request, id):
    if request.method == 'GET':
        try:
            alimony = Alimony.objects.get(id=id)
        except Alimony.DoesNotExist:
            return Response({'no data'})
        recipient = Recipient.objects.get(id=alimony.recipient.id)
        serializer = RecipientSerializer(recipient, context={'request':request})
        return Response(serializer.data)

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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([IpThrottle])
def mustpay_detail(request, id):
    if request.method == 'GET':
        try:
            alimony = Alimony.objects.get(id=id)
        except Alimony.DoesNotExist:
            return Response({'no data'})
        mustpay = MustPay.objects.get(id=alimony.must_pay.id)
        serializer = MustPaySerializer(mustpay, context={'request':request})
        return Response(serializer.data)

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
        try:
            insolvents = []
            for alimony in Alimony.objects.filter(status=False):
                try:
                    if(date.today() - alimony.must_pay.receipts.latest().payment_date).days > 90:
                        insolvents.append(alimony.must_pay)
                except AssertionError:
                    return Response({'aa'})
                serializer = MustPaySerializer(insolvents, context={'request':request}, many=True)
                return Response(serializer.data)
        except AssertionError:
            return Response({'ok'})


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
@parser_classes([MultiPartParser, FormParser, JSONParser])
@throttle_classes([IpThrottle])
def add_alimony(request):
    if request.method == 'POST':
        recipient = {
            'name_and_lastname': request.POST['recipient[name_and_lastname]'],
            'birthday': request.POST['recipient[birthday]'],
            'phone_number': request.POST['recipient[phone_number]'],
            'address': request.POST['recipient[address]'],
            'document_scan': request.FILES['recipient[document_scan]']
        }
        mustpay = {
            'name_and_lastname': request.POST['mustpay[name_and_lastname]'],
            'birthday': request.POST['mustpay[birthday]'],
            'phone_number': request.POST['mustpay[phone_number]'],
            'phone_number2': request.POST['mustpay[phone_number2]'],
            'address': request.POST['mustpay[address]'],
            'job_status': request.POST['mustpay[job_status]'],
            'document_scan': request.FILES['mustpay[document_scan]']
        }
        alimony = {
            'Category': request.POST['alimony[Category]'],
            'ruling': request.POST['alimony[ruling]'],
            'ruling_date': request.POST['alimony[ruling_date]'],
            'began_paying': request.POST['alimony[began_paying]'],
            'ruling_scan': request.FILES['alimony[ruling_scan]'],
            'executor': request.POST['alimony[executor]'],
            'executor_register': request.POST['alimony[executor_register]'],
            'executor_date': request.POST['alimony[executor_date]'],
            'note': request.POST['alimony[note]']
        }
        recipient_serializer = RecipientSerializer(data=recipient)
        mustpay_serializer = MustPaySerializer(data=mustpay)
        alimony_serializer = AlimonySerializer(data=alimony)
        if recipient_serializer.is_valid() and mustpay_serializer.is_valid() and alimony_serializer.is_valid():
            addedRecipient = recipient_serializer.save(recipient_adder=request.user)
            addedMustPay = mustpay_serializer.save(mustpay_adder=request.user)
            alimony_serializer.save(user=request.user, recipient=addedRecipient, must_pay=addedMustPay)
            return Response({'SUCCESS': 'Submitted sucessfully!'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def pass_undefined(request):
    if request.method == 'GET':
        return Response({'reload'})