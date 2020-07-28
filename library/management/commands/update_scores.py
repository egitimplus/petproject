from django.core.management.base import BaseCommand
from company.models import Brand
from food.models import Food, FoodType, Ingredient, IngredientType, FoodFor, IngredientParent, FoodIngredient, Guaranteed, FoodStage
import json
from datetime import datetime
from django.db.models import Avg, Count


def change_date(date):
    d = datetime.strptime(date, "%B %d, %Y")
    return d.strftime('%Y/%m/%d')


def join_ingredients(ingredients):
    separator = ', '
    return separator.join(ingredients)


class Command(BaseCommand):

    def _data_crate(self):

        recommended = {
            'protein': 30,
            'fat': 9,
            'ash': 1,
            'taurine': 0.1,
            'calcium': 1,
            'phosphorus':0.8,
            'magnesium':0.08,
            'epa-dha': 0.012,
            'fibre': 0,
        }


        nutrition_points = {
            'protein': 0,
            'fat': 0,
            'ash': 0,
            'taurine': 0,
            'calcium': 0,
            'phosphorus': 0,
            'magnesium': 0,
            'epa-dha': 0,
            'fibre':0
        }

        averages = Guaranteed.objects.aggregate(
            protein=Avg('protein'),
            fat=Avg('fat'),
            ash=Avg('ash'),
            fibre=Avg('fibre'),
            moisture=Avg('moisture')
        )

        guaranteed_query = Guaranteed.objects.values()

        for guaranteed in guaranteed_query:
            edha = 0
            for k in guaranteed:
                if k != 'food_id' and k != 'epa' and k != 'dha' and k != 'moisture':
                    val = ((guaranteed[k] / (100-guaranteed['moisture']))*100)

                    if val > recommended[k]:
                        nutrition_points[k] += 0.5

                    if val > averages[k]:
                        nutrition_points[k] += 0.5

                if k == 'epa' or k == 'dha':
                    edha += ((guaranteed[k] / (100-guaranteed['moisture']))*100)

            if edha > recommended['epa-dha']:
                print(k)

                nutrition_points['epa-dha'] += 0.5

            if edha > averages['epa'] + averages['dha']:
                nutrition_points['epa-dha'] += 0.5

    def handle(self, *args, **options):
        self._data_crate()
