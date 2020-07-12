from food.models import Ingredient
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from food.serializers import FoodIngredientSerializer
from food.models import FoodIngredient

class IngredientSerializer(FlexFieldsModelSerializer):

    stats = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'slug',
            'allergen',
            'slug',
            'active',
            'stats'
        )

        extra_kwargs = {
            'slug': {'required': False, 'read_only':True},
            'active': {'write_only': True},
        }

        expandable_fields = {
            'type': 'food.IngredientTypeSerializer',
            'quality': 'food.IngredientQualitySerializer',
            'parent': 'food.IngredientParentSerializer',
        }

    def get_stats(self, obj):

        data = FoodIngredient.objects.filter(food_id=self.context['food_id'], ingredient_id=obj.id).first()
        serializer = FoodIngredientSerializer(data)
        return serializer.data
