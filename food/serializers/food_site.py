from food.models import FoodSite
from rest_flex_fields import FlexFieldsModelSerializer
from company.serializers import PetShopSerializer


class FoodSiteSerializer(FlexFieldsModelSerializer):

    petshop = PetShopSerializer()

    class Meta:
        model = FoodSite
        fields = (
            'id',
            'name',
            'old_price',
            'price',
            'stock',
            'cargo',
            'best_before',
            'top_site',
            'url',
            'updated',
            'petshop',
            'food',
        )
