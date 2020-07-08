from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from food.views import FoodViewSet, IngredientViewSet, TypeViewSet
from document.views import ImageViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'food', FoodViewSet, basename='Food')
router.register(r'ingredient', IngredientViewSet, basename='Ingredient')
router.register(r'image', ImageViewSet, basename='Image')
router.register(r'categories', TypeViewSet, basename='FoodType')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls))
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
