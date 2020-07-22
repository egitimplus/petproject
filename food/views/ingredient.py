from food.serializers import IngredientSerializer
from food.models import Ingredient
from rest_flex_fields import FlexFieldsModelViewSet


class IngredientViewSet(FlexFieldsModelViewSet):

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    lookup_field = 'slug'


