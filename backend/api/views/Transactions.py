from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serialializers import TransactionsSerializer, TransactionsTypesSerializers, TransactionsSerializerCreate
from ..models import Transactions, TransactionType
from ..utils.GetRecords import GetAllRecords, GetRecordsFiltered
import jwt
from django.conf import settings
from django.http import HttpResponseForbidden

secret_key = getattr(settings, 'SECRET_KEY', 'default_value_if_not_set')

@api_view(['GET'])
def GetTransactionsAll(request):
    transactions = GetAllRecords(Transactions, TransactionsSerializer)
    return Response(transactions, status = status.HTTP_200_OK)

@api_view(['GET'])
def GetTransactionTypes(request):
    transactions = GetAllRecords(TransactionType, TransactionsTypesSerializers)
    return Response(transactions, status = status.HTTP_200_OK)

@api_view(['POST'])
def CreateTransaction(request):
    User = request.headers['usertoken']
    User = jwt.decode(User, secret_key, algorithms=['HS256'])
    Data = {
        "User": User['id'],
        "Amount": request.data['Amount'],
        "Title": request.data['Title'],
        "Description": request.data['Description'],
        "Type": request.data['Type'],
        "Category": request.data['Category']
    }
    serializer = TransactionsSerializerCreate(data = Data)
    if serializer.is_valid():
        User = serializer.validated_data['User']
        Amount = serializer.validated_data['Amount']
        Title = serializer.validated_data['Title']
        Description = serializer.validated_data['Description']
        Type = serializer.validated_data['Type']
        Category = serializer.validated_data['Category']

        Transactions.objects.create(
            User = User,
            Amount = Amount,
            Title = Title,
            Description = Description,
            Type = Type,
            Category = Category
        )

        return Response({ 'Message': 'Transaction Succesfully Created'}, status = status.HTTP_201_CREATED)
    return Response({'Message': 'Invalid Body', "error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def GetTransactionsFiltered(request):
    field = request.data.get('field')
    value = request.data.get('value')

    User = request.headers['usertoken']
    if(not User):
        return HttpResponseForbidden("You do not have permission to access this resource.")
    User = jwt.decode(User, secret_key, algorithms=['HS256'])
    
    try:
        records = GetRecordsFiltered(Transactions, TransactionsSerializer, {'name': field, 'value': value}, User['id'])
        return Response({'Data': records},  status = status.HTTP_200_OK)
    except Transactions.DoesNotExist:
        return Response({'Message': 'Not Records', "Data": []}, status = status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def DeleteTransaction(request, id):
    try:
        record = Transactions.objects.get(pk = id)
        Transaction = TransactionsSerializer(record).data
        User = request.headers['usertoken']
        User = jwt.decode(User, secret_key, algorithms=['HS256'])
        if(Transaction["User"] != User["username"]):
            return HttpResponseForbidden("You do not have permission to access this resource.")
    except Transactions.DoesNotExist:
        return Response({'Message': 'Not Records', "Data": []}, status = status.HTTP_404_NOT_FOUND)

    record.delete()
    return Response({'Message': 'Transaction Successfully Deleted'}, status= status.HTTP_200_OK)
    
