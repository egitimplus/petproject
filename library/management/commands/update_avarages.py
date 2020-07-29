from django.core.management.base import BaseCommand
from food.models import Avarage, Dry, Guaranteed, Calorie
from django.db.models import Avg
import re


def truncate(num):
    return float(re.sub(r'^(\d+\.\d{,4})\d*$',r'\1', str(num)))


class Command(BaseCommand):

    def _data_crate(self):

        avarages = Dry.objects.aggregate(
            protein=Avg('protein'),
            fat=Avg('fat'),
            ash=Avg('ash'),
            fibre=Avg('fibre'),
            carbs=Avg('carbs')
        )

        obj, created = Avarage.objects.update_or_create(
            name='protein',
            defaults={
                'avarage': truncate(avarages['protein']),
                'recommend': 30
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='fat',
            defaults={
                'avarage': truncate(avarages['fat']),
                'recommend': 9
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='ash',
            defaults={
                'avarage': truncate(avarages['ash']),
                'recommend': 0.6
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='fibre',
            defaults={
                'avarage': truncate(avarages['fibre']),
                'recommend': 0
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='carbs',
            defaults={
                'avarage': truncate(avarages['carbs']),
                'recommend': 0
            }
        )

        query = Dry.objects.filter(taurine__gt=0).aggregate(taurine=Avg('taurine'))
        obj, created = Avarage.objects.update_or_create(
            name='taurine',
            defaults={
                'avarage': truncate(query['taurine']),
                'recommend': 0.1
            }
        )

        query = Dry.objects.filter(calcium__gt=0).aggregate(calcium=Avg('calcium'))
        obj, created = Avarage.objects.update_or_create(
            name='calcium',
            defaults={
                'avarage': truncate(query['calcium']),
                'recommend': 1
            }
        )

        query = Dry.objects.filter(phosphorus__gt=0).aggregate(phosphorus=Avg('phosphorus'))
        obj, created = Avarage.objects.update_or_create(
            name='phosphorus',
            defaults={
                'avarage': truncate(query['phosphorus']),
                'recommend': 0.8
            }
        )

        query = Dry.objects.filter(magnesium__gt=0).aggregate(magnesium=Avg('magnesium'))
        obj, created = Avarage.objects.update_or_create(
            name='magnesium',
            defaults={
                'avarage': truncate(query['magnesium']),
                'recommend': 0.08
            }
        )


        query = Dry.objects.filter(epa__gt=0).aggregate(epa=Avg('epa'))
        obj, created = Avarage.objects.update_or_create(
            name='epa',
            defaults={
                'avarage': truncate(query['epa']),
                'recommend': 0.06
            }
        )

        query = Dry.objects.filter(dha__gt=0).aggregate(dha=Avg('dha'))
        obj, created = Avarage.objects.update_or_create(
            name='dha',
            defaults={
                'avarage': truncate(query['dha']),
                'recommend': 0.06
            }
        )

        query = Dry.objects.filter(omega3__gt=0).aggregate(omega3=Avg('omega3'))
        obj, created = Avarage.objects.update_or_create(
            name='omega3',
            defaults={
                'avarage': truncate(query['omega3']),
                'recommend': 0
            }
        )

        query = Dry.objects.filter(omega6__gt=0).aggregate(omega6=Avg('omega6'))
        obj, created = Avarage.objects.update_or_create(
            name='omega6',
            defaults={
                'avarage': truncate(query['omega6']),
                'recommend': 0
            }
        )

        query = Guaranteed.objects.filter(moisture__gt=0).aggregate(moisture=Avg('moisture'))
        obj, created = Avarage.objects.update_or_create(
            name='moisture',
            defaults={
                'avarage': truncate(query['moisture']),
                'recommend': 0
            }
        )

        query = Calorie.objects.aggregate(protein=Avg('protein'), fat=Avg('fat'), carbs=Avg('carbs'), total=Avg('total'),)

        obj, created = Avarage.objects.update_or_create(
            name='calorie_protein',
            defaults={
                'avarage': truncate(query['protein']),
                'recommend': 0
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='calorie_fat',
            defaults={
                'avarage': truncate(query['fat']),
                'recommend': 0
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='calorie_carbs',
            defaults={
                'avarage': truncate(query['carbs']),
                'recommend': 0
            }
        )

        obj, created = Avarage.objects.update_or_create(
            name='calorie_total',
            defaults={
                'avarage': truncate(query['carbs']),
                'recommend': 0
            }
        )


    def handle(self, *args, **options):
        self._data_crate()
