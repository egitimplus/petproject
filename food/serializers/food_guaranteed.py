from food.models import Guaranteed
from rest_flex_fields import FlexFieldsModelSerializer


class FoodGuaranteedSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Guaranteed
        exclude = ('food', )

