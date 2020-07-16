from food.models import FoodPackage
from rest_flex_fields import FlexFieldsModelSerializer


class FoodPackageSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = FoodPackage
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
