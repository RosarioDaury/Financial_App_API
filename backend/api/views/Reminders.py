from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serialializers import ReminderSerializar, RemindersIntervalsSerializer, ReminderSerializerCreate
from ..models import Reminder, RemindersInterval
from ..utils.GetRecords import GetAllRecords, GetRecordsFiltered
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
import jwt
from django.conf import settings
from django.http import HttpResponseForbidden

secret_key = getattr(settings, 'SECRET_KEY', 'default_value_if_not_set')

@api_view(['GET'])
def GetAllReminders(request):
    reminders = GetAllRecords(Reminder, ReminderSerializar)
    return Response(reminders, status = status.HTTP_200_OK)

@api_view(['GET'])
def GetAllRemindersIntervals(request):
    reminders = GetAllRecords(RemindersInterval, RemindersIntervalsSerializer)
    return Response(reminders, status = status.HTTP_200_OK)

@api_view(['POST'])
def GetRemindersFiltered( request ):
    field = request.data.get('field')
    value = request.data.get('value')

    User = request.headers['usertoken']
    if(not User):
        return HttpResponseForbidden("You do not have permission to access this resource.")
    User = jwt.decode(User, secret_key, algorithms=['HS256'])

    
    try:
        records = GetRecordsFiltered(Reminder, ReminderSerializar, {'name': field, 'value': value}, User['id'])
        return Response({'Data': records},  status = status.HTTP_200_OK)
    except Reminder.DoesNotExist:
        return Response({'Message': 'Not Records', "Data": []}, status = status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def CreateReminder( request ):
    User = request.headers['usertoken']
    User = jwt.decode(User, secret_key, algorithms=['HS256'])
    Data = {
        "User": User['id'],
        "Amount": request.data['Amount'],
        "Interval": request.data['Interval'],
        "Date": request.data['Date'],
        "NextRunning": request.data['NextRunning'],
        "Title": request.data['Title'],
        "Description": request.data['Description']
    }
    serializer = ReminderSerializerCreate(data = Data)

    if serializer.is_valid():
        User = serializer.validated_data['User']
        Amount = serializer.validated_data['Amount']
        Interval = serializer.validated_data['Interval']
        Date = serializer.validated_data['Date']
        NextRunning = serializer.validated_data['NextRunning']
        Title = serializer.validated_data['Title']
        Description = serializer.validated_data['Description']

        Reminder.objects.create(
            User = User,
            Amount = Amount,
            Interval = Interval,
            Date = Date,
            NextRunning = NextRunning,
            Title = Title,
            Description = Description
        )

        return Response({ 'Message': 'Reminder Succesfully Created'}, status = status.HTTP_201_CREATED)
    return Response({'Message': 'Invalid Body', "error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def UpdateReminder(request, field):
    reminder_id = request.data.get('reminder')

    if(reminder_id is None):
        return Response(status= status.HTTP_400_BAD_REQUEST)  
            
    try:
        reminder = Reminder.objects.get(pk = reminder_id)
        remind = ReminderSerializar(reminder).data 
        User = request.headers['usertoken']
        User = jwt.decode(User, secret_key, algorithms=['HS256'])
        print(User['username'], remind['User'])
        if(remind['User'] != User["username"]):
            return HttpResponseForbidden("You do not have permission to access this resource.")
        

        match field:
            case 'Amount':
                Amount =  request.data.get('Amount')

                if(Amount is None):
                    return Response(status= status.HTTP_400_BAD_REQUEST) 
                reminder.Amount = Amount

            case 'Interval':
                Interval =  request.data.get('Interval')
                if(Interval is None):
                    return Response(status= status.HTTP_400_BAD_REQUEST) 
                
                try:
                    reminder_interval = RemindersInterval.objects.get(pk = Interval)
                except RemindersInterval.DoesNotExist:
                    return Response(status= status.HTTP_400_BAD_REQUEST) 
                
                reminder.Interval = reminder_interval

            case 'NextRunning':
                NextRunning =  request.data.get('NextRunning')
                if(NextRunning is None):
                    return Response(status= status.HTTP_400_BAD_REQUEST) 
                
                reminder.NextRunning = NextRunning

            case 'Title':
                Title =  request.data.get('Title')
                if(Title is None):
                    return Response(status= status.HTTP_400_BAD_REQUEST) 
                
                reminder.Title = NextRunning

            case 'Description':
                Title =  request.data.get('Description')
                if(Title is None):
                    return Response(status= status.HTTP_400_BAD_REQUEST) 
                
                reminder.Title = NextRunning
            
            case _:
                return Response(status= status.HTTP_400_BAD_REQUEST) 

        try:
            reminder.save()
        except ValidationError as e:
            return Response({"Error": e.error_list[0]}, status= status.HTTP_400_BAD_REQUEST) 
        return Response({'Message': "Reminder's {} Updated".format(field)}, status= status.HTTP_200_OK)
    except Reminder.DoesNotExist:
        return Response({'Message': 'Reminder Not Found'}, status = status.HTTP_404_NOT_FOUND)
    except IntegrityError as e:
        return Response({'Message': 'Integrity Error'}, status = status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def DeleteReminder(request, id):
    try:
        record = Reminder.objects.get(pk = id)
        reminder = ReminderSerializar(record).data
        User = request.headers['usertoken']
        User = jwt.decode(User, secret_key, algorithms=['HS256'])
        if(reminder["User"] != User["username"]):
            return HttpResponseForbidden("You do not have permission to access this resource.")
    except Reminder.DoesNotExist:
        return Response({'Message': 'Not Records', "Data": []}, status = status.HTTP_404_NOT_FOUND)

    record.delete()
    return Response({'Message': 'Transaction Successfully Deleted'}, status= status.HTTP_200_OK)