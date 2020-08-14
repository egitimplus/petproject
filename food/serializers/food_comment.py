from food.models import FoodComment
from rest_flex_fields import FlexFieldsModelSerializer
from company.serializers import PetShopSerializer


class FoodCommentSerializer(FlexFieldsModelSerializer):

    petshop = PetShopSerializer()

    class Meta:
        model = FoodComment
        fields = (
            'id',
            'name',
            'content',
            'created',
            'petshop',
            'user',
            'food',
            'rating'
        )
