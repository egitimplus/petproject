from food.serializers import IngredientSerializer
from food.models import Ingredient
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_flex_fields.views import FlexFieldsMixin


class IngredientViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    lookup_field = 'slug'


