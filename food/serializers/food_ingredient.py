from food.models import FoodIngredient
from rest_flex_fields import FlexFieldsModelSerializer


class FoodIngredientSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = FoodIngredient
        fields = (
            'ingredient_percent',
            'top_ingredient',
        )