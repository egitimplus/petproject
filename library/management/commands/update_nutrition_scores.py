from django.core.management.base import BaseCommand
from food.models import Food
import re


def truncate(num):
    return float(re.sub(r'^(\d+\.\d{,2})\d*$',r'\1', str(num)))


class Command(BaseCommand):

    def _data_crate(self):
        foods = Food.objects.all()

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
                'proteins': [],
                'broth': 0
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

                if ingredient.ingredient.quality.slug != 'broth' and ingredient.ingredient.quality.slug != 'protein' and ingredient.ingredient.quality.slug != 'meat' and ingredient.ingredient.quality.slug != 'meal' and ingredient.ingredient.quality.slug != 'giblets' and ingredient.ingredient.quality.slug != 'by-product':
                    qualities['other']['wet'] += (ingredient.ingredient_percent - ingredient.dehydrated_percent)
                    qualities['other']['dry'] += ingredient.dehydrated_percent

                if ingredient.ingredient.parent.regnum.slug == 'animals':
                    if ingredient.ingredient.parent.slug not in qualities['proteins'] and ingredient.ingredient.parent.slug != 'egg':
                        qualities['proteins'].append(ingredient.ingredient.parent.slug)

                    qualities['animal']['wet'] += (ingredient.ingredient_percent - ingredient.dehydrated_percent)
                    qualities['animal']['dry'] += ingredient.dehydrated_percent

                if ingredient.ingredient.quality.slug == 'broth':
                    qualities['broth'] += ingredient.ingredient_percent

            qualities['no-content'] = 100 - (qualities['broth'] + qualities['meat']['wet'] + qualities['by-product']['wet'] + qualities['meal']['wet'] + qualities['other']['wet'] + qualities['meat']['dry'] + qualities['by-product']['dry'] + qualities['meal']['dry'] + qualities['other']['dry'])

            meat = truncate(((qualities['meat']['wet'] * 0.30) + qualities['meat']['dry']))
            meal = truncate((qualities['meal']['wet'] + qualities['meat']['dry']))
            by = truncate((qualities['by-product']['wet'] + qualities['by-product']['dry']))
            protein = truncate((qualities['protein']['wet'] + qualities['protein']['dry']))
            broth = truncate(qualities['broth'])

            # MEAT POINT
            meat_point = 0
            total_meat_protein = meat + meal + by + protein
            meat_percent = truncate((meat / total_meat_protein))
            meal_percent = truncate((meal / total_meat_protein))
            other_meat_percent = truncate((1 - (meat_percent + meal_percent)))

            meat_point += (meat_percent * 1 + meal_percent * 0.5 + other_meat_percent * 0.3)

            if other_meat_percent > 0.5:
                meat_point += 0
            elif other_meat_percent > 0.25:
                meat_point += 0.5
            elif other_meat_percent > 0.05:
                meat_point += 0.75
            else:
                meat_point += 1

            food_percent = 70
            if food.type.slug == 'wet':
                food_percent = 30

            multiplier = total_meat_protein / food_percent

            if multiplier > 1:
                multiplier = 1

            meat_point = meat_point * multiplier
            point += meat_point

            # OTHER POINT

            if food.type.slug == 'dry':
                other = truncate(qualities['no-content'])

                other_percent = 100
                diff_other = other_percent - other

                other_point = truncate((diff_other/100)*0.5)

                if other < 5:
                    other_point += 0.5
                elif other < 10:
                    other_point += 0.35
                elif other < 25:
                    other_point += 0.2

                point += other_point

            # TYPE POINT
            type_point = 0
            proteins = len(qualities['proteins'])
            if proteins > 3:
                type_point += 0.5
            elif proteins > 2:
                type_point += 0.4
            elif proteins > 1:
                type_point += 0.3
            elif proteins == 1:
                type_point += 0.2

            point += type_point

            # ANIMAl POINT
            animal = truncate((qualities['animal']['wet'] + qualities['animal']['dry']))
            animal_point = 0

            if animal > 75:
                animal_point += 0.5
            elif animal > 60:
                animal_point += 0.4
            elif animal > 50:
                animal_point += 0.3
            elif animal > 40:
                animal_point += 0.2

            point += animal_point

            if food.type.slug == 'wet':
                point = point * 5 / 3

            if food.type.slug == 'dry':
                point = point * 5 / 4

            Food.objects.filter(id=food.id).update(nutrition_score=round(point))

    def handle(self, *args, **options):
        self._data_crate()
