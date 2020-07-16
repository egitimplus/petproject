from django.contrib import admin
from company.models import Company, Brand



@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]
