from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serialializers import CustomUserSerializer, CustomUserSerializerCreate, AccountTypesSerializer
from ..models import CustomUser, AccountTypes
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
import jwt
from django.conf import settings
from ..utils.GetRecords import GetAllRecords

secret_key = getattr(settings, 'SECRET_KEY', 'default_value_if_not_set')

@api_view(['GET'])
def Users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many= True)
    return Response(serializer.data, status= status.HTTP_200_OK)

@api_view(['GET'])
def GetAccountTypes( request ):
    transactions = GetAllRecords(AccountTypes, AccountTypesSerializer)
    return Response(transactions, status = status.HTTP_200_OK)

@api_view(['POST'])
def AuthUser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username = username, password = password)
    if user is not None:
        UserData =  CustomUserSerializer(user).data
        UserData = jwt.encode(UserData, secret_key, algorithm='HS256')
        return Response({ 'User': UserData, 'IsAuth': True }, status= status.HTTP_200_OK)
    return Response({ 'password': password, 'username': username, 'IsAuth': False }, status= status.HTTP_200_OK)

@api_view(['POST'])
def CreateUser( request ):
    serializer = CustomUserSerializerCreate(data= request.data)

    if(serializer.is_valid()):
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        firstName = serializer.validated_data['first_name']
        lastName = serializer.validated_data['last_name']
        email = serializer.validated_data['email']
        accountType = serializer.validated_data['Account_type']
        Budget = serializer.validated_data['Budget']
        Limit = serializer.validated_data['Limit']

        CustomUser.objects.create(
            username = username,
            password = password,
            first_name = firstName,
            last_name = lastName,
            email = email,
            Account_type = accountType, 
            Budget = Budget,
            Limit = Limit
        )

        return Response({ 'Message': 'User Succesfully Created'}, status = status.HTTP_201_CREATED)
    return Response({'Message': 'Invalid Body', "error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def DeactivateUser( request ):
    usertoken = request.headers.get('usertoken')
    userdecoded = jwt.decode(usertoken, secret_key, algorithms=['HS256'])
    try:
        user = CustomUser.objects.get(pk=userdecoded["id"])
        user.is_active = False
        user.save()
        user = CustomUserSerializer(user).data
        user = jwt.encode(user, secret_key, algorithm='HS256')
        return Response({'Message': 'Succesfull', 'User': user}, status = status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'Message': 'User Not Found'}, status = status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def UpdateFieldUser( request, field ):
    usertoken = request.headers['usertoken']
    username = jwt.decode(usertoken, secret_key, algorithms=['HS256'])['username']
    match field:
        case "Password":
            old_password = request.data.get('oldPassword')
            new_password = request.data.get('newPassword')

            if (old_password is None or new_password is None or username is None):
                return Response(status= status.HTTP_400_BAD_REQUEST)

            user = authenticate(username = username, password = old_password)
            if (user is not None):
                user.set_password(new_password)
                user.save()
                user = CustomUserSerializer(user).data
            else:
                return Response({'Message': 'Current Password is Incorrect'}, status = status.HTTP_404_NOT_FOUND)
        
        case "Username":
            new_username = request.data.get('newUsername')

            if(new_username is None or username is None):
                return Response(status= status.HTTP_400_BAD_REQUEST)                
            
            try:
                user = CustomUser.objects.get(username = username)  
                user.username = new_username   
                user.save()
                user = CustomUserSerializer(user).data
            except CustomUser.DoesNotExist:
                return Response({'Message': 'User Not Found'}, status = status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({'Message': 'Integrity Error'}, status = status.HTTP_404_NOT_FOUND)
            
        case "First_Name":
            first_name = request.data.get('firstName')

            if(username is None or first_name is None):
                return Response(status= status.HTTP_400_BAD_REQUEST)                
            
            try:
                user = CustomUser.objects.get(username = username)  
                user.first_name = first_name
                user.save()
                user = CustomUserSerializer(user).data
            except CustomUser.DoesNotExist:
                return Response({'Message': 'User Not Found'}, status = status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({'Message': 'Integrity Error'}, status = status.HTTP_404_NOT_FOUND)
        case "Last_Name":
            last_name = request.data.get('lastName')

            if(username is None or last_name is None):
                return Response(status= status.HTTP_400_BAD_REQUEST)                
            
            try:
                user = CustomUser.objects.get(username = username)  
                user.last_name = last_name
                user.save()
                user = CustomUserSerializer(user).data
            except CustomUser.DoesNotExist:
                return Response({'Message': 'User Not Found'}, status = status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({'Message': 'Integrity Error'}, status = status.HTTP_404_NOT_FOUND)
        case _:
            return Response({'Message': 'Invalid Field'}, status= status.HTTP_400_BAD_REQUEST)

    user =  jwt.encode(user, secret_key, algorithm='HS256')
    return Response({'Message': "User's {} Updated".format(field), 'User': user}, status= status.HTTP_200_OK)
