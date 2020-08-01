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
            ingredient = food.dry.protein
            point = 0

            if ingredient >= data.recommend:
                if ingredient < data.avarage:

                    avarage_diff = data.avarage - data.recommend

                    if avarage_diff < 1:
                        avarage_diff = 1

                    recommend_diff = ingredient - data.recommend

                    if recommend_diff < 1:
                        recommend_diff = 1

                    diff = round(recommend_diff / (avarage_diff / 5))

                    if diff < 1:
                        diff = 1

                    point = diff * 0.1

                    if point > 0.5:
                        point = 0.5

                else:

                    max_diff = data.max_value - data.avarage

                    if max_diff < 1:
                        max_diff = 1

                    avarage_diff = ingredient - data.avarage

                    if avarage_diff < 1:
                        avarage_diff = 1

                    diff = round(avarage_diff / (max_diff / 5))

                    if diff < 1:
                        diff = 1

                    add_plus = diff * 0.1

                    point = 0.5 + add_plus

            nutrition_point += point
            Food.objects.filter(id=food.id).update(nutrition_score=round(point))

    def handle(self, *args, **options):
        self._data_crate()
