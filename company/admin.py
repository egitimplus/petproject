from django.contrib import admin
from company.models import Company, Brand, PetShop, Site, Serie


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]


@admin.register(PetShop)
class PetShopAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass
