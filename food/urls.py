from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from food.views import FoodViewSet


router = DefaultRouter()
router.register(r'food', FoodViewSet, basename='Food')

urlpatterns = [
    url(r'^', include(router.urls))
]