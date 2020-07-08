from document.serializers import ImageSerializer
from document.models import Image
from rest_flex_fields import FlexFieldsModelViewSet


class ImageViewSet(FlexFieldsModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
