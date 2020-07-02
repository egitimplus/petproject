from food.models import DryMatter
from rest_flex_fields import FlexFieldsModelSerializer


class FoodDryMatterSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = DryMatter
        exclude = ('food', )

