from rest_flex_fields import FlexFieldsModelSerializer
from food.models import Food


class FoodSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Food
        fields = (
            'id',
            'name',
            'slug',
            'manufacturer_url',
            'ingredient_score',
            'nutrition_score',
            'content',
        )

        extra_kwargs = {
            'slug': {'required': False},
        }

        expandable_fields = {
            'ingredients': ('food.IngredientSerializer', {'many': True}),
            'health': ('food.FoodForSerializer', {'many': True}),
            'stage': ('food.FoodStageSerializer', {'many': True}),
            'brand': 'food.BrandSerializer',
            'type': 'food.FoodTypeSerializer',
            'image': ('document.ImageSerializer', {'many': True}),
            'calorie': 'food.FoodCalorieSerializer',
            'guaranteed': 'food.FoodGuaranteedSerializer',
            'drymatter': 'food.FoodDryMatterSerializer',

        }
