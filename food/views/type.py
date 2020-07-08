from food.serializers import FoodTypeSerializer
from food.models import FoodType
from rest_flex_fields import FlexFieldsModelViewSet


class TypeViewSet(FlexFieldsModelViewSet):

    serializer_class = FoodTypeSerializer
    queryset = FoodType.objects.all()
