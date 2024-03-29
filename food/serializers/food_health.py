from food.models import FoodFor
from rest_flex_fields import FlexFieldsModelSerializer


class FoodForSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = FoodFor
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
