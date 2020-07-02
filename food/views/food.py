from food.serializers import FoodSerializer
from food.models import Food
from rest_flex_fields import FlexFieldsModelViewSet
from rest_flex_fields import is_expanded


class FoodViewSet(FlexFieldsModelViewSet):
    permit_list_expands = []
    serializer_class = FoodSerializer

    def get_queryset(self):
        queryset = Food.objects.all()

        expand = self.request.query_params.get("expand", "")

        for e in expand.split(","):
            l = e.split(".")

            if l[-1] == 'quality':
                queryset = queryset.prefetch_related('ingredients__quality')

            if l[-1] == 'ingredients':
                queryset = queryset.prefetch_related('ingredients')

        return queryset
