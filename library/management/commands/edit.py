from django.core.management.base import BaseCommand
from company.models import Brand
from food.models import Food, FoodType, Ingredient, IngredientType, FoodFor, IngredientParent, FoodIngredient, Guaranteed, DryMatter, Calorie
import json
from datetime import datetime



class Command(BaseCommand):

    def _data_crate(self):
        bl = Brand.objects.filter(id=3).delete()

    def handle(self, *args, **options):
        self._data_crate()
