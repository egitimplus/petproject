from food.models import IngredientQuality
from rest_flex_fields import FlexFieldsModelSerializer


class IngredientQualitySerializer(FlexFieldsModelSerializer):

    class Meta:
        model = IngredientQuality
        fields = (
            'id',
            'name',
        )

        extra_kwargs = {
            'slug': {'required': False},
        }
