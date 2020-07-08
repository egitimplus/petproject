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
            'slug'
        )

        extra_kwargs = {
            'slug': {'required': False, 'read_only':True},
            'active': {'write_only': True},
        }

        expandable_fields = {
          'company': CompanySerializer,
        }
