from django.urls import path
from ..views.Reminders import GetAllReminders, GetRemindersFiltered, CreateReminder, UpdateReminder, DeleteReminder, GetAllRemindersIntervals

urlpatterns = [
    path('get/all', GetAllReminders),
    path('types/get', GetAllRemindersIntervals),
    path('get', GetRemindersFiltered),
    path('create', CreateReminder),
    path('update/<str:field>', UpdateReminder),
    path('delete/<int:id>', DeleteReminder)
]