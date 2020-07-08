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
            'brand',
            'type',
            'active'
        )

        extra_kwargs = {
            'slug': {'required': False, 'read_only':True},
            'active': {'write_only': True},
        }

        expandable_fields = {
            'ingredients': ('food.IngredientSerializer', {'many': True}),
            'health': ('food.FoodForSerializer', {'many': True}),
            'stage': ('food.FoodStageSerializer', {'many': True}),
            'brand': 'company.BrandSerializer',
            'type': 'food.FoodTypeSerializer',
            'image': ('document.ImageSerializer', {'many': True}),
            'calorie': 'food.FoodCalorieSerializer',
            'guaranteed': 'food.FoodGuaranteedSerializer',
            'drymatter': 'food.FoodDryMatterSerializer',
        }


