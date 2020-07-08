from food.models import Food
import rest_framework_filters as filters


class FoodFilter(filters.FilterSet):
    min_score = filters.NumberFilter(field_name="ingredient_score", lookup_expr='gte')
    max_score = filters.NumberFilter(field_name="ingredient_score", lookup_expr='lte')

    class Meta:
        model = Food
        fields = ['id', 'name', 'ingredient_score', 'brand']
