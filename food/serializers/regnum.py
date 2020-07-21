from food.models import Regnum
from rest_flex_fields import FlexFieldsModelSerializer


class RegnumSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Regnum
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
