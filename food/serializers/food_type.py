from food.models import FoodType
from rest_flex_fields import FlexFieldsModelSerializer


class FoodTypeSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = FoodType
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
