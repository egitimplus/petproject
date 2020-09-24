from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class FoodComment(models.Model):
    id = models.AutoField(primary_key=True)
    food = models.ForeignKey('food.Food', on_delete=models.CASCADE, related_name='foodcomment')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    petshop = models.ForeignKey('company.PetShop', on_delete=models.SET_NULL, null=True, blank=True, related_name='foodcomment')

    class Meta:
        ordering = ['-created']
