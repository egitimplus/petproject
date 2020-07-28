from django.core.management.base import BaseCommand
from food.models import Guaranteed, Calorie


class Command(BaseCommand):

    def _data_crate(self):

        guaranteed_query = Guaranteed.objects.all()

        d = {
            'food_id': 0,
            'protein': 0,
            'fat': 0,
            'carbs': 0,
            'total': 0,
        }

        for guaranteed in guaranteed_query:
            d['protein'] = guaranteed.protein * 3.5
            d['fat'] = guaranteed.fat * 8.5
            d['carbs'] = guaranteed.carbs * 3.5

            d['food_id'] = guaranteed.food_id
            d['total'] = d['protein'] + d['fat'] + d['carbs']

            m = Calorie(**d)
            m.save()

    def handle(self, *args, **options):
        self._data_crate()
