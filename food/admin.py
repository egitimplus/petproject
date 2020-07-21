from django.contrib import admin
from food.models import Regnum, Food, Guaranteed, FoodFor, FoodStage, FoodType, Ingredient, IngredientType, IngredientQuality, IngredientParent, FoodSize, FoodPackage
from django.db.models import Count
# Register your models here.


class GuaranteedInline(admin.StackedInline):
    model = Guaranteed


class IngredientInline(admin.TabularInline):
    model = Food.ingredients.through


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    inlines = [GuaranteedInline, IngredientInline]
    list_display = ('name', 'brand', 'type', 'updated', 'active', 'user')
    list_filter = ['brand', 'type', 'package', 'size', 'health', 'stage', 'active', 'user']
    readonly_fields = ["slug", "ingredient_score", "nutrition_score", "total_score"]
    ordering = ['-id']


@admin.register(FoodFor)
class FoodForAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]


@admin.register(FoodSize)
class FoodSizeAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]


@admin.register(FoodStage)
class FoodStageAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]


@admin.register(FoodType)
class FoodTypeAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]
    list_display = ["name", "food_count"]

    def get_queryset(self, request):
        qs = super(FoodTypeAdmin, self).get_queryset(request)
        return qs.annotate(food_count=Count('food'))

    def food_count(self, inst):
        return inst.food_count

    food_count.admin_order_field = 'food_count'

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]
    list_display = ('name', 'parent', 'quality', 'count')
    list_filter = ('parent', 'quality')

    def get_queryset(self, request):
        qs = super(IngredientAdmin, self).get_queryset(request)
        return qs.annotate(ingredient_count=Count('foods'))

    def count(self, inst):
        return inst.ingredient_count

    count.admin_order_field = 'ingredient_count'


@admin.register(IngredientType)
class IngredientTypeAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]


@admin.register(IngredientQuality)
class IngredientQualityAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]
    list_display = ["name", "ingredient_count"]

    def get_queryset(self, request):
        qs = super(IngredientQualityAdmin, self).get_queryset(request)
        return qs.annotate(ingredient_count=Count('ingredient'))

    def ingredient_count(self, inst):
        return inst.ingredient_count

    ingredient_count.admin_order_field = 'ingredient_count'


@admin.register(IngredientParent)
class IngredientParentAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]
    list_display = ["name", "ingredient_count"]

    def get_queryset(self, request):
        qs = super(IngredientParentAdmin, self).get_queryset(request)
        return qs.annotate(ingredient_count=Count('ingredient'))

    def ingredient_count(self, inst):
        return inst.ingredient_count

    ingredient_count.admin_order_field = 'ingredient_count'


@admin.register(FoodPackage)
class FoodPackageAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]

@admin.register(Regnum)
class RegnumAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]
