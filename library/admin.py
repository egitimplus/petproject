from django.contrib import admin
from library.models import ProductLink


@admin.register(ProductLink)
class ProductLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'food_type', 'food', 'down', 'active')
    list_filter = ('brand', 'down', 'active', 'food_type')
