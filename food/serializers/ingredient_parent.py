from food.models import IngredientParent
from rest_flex_fields import FlexFieldsModelSerializer


class IngredientParentSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = IngredientParent
        fields = (
            'id',
            'name',
            'allergen',
            'active'
        )

        extra_kwargs = {
            'slug': {'required': False},
        }
