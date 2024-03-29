from food.models import FoodStage
from rest_flex_fields import FlexFieldsModelSerializer


class FoodStageSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = FoodStage
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
