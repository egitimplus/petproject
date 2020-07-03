from company.models import Company
from rest_flex_fields import FlexFieldsModelSerializer


class CompanySerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'active',
            'slug'
        )

        extra_kwargs = {
            'slug': {'required': False},
            'active': {'write_only': True},
        }
