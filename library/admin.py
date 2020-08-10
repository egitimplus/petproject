from django.contrib import admin
from library.models import ProductLink
from food.models import Food
from urllib.parse import parse_qsl


@admin.register(ProductLink)
class ProductLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'food_type', 'food', 'petshop')
    list_filter = ('food_brand', 'down', 'active', 'food_type', 'brand')
    search_fields = ('name', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        obj_id = request.META['PATH_INFO'].rstrip('/').split('/')[-2]

        if db_field.name == 'food' and obj_id.isdigit():

            obj = self.get_object(request, obj_id)

            if obj:
                kwargs['queryset'] = Food.objects.filter(brand=obj.food_brand_id)

                if obj.food_type == 'dry':
                    kwargs['queryset'] = Food.objects.filter(brand=obj.food_brand_id, type_id=1)
                elif obj.food_type == 'wet':
                    kwargs['queryset'] = Food.objects.filter(brand=obj.food_brand_id, type_id=2)

        return super(ProductLinkAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
