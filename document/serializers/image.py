from document.models import Image
from rest_flex_fields import FlexFieldsModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer


class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__192x192'),
        ]
    )

    class Meta:
        model = Image
        fields = (
            'id',
            'name',
            'image',
            'slug',
        )

        extra_kwargs = {
            'slug': {'required': False, 'read_only': True},
        }
