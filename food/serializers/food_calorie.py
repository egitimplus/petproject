from food.models import Calorie
from rest_flex_fields import FlexFieldsModelSerializer


class FoodCalorieSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Calorie
        exclude = ('food', )

