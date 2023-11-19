from api.models import RemindersInterval
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        to_seed = [
            RemindersInterval(Interval= 1, Label = "Daily"),
            RemindersInterval(Interval= 7, Label = "Weekly"),
            RemindersInterval(Interval= 15, Label = "Biweekly"),
            RemindersInterval(Interval= 30, Label = "Monthly"),
            RemindersInterval(Interval= 60, Label = "Two Months"),
            RemindersInterval(Interval= 90, Label = "Three Months"),
        ]
        RemindersInterval.objects.bulk_create(to_seed)