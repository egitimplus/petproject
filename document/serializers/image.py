from document.models import Image
from rest_flex_fields import FlexFieldsModelSerializer


class ImageSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Image
        fields = (
            'id',
            'name',
            'file',
            'active',
        )

        extra_kwargs = {
            'slug': {'required': False},
        }
