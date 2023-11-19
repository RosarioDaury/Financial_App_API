from django.urls import path
from ..views.User import Users, AuthUser, CreateUser, DeactivateUser, UpdateFieldUser, GetAccountTypes

urlpatterns = [
    path('get', Users),
    path('auth', AuthUser),
    path('create', CreateUser),
    path('deactivate', DeactivateUser),
    path('update/<str:field>', UpdateFieldUser),
    path('types/get', GetAccountTypes),
]