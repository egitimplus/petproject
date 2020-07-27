from document.serializers import ImageSerializer
from document.models import Image
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_flex_fields.views import FlexFieldsMixin


class ImageViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
