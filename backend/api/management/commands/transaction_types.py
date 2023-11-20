from api.models import TransactionType
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand): 
    def handle(self, *args, **options):
        to_seed = [
            TransactionType(Type = "Income"),
            TransactionType(Type = "Outcome")
        ]
        TransactionType.objects.bulk_create(to_seed)