from django.core.management.base import BaseCommand
from food.models import Avarage, Dry, Guaranteed, Calorie, Food
from django.db.models import Avg, Max, Min
import re


def truncate(num):
    return float(re.sub(r'^(\d+\.\d{,4})\d*$',r'\1', str(num)))


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a username prefix', )

    def _avarage_crate(self):

        avarages = Dry.objects.aggregate(
            protein=Avg('protein'),
            max_protein=Max('protein'),
            min_protein=Min('protein'),
            fat=Avg('fat'),
            max_fat=Max('fat'),
            min_fat=Min('fat'),
            ash=Avg('ash'),
            max_ash=Max('ash'),
            min_ash=Min('ash'),
            fibre=Avg('fibre'),
            max_fibre=Max('fibre'),
            min_fibre=Min('fibre'),
            carbs=Avg('carbs'),
            max_carbs=Max('carbs'),
            min_carbs=Min('carbs')
        )

        obj, created = Avarage.objects.update_or_create(
            name='protein',
            defaults={
                'avarage': truncate(avarages['protein']),
                'max_value': truncate(avarages['max_protein']),
                'min_value': truncate(avarages['min_protein']),
                'recommend': 30
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='fat',
            defaults={
                'avarage': truncate(avarages['fat']),
                'max_value': truncate(avarages['max_fat']),
                'min_value': truncate(avarages['min_fat']),
                'recommend': 9
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='ash',
            defaults={
                'avarage': truncate(avarages['ash']),
                'max_value': truncate(avarages['max_ash']),
                'min_value': truncate(avarages['min_ash']),
                'recommend': 0.6
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='fibre',
            defaults={
                'avarage': truncate(avarages['fibre']),
                'max_value': truncate(avarages['max_fibre']),
                'min_value': truncate(avarages['min_fibre']),
                'recommend': 0
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='carbs',
            defaults={
                'avarage': truncate(avarages['carbs']),
                'max_value': truncate(avarages['max_carbs']),
                'min_value': truncate(avarages['min_carbs']),
                'recommend': 0
            }
        )

        query = Dry.objects.filter(taurine__gt=0).aggregate(
            taurine=Avg('taurine'),
            max_taurine=Max('taurine'),
            min_taurine=Min('taurine'),
        )

        obj, created = Avarage.objects.update_or_create(
            name='taurine',
            defaults={
                'avarage': truncate(query['taurine']),
                'max_value': truncate(query['max_taurine']),
                'min_value': truncate(query['min_taurine']),
                'recommend': 0.1
            }
        )

        query = Dry.objects.filter(calcium__gt=0).aggregate(
            calcium=Avg('calcium'),
            max_calcium=Max('calcium'),
            min_calcium=Min('calcium'),
        )

        obj, created = Avarage.objects.update_or_create(
            name='calcium',
            defaults={
                'avarage': truncate(query['calcium']),
                'max_value': truncate(query['max_calcium']),
                'min_value': truncate(query['min_calcium']),
                'recommend': 1
            }
        )

        query = Dry.objects.filter(phosphorus__gt=0).aggregate(
            phosphorus=Avg('phosphorus'),
            max_phosphorus=Max('phosphorus'),
            min_phosphorus=Min('phosphorus'),
        )

        obj, created = Avarage.objects.update_or_create(
            name='phosphorus',
            defaults={
                'avarage': truncate(query['phosphorus']),
                'max_value': truncate(query['max_phosphorus']),
                'min_value': truncate(query['min_phosphorus']),
                'recommend': 0.8
            }
        )

        query = Dry.objects.filter(magnesium__gt=0).aggregate(
            magnesium=Avg('magnesium'),
            max_magnesium=Max('magnesium'),
            min_magnesium=Min('magnesium'),
        )

        obj, created = Avarage.objects.update_or_create(
            name='magnesium',
            defaults={
                'avarage': truncate(query['magnesium']),
                'max_value': truncate(query['max_magnesium']),
                'min_value': truncate(query['min_magnesium']),
                'recommend': 0.08
            }
        )

        query = Dry.objects.filter(epa__gt=0).aggregate(
            epa=Avg('epa'),
            max_epa=Max('epa'),
            min_epa=Min('epa'),
        )
        obj, created = Avarage.objects.update_or_create(
            name='epa',
            defaults={
                'avarage': truncate(query['epa']),
                'max_value': truncate(query['max_epa']),
                'min_value': truncate(query['min_epa']),
                'recommend': 0.06
            }
        )

        query = Dry.objects.filter(dha__gt=0).aggregate(
            dha=Avg('dha'),
            max_dha=Max('dha'),
            min_dha=Min('dha'),
        )

        obj, created = Avarage.objects.update_or_create(
            name='dha',
            defaults={
                'avarage': truncate(query['dha']),
                'max_value': truncate(query['max_dha']),
                'min_value': truncate(query['min_dha']),
                'recommend': 0.06
            }
        )

        query = Dry.objects.filter(omega3__gt=0).aggregate(
            omega3=Avg('omega3'),
            max_omega3=Max('omega3'),
            min_omega3=Min('omega3'),
        )

        obj, created = Avarage.objects.update_or_create(
            name='omega3',
            defaults={
                'avarage': truncate(query['omega3']),
                'max_value': truncate(query['max_omega3']),
                'min_value': truncate(query['min_omega3']),
                'recommend': 0
            }
        )

        query = Dry.objects.filter(omega6__gt=0).aggregate(
            omega6=Avg('omega6'),
            max_omega6=Max('omega6'),
            min_omega6=Min('omega6'),
        )

        obj, created = Avarage.objects.update_or_create(
            name='omega6',
            defaults={
                'avarage': truncate(query['omega6']),
                'max_value': truncate(query['max_omega6']),
                'min_value': truncate(query['min_omega6']),
                'recommend': 0
            }
        )

        query = Guaranteed.objects.filter(moisture__gt=0).aggregate(
            moisture=Avg('moisture'),
            max_moisture=Max('moisture'),
            min_moisture=Min('moisture'),
        )

        obj, created = Avarage.objects.update_or_create(
            name='moisture',
            defaults={
                'avarage': truncate(query['moisture']),
                'max_value': truncate(query['max_moisture']),
                'min_value': truncate(query['min_moisture']),
                'recommend': 0
            }
        )

        query = Calorie.objects.aggregate(
            protein=Avg('protein'),
            max_protein=Max('protein'),
            min_protein=Min('protein'),
            fat=Avg('fat'),
            max_fat=Max('fat'),
            min_fat=Min('fat'),
            carbs=Avg('carbs'),
            max_carbs=Max('carbs'),
            min_carbs=Min('carbs'),
            total=Avg('total'),
            max_total=Max('total'),
            min_total=Min('total'),
        )

        obj, created = Avarage.objects.update_or_create(
            name='calorie_protein',
            defaults={
                'avarage': truncate(query['protein']),
                'max_value': truncate(query['max_protein']),
                'min_value': truncate(query['min_protein']),
                'recommend': 0
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='calorie_fat',
            defaults={
                'avarage': truncate(query['fat']),
                'max_value': truncate(query['max_fat']),
                'min_value': truncate(query['min_fat']),
                'recommend': 0
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='calorie_carbs',
            defaults={
                'avarage': truncate(query['carbs']),
                'max_value': truncate(query['max_carbs']),
                'min_value': truncate(query['min_carbs']),
                'recommend': 0
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='calorie_total',
            defaults={
                'avarage': truncate(query['total']),
                'max_value': truncate(query['max_total']),
                'min_value': truncate(query['min_total']),
                'recommend': 0
            }
        )

    def _calorie_crate(self):

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

    def _dry_crate(self):

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

    def _guaranteed_crate(self):

        guaranteed_query = Guaranteed.objects.all()

        for guaranteed in guaranteed_query:
            total = guaranteed.protein + guaranteed.fat + guaranteed.ash + guaranteed.fibre + guaranteed.moisture

            if total > 100:
                guaranteed.moisture = 100 - guaranteed.protein + guaranteed.fat + guaranteed.ash + guaranteed.fibre
                guaranteed.carbs = 0
            else:
                guaranteed.carbs = 100 - total

            guaranteed.save()

    def _ingredient_score_crate(self):
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

            Food.objects.filter(id=food.id).update(ingredient_score=round(point))

    def _nutrition_score_crate(self):
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
        update_type = options.get('type', None)

        if update_type is not None:
            if update_type == 'avarage':
                self._avarage_crate()
                print('Avarage updated')
            elif update_type == 'calorie':
                self._calorie_crate()
                print('Calorie updated')
            elif update_type == 'dry':
                self._dry_crate()
                print('Dry updated')
            elif update_type == 'guaranteed':
                self._guaranteed_crate()
                print('Guaranteed updated')
            elif update_type == 'ingredient_score':
                self._ingredient_score_crate()
                print('Ingredient score updated')
            elif update_type == 'nutrition_score':
                self._nutrition_score_crate()
                print('Nutrition score updated')
            elif update_type == 'score':
                self._ingredient_score_crate()
                print('Ingredient score updated')
                self._nutrition_score_crate()
                print('Nutrition score updated')
            elif update_type == 'all':
                self._guaranteed_crate()
                print('Guaranteed updated')
                self._dry_crate()
                print('Dry updated')
                self._calorie_crate()
                print('Calorie updated')
                self._avarage_crate()
                print('Avarage updated')
                self._ingredient_score_crate()
                print('Ingredient score updated')
                self._nutrition_score_crate()
                print('Nutrition score updated')
