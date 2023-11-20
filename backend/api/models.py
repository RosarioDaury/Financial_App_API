from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager
from model_utils.models import TimeStampedModel

class AccountTypes(models.Model):
    id = models.AutoField(primary_key= True)
    Type = models.CharField(max_length= 50, blank= False, null= False)

    def __str__(self):
        return self.Type

class TransactionType(models.Model):
    id = models.AutoField(primary_key= True)
    Type = models.CharField(max_length= 50, blank= False, null= False)

    def __str__(self):
        return self.Type

class ExpensesCategory(models.Model):
    id = models.AutoField(primary_key= True)
    Label = models.CharField(max_length= 50, blank= False, null= False) 
    isCustom = models.BooleanField(default = False, blank= False, null= False)

    def __str__(self):
        return self.Label

class RemindersInterval(models.Model):
    id = models.AutoField(primary_key= True)
    Label = models.CharField(max_length= 50, blank= False, null= False)
    Interval = models.IntegerField(blank= False, null= False)

    def __str__(self):
        return self.Label

class CustomUserManager(BaseUserManager):
    def create(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    groups = None
    Account_type = models.ForeignKey(AccountTypes, on_delete= models.CASCADE)
    Categories = models.ManyToManyField(ExpensesCategory, blank= True)
    Budget = models.FloatField(default= 0.0)
    Limit = models.IntegerField(default= 0, null= False, blank= False)

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        related_name='custom_users_permissions',
        default= []  # Unique related_name
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
class Transactions(TimeStampedModel):
    User = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    Amount = models.IntegerField(null= False, blank= False)
    Date = models.DateField(null= False, blank= False, auto_now= True)
    Title =  models.CharField(max_length=65, null= False, blank= False, unique= True)
    Description = models.CharField(max_length= 150, null= False, blank= False)
    Type = models.ForeignKey(TransactionType, on_delete= models.CASCADE)
    Category = models.ForeignKey(ExpensesCategory, on_delete= models.CASCADE)


    def __str__ (self):
        return self.Title
    
class Reminder(TimeStampedModel): 
    User = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    Amount = models.IntegerField(null= False, blank= False)
    Interval = models.ForeignKey(RemindersInterval, on_delete= models.CASCADE)
    Date =  models.DateField(null= False, blank= False)
    NextRunning = models.DateField()
    Title =  models.CharField(max_length=65, null= False, blank= False, unique= True)
    Description = models.CharField(max_length= 150, null= False, blank= False)

    def __str__ (self):
        return self.Title
    

