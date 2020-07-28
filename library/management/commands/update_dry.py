from django.core.management.base import BaseCommand
from food.models import Guaranteed, Dry
import re


def truncate(num):
    return float(re.sub(r'^(\d+\.\d{,4})\d*$',r'\1', str(num)))


class Command(BaseCommand):

    def _data_crate(self):

        guaranteed_query = Guaranteed.objects.values()

        d = {
            'food_id': 0,
            'protein': 0,
            'fat': 0,
            'ash': 0,
            'taurine': 0,
            'calcium': 0,
            'phosphorus': 0,
            'magnesium': 0,
            'epa': 0,
            'dha': 0,
            'omega3': 0,
            'omega6': 0,
            'fibre': 0,
            'carbs': 0
        }

        for guaranteed in guaranteed_query:
            for key in guaranteed:
                if key != 'food_id' and key != 'moisture':
                    val = ((guaranteed[key] / (100-guaranteed['moisture']))*100)
                    d[key] = truncate(val)

            d['food_id'] = guaranteed['food_id']
            d['carbs'] = truncate(100 - (d['protein'] + d['fat'] + d['ash'] + d['fibre']))

            d.pop('moisture', None)

            m = Dry(**d)
            m.save()

    def handle(self, *args, **options):
        self._data_crate()
