from food.models import Ingredient
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers


class IngredientSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'slug',
            'allergen',
            'slug',
            'active',
        )

        extra_kwargs = {
            'slug': {'required': False},
            'active': {'write_only': True},
        }

        expandable_fields = {
            'type': 'food.IngredientTypeSerializer',
            'quality': 'food.IngredientQualitySerializer',
            'parent': 'food.IngredientParentSerializer',
        }
