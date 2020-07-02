from company.models import Brand
from rest_flex_fields import FlexFieldsModelSerializer
from company.serializers import CompanySerializer


class BrandSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Brand
        fields = (
            'id',
            'name',
            'active',
            'created',
            'updated'
        )

        extra_kwargs = {
            'slug': {'required': False},
        }

        expandable_fields = {
          'company': CompanySerializer,
        }
