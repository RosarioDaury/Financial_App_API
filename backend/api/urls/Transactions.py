from django.urls import path
from ..views.Transactions import GetTransactionsAll, CreateTransaction, GetTransactionsFiltered, GetTransactionTypes, DeleteTransaction

urlpatterns = [
    path('get/all', GetTransactionsAll),
    path('types/get', GetTransactionTypes),
    path('create', CreateTransaction),
    path('get', GetTransactionsFiltered),
    path('delete/<int:id>', DeleteTransaction)
]