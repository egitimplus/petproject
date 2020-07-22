from food.models import Ingredient
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from food.serializers import FoodIngredientSerializer
from food.models import FoodIngredient


class IngredientSerializer(FlexFieldsModelSerializer):

    stats = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        lookup_field = 'slug'
        fields = (
            'id',
            'name',
            'slug',
            'content',
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
            'image': ('document.ImageSerializer', {'many': True}),
        }

    def get_stats(self, obj):

        food_id = self.context.get('food_id', None)

        if food_id:
            data = FoodIngredient.objects.filter(food_id=self.context['food_id'], ingredient_id=obj.id).first()
            serializer = FoodIngredientSerializer(data)

            return serializer.data

        return []

