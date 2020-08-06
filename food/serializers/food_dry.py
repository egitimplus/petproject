from food.models import Dry
from rest_flex_fields import FlexFieldsModelSerializer


class FoodDrySerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Dry
        exclude = ('food', )

