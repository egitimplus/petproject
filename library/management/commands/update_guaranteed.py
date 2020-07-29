from django.core.management.base import BaseCommand
from food.models import Guaranteed, Dry
import re


def truncate(num):
    return float(re.sub(r'^(\d+\.\d{,4})\d*$',r'\1', str(num)))


class Command(BaseCommand):

    def _data_crate(self):

        guaranteed_query = Guaranteed.objects.all()

        for guaranteed in guaranteed_query:
            total = guaranteed.protein + guaranteed.fat + guaranteed.ash + guaranteed.fibre + guaranteed.moisture

            if total > 100:
                guaranteed.moisture = 100 - guaranteed.protein + guaranteed.fat + guaranteed.ash + guaranteed.fibre
                guaranteed.carbs = 0
            else:
                guaranteed.carbs = 100 - total

            guaranteed.save()

    def handle(self, *args, **options):
        self._data_crate()
