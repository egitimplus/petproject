from django.core.management.base import BaseCommand
from company.models import Brand
from food.models import Food, FoodType, Ingredient, IngredientType, FoodFor, IngredientParent, FoodIngredient, Guaranteed, DryMatter, Calorie, FoodStage
import json
from datetime import datetime


def change_date(date):
    d = datetime.strptime(date, "%B %d, %Y")
    return d.strftime('%Y/%m/%d')


def join_ingredients(ingredients):
    separator = ', '
    return separator.join(ingredients)


class Command(BaseCommand):

    def _data_crate(self):

        json_data = open(r'C:\Users\info\PycharmProjects\petproject\static/purina.json')
        data1 = json.load(json_data)

        food_for = FoodFor.objects.get_or_create(name='Kedi')[0]
        food_stage = FoodStage.objects.get_or_create(name='Tüm yaşlar')[0]
        parent = IngredientParent.objects.get_or_create(name='Genel', defaults={'allergen': 0})[0]
        type = IngredientType.objects.get_or_create(name='Genel')[0]

        for food in data1:
            food_date = change_date(food['date_added'])
            brand = Brand.objects.get_or_create(name=food['brand'])[0]
            food_type = FoodType.objects.get_or_create(name=food['food_type'])[0]
            content = join_ingredients(food['ingredients'])

            food_instance = Food.objects.create(
                name=food['name'],
                ingredient_score=food['ingredient_score'],
                nutrition_score=food['nutrition_score'],
                manufacturer_url=food['brand_url'],
                image=food['image'],
                brand=brand,
                food_type=food_type,
                food_for=food_for,
                food_stage=food_stage,
                content=content,
                created=food_date,
                updated=food_date
            )

            Guaranteed.objects.create(
                protein=food['guaranteed']['protein'].replace("%", ""),
                carbs=food['guaranteed']['carbs'].replace("%", ""),
                fat=food['guaranteed']['fat'].replace("%", ""),
                fiber=food['guaranteed']['fiber'].replace("%", ""),
                ash=food['guaranteed']['ash'].replace("%", ""),
                moisture=food['guaranteed']['moisture'].replace("%", ""),
                food=food_instance
            )

            DryMatter.objects.create(
                protein=food['dry_matter']['protein'].replace("%", ""),
                carbs=food['dry_matter']['carbs'].replace("%", ""),
                fat=food['dry_matter']['fat'].replace("%", ""),
                fiber=food['dry_matter']['fiber'].replace("%", ""),
                ash=food['dry_matter']['ash'].replace("%", ""),
                food=food_instance
            )

            Calorie.objects.create(
                protein=food['calories']['protein'],
                carbs=food['calories']['carbs'],
                fat=food['calories']['fat'],
                total=food['est_calories'],
                food=food_instance
            )

            for ingredient in food['ingredients']:
                ingredient_lower = ingredient.lower()
                quality = 1
                allergen = 0

                if ingredient_lower in (name.lower() for name in food['quality_ingredients']):
                    quality = 2

                if ingredient_lower in (name.lower() for name in food['questionable_ingredients']):
                    quality = 0

                if ingredient_lower in (name.lower() for name in food['potantial_allergens']):
                    allergen = 1

                try:
                    ingredient_instance = Ingredient.objects.get(name=ingredient_lower)
                except Ingredient.DoesNotExist:
                    ingredient_instance = Ingredient.objects.create(
                        name=ingredient_lower,
                        quality=quality,
                        type=type,
                        allergen=allergen,
                        parent_id=1
                    )


                FoodIngredient.objects.create(ingredient=ingredient_instance, food=food_instance, ingredient_percent=0)

    def handle(self, *args, **options):
        self._data_crate()
