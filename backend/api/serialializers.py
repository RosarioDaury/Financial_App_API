from api.models import CustomUser, Transactions, Reminder, RemindersInterval, AccountTypes, TransactionType
from rest_framework import serializers

class AccountTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTypes
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    Account_type = serializers.StringRelatedField()
    class Meta:
        model = CustomUser
        fields = '__all__'
    
class CustomUserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class TransactionsSerializer(serializers.ModelSerializer):
    Type = serializers.StringRelatedField()
    User = serializers.StringRelatedField()    
    class Meta:
        model = Transactions
        fields = '__all__'

class TransactionsSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'

class TransactionsTypesSerializers(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'

class ReminderSerializar(serializers.ModelSerializer):
    Interval = serializers.StringRelatedField()
    User = serializers.StringRelatedField()    
    class Meta:
        model = Reminder
        fields = '__all__'

class ReminderSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'

class RemindersIntervalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemindersInterval
        fields = '__all__'