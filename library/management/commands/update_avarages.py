from django.core.management.base import BaseCommand
from food.models import Avarage, Dry, Guaranteed, Calorie
from django.db.models import Avg, Max, Min
import re


def truncate(num):
    return float(re.sub(r'^(\d+\.\d{,4})\d*$',r'\1', str(num)))


class Command(BaseCommand):

    def _data_crate(self):

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


    def handle(self, *args, **options):
        self._data_crate()
