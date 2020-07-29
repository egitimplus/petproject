from django.core.management.base import BaseCommand
from food.models import Food, Avarage
import re


def truncate(num):
    return float(re.sub(r'^(\d+\.\d{,2})\d*$',r'\1', str(num)))


class Command(BaseCommand):

    def _data_crate(self):
        foods = Food.objects.all()

        avarages = Avarage.objects.values()

        print(avarages)
        for food in foods:

            protein = food.dry.protein



            print(protein)


            #Food.objects.filter(id=food.id).update(nutrition_score=round(point))

    def handle(self, *args, **options):
        self._data_crate()
