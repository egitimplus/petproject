from food.serializers import IngredientSerializer
from food.models import Ingredient
from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework.response import Response

'''
    {
        price: 15,
        images: [
            'images/products/acana-regionals-wild-prairie-1.png',
            'images/products/acana-regionals-wild-prairie-2.png',
            'images/products/acana-regionals-wild-prairie-3.jpg',
            'images/products/acana-regionals-wild-prairie-4.jpg',
        ],
        rating: 2,
        reviews: 5,
        availability: 'in-stock',
        brand: 'brandix',
        categories: ['instruments'],
        attributes: [
            { slug: 'color', values: ['pear-green', 'blue'] },
            { slug: 'speed', values: '750-rpm', featured: true },
            { slug: 'power-source', values: 'cordless-electric', featured: true },
            { slug: 'battery-cell-type', values: 'lithium', featured: true },
            { slug: 'voltage', values: '20-volts', featured: true },
            { slug: 'battery-capacity', values: '2-Ah', featured: true },
        ],
    },
    
    manufacturer_url
    ingredient_score
    nutrition_score
    content
    ingredients
    
'''

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