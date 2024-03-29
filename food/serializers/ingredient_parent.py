from food.models import IngredientParent
from rest_flex_fields import FlexFieldsModelSerializer


class IngredientParentSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = IngredientParent
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

        expandable_fields = {
            'regnum': 'food.RegnumSerializer',
        }
