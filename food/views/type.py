from food.serializers import FoodTypeSerializer
from food.models import FoodType
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_flex_fields.views import FlexFieldsMixin


class TypeViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):

    serializer_class = FoodTypeSerializer
    queryset = FoodType.objects.all()
