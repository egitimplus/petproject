from django.contrib import admin
from library.models import ProductLinks


@admin.register(ProductLinks)
class ProductLinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'food_type', 'food', 'down', 'active')
    list_filter = ('brand', 'down', 'active', 'food_type')
