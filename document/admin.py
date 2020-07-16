from django.contrib import admin
from document.models import Image
# Register your models here.


@admin.register(Image)
class ImagedAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]


