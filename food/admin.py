from django.contrib import admin
from food.models import Food, Guaranteed, FoodFor, FoodStage, FoodType, Ingredient, IngredientType, IngredientQuality, IngredientParent
from document.models import Image
# Register your models here.


class GuaranteedInline(admin.StackedInline):
    model = Guaranteed


class IngredientInline(admin.TabularInline):
    model = Food.ingredients.through


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    inlines = [GuaranteedInline, IngredientInline]
    list_display = ('name', 'brand', 'type', 'updated', 'active', 'user')
    list_filter = ['brand', 'type', 'health', 'stage', 'active', 'user']


admin.site.register(FoodFor)
admin.site.register(FoodStage)
admin.site.register(FoodType)
admin.site.register(Ingredient)
admin.site.register(IngredientType)
admin.site.register(IngredientQuality)
admin.site.register(IngredientParent)
