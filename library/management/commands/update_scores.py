from django.core.management.base import BaseCommand
from food.models import Food
import re


def truncate(num):
    return float(re.sub(r'^(\d+\.\d{,2})\d*$',r'\1', str(num)))


class Command(BaseCommand):

    def _data_crate(self):
        foods = Food.objects.filter(type=2).all()

        for food in foods:
            point = 0

            qualities = {
                'meat': {'wet': 0, 'dry': 0},
                'meal': {'wet': 0, 'dry': 0},
                'by-product': {'wet': 0, 'dry': 0},
                'protein': {'wet': 0, 'dry': 0},
                'other': {'wet': 0, 'dry': 0},
                'no-content': 0,
                'animal': {'wet': 0, 'dry': 0},
                'proteins': []
            }

            for ingredient in food.food.all():

                if ingredient.ingredient.quality.slug == 'meat' or ingredient.ingredient.quality.slug == 'giblets':
                    qualities['meat']['wet'] += ingredient.ingredient_percent - ingredient.dehydrated_percent
                    qualities['meat']['dry'] += ingredient.dehydrated_percent

                if ingredient.ingredient.quality.slug == 'by-product':
                    qualities['by-product']['wet'] += (ingredient.ingredient_percent - ingredient.dehydrated_percent)
                    qualities['by-product']['dry'] += ingredient.dehydrated_percent

                if ingredient.ingredient.quality.slug == 'protein':
                    qualities['protein']['wet'] += (ingredient.ingredient_percent - ingredient.dehydrated_percent)
                    qualities['protein']['dry'] += ingredient.dehydrated_percent

                if ingredient.ingredient.quality.slug == 'meal':
                    qualities['meal']['wet'] += (ingredient.ingredient_percent - ingredient.dehydrated_percent)
                    qualities['meal']['dry'] += ingredient.dehydrated_percent

                if ingredient.ingredient.quality.slug != 'protein' and ingredient.ingredient.quality.slug != 'meat' and ingredient.ingredient.quality.slug != 'meal' and ingredient.ingredient.quality.slug != 'giblets' and ingredient.ingredient.quality.slug != 'by-product':
                    qualities['other']['wet'] += (ingredient.ingredient_percent - ingredient.dehydrated_percent)
                    qualities['other']['dry'] += ingredient.dehydrated_percent

                if ingredient.ingredient.parent.regnum.slug == 'animals':
                    if ingredient.ingredient.parent.slug not in qualities['proteins'] and ingredient.ingredient.parent.slug != 'egg':
                        qualities['proteins'].append(ingredient.ingredient.parent.slug)

                    qualities['animal']['wet'] += (ingredient.ingredient_percent - ingredient.dehydrated_percent)
                    qualities['animal']['dry'] += ingredient.dehydrated_percent

            qualities['no-content'] = 100 - (qualities['meat']['wet'] + qualities['by-product']['wet'] + qualities['meal']['wet'] + qualities['other']['wet'] + qualities['meat']['dry'] + qualities['by-product']['dry'] + qualities['meal']['dry'] + qualities['other']['dry'])

            meat = truncate(((qualities['meat']['wet'] * 0.35) + qualities['meat']['dry']))
            meal = truncate((qualities['meal']['wet'] + qualities['meat']['dry']))
            by = truncate((qualities['by-product']['wet'] + qualities['by-product']['dry']))
            protein = truncate((qualities['protein']['wet'] + qualities['protein']['dry']))

            # MEAT POINT
            meat_point = 0
            total_meat_protein = meat + meal + by + protein
            meat_percent = truncate((meat / total_meat_protein))
            meal_percent = truncate((meal / total_meat_protein))
            other_meat_percent = 100 - (meat_percent + meal_percent)

            meat_point += (meal_percent * 1 + meal_percent * 0.5 + other_meat_percent * 0.3)

            if other_meat_percent >50:
                meat_point += 0
            elif other_meat_percent>25:
                meat_point += 0.5
            elif other_meat_percent>5:
                meat_point += 0.75
            else:
                meat_point += 1

            multiplier = total_meat_protein / 70;

            if multiplier > 1:
                multiplier = 1

            point += (meat_point * multiplier)

            # OTHER POINT
            other = truncate(qualities['no-content'])
            point += truncate(((100 - other)/100)*0.5)

            if other < 5:
                point += 0.5
            elif other < 10:
                point += 0.35
            elif other < 25:
                point += 0.2

            # TYPE POINT
            proteins = len(qualities['proteins'])
            if proteins > 3:
                point += 1
            elif proteins > 2:
                point += 0.75
            elif proteins > 1:
                point += 0.5
            elif proteins == 1:
                point += 0.25

            # ANIMAl POINT
            animal = truncate((qualities['animal']['wet'] + qualities['animal']['dry']))

            if animal > 75:
                point += 1
            elif animal > 60:
                point += 0.75
            elif animal > 50:
                point += 0.5
            elif animal > 40:
                point += 0.25

            # hayvansal içerik puanı
            # diğer içerik puanı
            # protein çeşitlilik puanı
            # protein kaynağı puanı yüzde ve içerik

    def handle(self, *args, **options):
        self._data_crate()
