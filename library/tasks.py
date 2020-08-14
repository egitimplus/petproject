# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from food.models import Food


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return Food.objects.count()


@shared_task
def rename_widget(food_id, name):
    w = Food.objects.get(id=food_id)
    w.name = name
    w.save()
