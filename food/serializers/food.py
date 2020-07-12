from rest_flex_fields import FlexFieldsModelSerializer
from food.models import Food
from food.serializers import FoodIngredientSerializer


class FoodSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Food
        lookup_field = 'slug'
        fields = (
            'id',
            'name',
            'slug',
            'manufacturer_url',
            'ingredient_score',
            'nutrition_score',
            'content',
            'brand',
            'type',
            'created',
            'active',
        )

        extra_kwargs = {
            'slug': {'required': False, 'read_only':True},
            'active': {'write_only': True},
        }

        expandable_fields = {
            'ingredients': ('food.IngredientSerializer', {'many': True}),
            'health': ('food.FoodForSerializer', {'many': True}),
            'stage': ('food.FoodStageSerializer', {'many': True}),
            'brand': 'company.BrandSerializer',
            'type': 'food.FoodTypeSerializer',
            'image': ('document.ImageSerializer', {'many': True}),
            'guaranteed': 'food.FoodGuaranteedSerializer',
        }

    def to_representation(self, instance):
        self.context['food_id'] = instance.id
        return super(FoodSerializer, self).to_representation(instance)
