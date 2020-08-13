from company.models import PetShop
from rest_flex_fields import FlexFieldsModelSerializer
from document.serializers import ImageSerializer


class PetShopSerializer(FlexFieldsModelSerializer):

    image = ImageSerializer()

    class Meta:
        model = PetShop
        fields = (
            'id',
            'name',
            'active',
            'slug',
            'url',
            'image'
        )

        extra_kwargs = {
            'slug': {'required': False, 'read_only':True},
            'active': {'write_only': True},
        }
