from food.models import FoodSize
from rest_flex_fields import FlexFieldsModelSerializer


class FoodSizeSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = FoodSize
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
