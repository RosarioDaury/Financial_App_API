from api.models import CustomUser, AccountTypes
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        type = AccountTypes.objects.get(pk = 1)
        to_seed = [
            CustomUser.objects.create(
                username = "User1",
                password = "1234",
                first_name = "User",
                last_name = "Testing",
                email = "user@gmail.com",
                Account_type = type,
                Budget = 1500,
                Limit =  1000
            ),
        ]
        CustomUser.objects.bulk_create(to_seed)