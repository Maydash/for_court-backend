from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes, throttle_classes, APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from datetime import date
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
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'Error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
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

@api_view(['GET', 'PATCH', 'DELETE'])
@throttle_classes([IpThrottle])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_recipient_by_id_delete_patch(request, id):
    try:
        recipient = Recipient.objects.get(id=id)
    except Recipient.DoesNotExist:
        return Response({'ERROR': 'Recipient does NOT exists'}, status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
        print(request.user)
        serializer = RecipientSerializer(recipient, context={'request':request})
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = RecipientSerializer(instance=recipient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'SUCCESS': 'Recipient updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        if recipient.recipient_adder == request.user:
            recipient.delete()
            return Response({'SUCCESS': 'Recipient deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'ERROR': 'User can delete only he\'s added recipients'}, status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([IpThrottle])
def get_all_must_pays(request):
    if request.method == 'GET':
        data = MustPay.objects.all()
        serializer = MustPaySerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([IpThrottle])
def get_mustpay_by_id_patch_delete(request, id):
    try:
        mustpay = MustPay.objects.get(id=id)
    except MustPay.DoesNotExist:
        return Response({'ERROR': 'MustPay does NOT exists'}, status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
        serializer = MustPaySerializer(mustpay, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = MustPaySerializer(instance=mustpay, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'SUCCESS': 'MustPay updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        mustpay.delete()
        return Response({'SUCCESS': 'MustPay deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    # return Response({'ERROR': 'User can delete only he\'s added mustpays'}, status=status.HTTP_400_BAD_REQUEST)

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

class InsolventsSinceThreeMonths(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]

    def get(self, request):
        insolvents = []
        for alimony in Alimony.objects.filter(status=False):
            if (date.today() - alimony.must_pay.receipts.latest().payment_date).days > 90:
                insolvents.append(alimony.must_pay)
        serializer = MustPaySerializer(insolvents, context={'request': request}, many=True)
        return Response(serializer.data)

    # def get(self, request):
    #     unpaids = []
    #     for mustpay in MustPay.objects.all():
    #         if (mustpay.receipts.latest().payment_date - date.today()).days > 90:
    #             unpaids.append(mustpay)
    #     serializer = MustPaySerializer(unpaids, context={'request': request}, many=True)
    #     return Response(serializer.data)

class AlimonyList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [IpThrottle]
    
    def get(self, request):
        alimonies = Alimony.objects.all()
        serializer = AlimonySerializer(alimonies, context={'request': request}, many=True)
        return Response(serializer.data)





























































# @api_view(['POST'])
# @throttle_classes([IpThrottle])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @parser_classes([JSONParser, MultiPartParser, FormParser])
# def add_recipient_child(request):
#     if request.method == 'POST':
#         serializer = RecipientChildSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(child_adder=request.user)
#             return Response({'SUCCESS': 'recipient added successfully.'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @parser_classes([JSONParser])
# def create_models(request):
#     m1_d = request.data.get('recipient')
#     m2_d = request.data.get('child')

#     m1_d_ser = RecipientSerializer(data=m1_d)
#     if m1_d_ser.is_valid():
#         m1 = m1_d_ser.save(recipient_adder=request.user)
#     else:
#         return Response(m1_d_ser.errors, status=status.HTTP_400_BAD_REQUEST)

#     m2_d_ser = RecipientChildSerializer(data=m2_d)
#     if m2_d_ser.is_valid():
#         m2 = m2_d_ser.save(child_adder=request.user, recipient=m1)
#     else:
#         return Response(m2_d_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     # data = {
#     #     'recipient': m1_d_ser(m1).data,
#     #     'child': m2_d_ser(m2).data
#     # }

#     return Response({'ok'}, status=status.HTTP_201_CREATED)
