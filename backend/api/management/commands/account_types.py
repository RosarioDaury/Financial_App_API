from api.models import AccountTypes
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        to_seed = [
            AccountTypes(Type = "Personal"),
            AccountTypes(Type = "Company")
        ]
        AccountTypes.objects.bulk_create(to_seed)