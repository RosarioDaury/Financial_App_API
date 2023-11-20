from api.models import ExpensesCategory
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        to_seed = [
            ExpensesCategory(Label = "Health", isCustom = False),
            ExpensesCategory(Label = "Bills",  isCustom = False),
            ExpensesCategory(Label = "Personal Expenses",  isCustom = False),
        ]
        ExpensesCategory.objects.bulk_create(to_seed)