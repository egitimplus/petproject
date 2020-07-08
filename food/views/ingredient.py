from food.serializers import IngredientSerializer
from food.models import Ingredient
from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework.response import Response


class IngredientViewSet(FlexFieldsModelViewSet):

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(queryset, expand=["quality"], many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, expand=["quality"], many=True)
        return Response(serializer.data)