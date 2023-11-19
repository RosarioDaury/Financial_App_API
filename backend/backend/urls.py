from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('api.urls.Users')),
    path('api/transactions/', include('api.urls.Transactions')),
    path('api/reminders/', include('api.urls.Reminders'))
]
