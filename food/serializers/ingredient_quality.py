from food.models import IngredientQuality
from rest_flex_fields import FlexFieldsModelSerializer


class IngredientQualitySerializer(FlexFieldsModelSerializer):

    class Meta:
        model = IngredientQuality
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
