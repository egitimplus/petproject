from django.core.management.base import BaseCommand
from food.models import Avarage, Dry, Guaranteed
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

        obj, created = Avarage.objects.update_or_create(name='protein', defaults={'avarage': truncate(avarages['protein'])})
        obj, created = Avarage.objects.update_or_create(name='fat', defaults={'avarage': truncate(avarages['fat'])})
        obj, created = Avarage.objects.update_or_create(name='ash', defaults={'avarage': truncate(avarages['ash'])})
        obj, created = Avarage.objects.update_or_create(name='fibre', defaults={'avarage': truncate(avarages['fibre'])})
        obj, created = Avarage.objects.update_or_create(name='carbs', defaults={'avarage': truncate(avarages['carbs'])})

        avarages = Dry.objects.filter(taurine__gt=0).aggregate(taurine=Avg('taurine'))
        obj, created = Avarage.objects.update_or_create(name='taurine', defaults={'avarage': truncate(avarages['taurine'])})

        avarages = Dry.objects.filter(calcium__gt=0).aggregate(calcium=Avg('calcium'))
        obj, created = Avarage.objects.update_or_create(name='calcium', defaults={'avarage': truncate(avarages['calcium'])})

        avarages = Dry.objects.filter(phosphorus__gt=0).aggregate(phosphorus=Avg('phosphorus'))
        obj, created = Avarage.objects.update_or_create(name='phosphorus', defaults={'avarage': truncate(avarages['phosphorus'])})

        avarages = Dry.objects.filter(magnesium__gt=0).aggregate(magnesium=Avg('magnesium'))
        obj, created = Avarage.objects.update_or_create(name='magnesium', defaults={'avarage': truncate(avarages['magnesium'])})

        avarages = Dry.objects.filter(magnesium__gt=0).aggregate(magnesium=Avg('magnesium'))
        obj, created = Avarage.objects.update_or_create(name='magnesium', defaults={'avarage': truncate(avarages['magnesium'])})

        avarages = Dry.objects.filter(epa__gt=0).aggregate(epa=Avg('epa'))
        obj, created = Avarage.objects.update_or_create(name='epa', defaults={'avarage': truncate(avarages['epa'])})

        avarages = Dry.objects.filter(dha__gt=0).aggregate(dha=Avg('dha'))
        obj, created = Avarage.objects.update_or_create(name='dha', defaults={'avarage': truncate(avarages['dha'])})

        avarages = Dry.objects.filter(omega3__gt=0).aggregate(omega3=Avg('omega3'))
        obj, created = Avarage.objects.update_or_create(name='omega3', defaults={'avarage': truncate(avarages['omega3'])})

        avarages = Dry.objects.filter(omega6__gt=0).aggregate(omega6=Avg('omega6'))
        obj, created = Avarage.objects.update_or_create(name='omega6', defaults={'avarage': truncate(avarages['omega6'])})

        avarages = Guaranteed.objects.filter(moisture__gt=0).aggregate(moisture=Avg('moisture'))
        obj, created = Avarage.objects.update_or_create(name='moisture', defaults={'avarage': truncate(avarages['moisture'])})

    def handle(self, *args, **options):
        self._data_crate()
