from django.contrib import admin
from food.models import Dry, Regnum, Calorie, Food, FoodSite, Guaranteed, FoodComment, FoodFor, FoodStage, FoodType, Ingredient, IngredientType, IngredientQuality, IngredientParent, FoodSize, FoodPackage
from django.db.models import Count
# Register your models here.
from django_summernote.admin import SummernoteModelAdmin


class GuaranteedInline(admin.StackedInline):
    model = Guaranteed


class SiteInline(admin.TabularInline):
    model = FoodSite


class IngredientInline(admin.TabularInline):
    model = Food.ingredients.through


@admin.register(Food)
class FoodAdmin(SummernoteModelAdmin):
    inlines = [GuaranteedInline, IngredientInline, SiteInline]
    list_display = ('name', 'brand', 'serie', 'type', 'updated', 'active', 'user')
    list_filter = ['brand', 'type', 'package', 'size', 'health', 'stage', 'active', 'user']
    readonly_fields = ["slug", "ingredient_score", "nutrition_score", "total_score"]
    ordering = ['-id']
    summernote_fields = '__all__'


@admin.register(FoodSite)
class FoodSiteAdmin(admin.ModelAdmin):
    list_display = ('food', 'petshop', 'size', 'updated')
    list_filter = ('petshop', 'size')


@admin.register(FoodFor)
class FoodForAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]

@admin.register(FoodComment)
class FoodCommentAdmin(admin.ModelAdmin):
    pass

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

@admin.register(Dry)
class DryAdmin(admin.ModelAdmin):
    pass

@admin.register(Calorie)
class CalorieAdmin(admin.ModelAdmin):
    pass