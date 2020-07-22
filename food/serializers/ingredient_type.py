from food.models import Ingredient
from rest_flex_fields import FlexFieldsModelSerializer


class IngredientTypeSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'slug',
            'active'
        )

        extra_kwargs = {
            'slug': {'required': False, 'read_only':True},
            'active': {'write_only': True},
        }
