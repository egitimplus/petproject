from django.core.management.base import BaseCommand
from food.models import Food, Avarage
import re


def truncate(num):
    return float(re.sub(r'^(\d+\.\d{,2})\d*$',r'\1', str(num)))


class Command(BaseCommand):

    def _data_crate(self):
        foods = Food.objects.all()

        for food in foods:
            nutrition_point = 0

            data = Avarage.objects.filter(name='protein').first()
            protein_ingredient = food.dry.protein
            point = 0

            if protein_ingredient >= data.recommend:

                if protein_ingredient > 52:
                    point = 1

                else:
                    point = round(protein_ingredient / 52, 1)

                    if point > 1:
                        point = 1

            nutrition_point += point

            fat_ingredient = food.dry.fat
            if fat_ingredient >= data.recommend:

                if fat_ingredient < 22:

                    point = round(fat_ingredient/22, 1)

                    if point > 1:
                        point = 1

                elif fat_ingredient > 36:
                    point = round(36/fat_ingredient, 1)

                    if point > 1:
                        point = 1

                else:
                    point = 1

            nutrition_point += point

            carbs_ingredient = food.dry.carbs

            if carbs_ingredient < 12:
                point = 1

            else:
                point = round(12 / carbs_ingredient, 1)

                if point > 1:
                    point = 1

            nutrition_point += point

            additives_point = 0

            if food.dry.calcium >= 1:
                additives_point += 0.15

            if food.dry.taurine >= 0.1:
                additives_point += 0.25

            if food.dry.phosphorus >= 0.8:
                additives_point += 0.15

            if food.dry.magnesium >= 0.08:
                additives_point += 0.15

            if food.dry.epa + food.dry.dha >= 0.12:
                additives_point += 0.15

            if food.dry.omega3 >= 0:
                additives_point += 0.25

            if food.dry.omega6 >= 0:
                additives_point += 0.25

            if additives_point > 1:
                additives_point = 1

            nutrition_point += additives_point

            fibre_ingredient = food.dry.fibre

            if fibre_ingredient < 1.4:
                point = round((fibre_ingredient/1.4)/2, 1)

                if point > 0.5:
                    point = 0.5

            elif fibre_ingredient > 3.5:
                point = round((3.5/fibre_ingredient)/2, 1)

                if point > 0.5:
                   point = 0.5

            else:
                point = 0.5

            nutrition_point += point

            ash_ingredient = food.dry.ash

            if ash_ingredient > 2 and ash_ingredient < 8:
                    point = 0.5
            elif ash_ingredient <= 2:
                point = round((ash_ingredient/2)/2, 1)

                if point > 0.5:
                   point = 0.5

            else:
                point = 0.5
                point = round((8/ash_ingredient)/2, 1)

                if point > 0.5:
                   point = 0.5

            nutrition_point += point

            Food.objects.filter(id=food.id).update(nutrition_score=round(nutrition_point))

    def handle(self, *args, **options):
        self._data_crate()
