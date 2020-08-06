from django.db import models
from django.utils import timezone


class ProductLink(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    food_type = models.CharField(max_length=255)
    url = models.URLField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=1)
    down = models.BooleanField(default=0)
    food = models.ForeignKey('food.Food', on_delete=models.SET_NULL, null=True, blank=True, related_name='productlink')
    petshop = models.ForeignKey('company.PetShop', on_delete=models.SET_NULL, null=True, blank=True, related_name='productlink')

    def __str__(self):
        return '%s - %s' % (self.brand, self.name)


class Product(models.Model):

    link = models.ForeignKey('library.ProductLink', on_delete=models.CASCADE, related_name='product')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    food_type = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    stock = models.BooleanField(default=1)
    free_cargo = models.BooleanField(default=0)
    cargo_day = models.PositiveSmallIntegerField(default=1)
    best_before = models.DateTimeField()
    code = models.CharField(max_length=255)
    weight = models.ForeignKey('food.FoodSize', on_delete=models.SET_NULL, null=True, blank=True, related_name='product')
    content = models.TextField()

    def __str__(self):
        return '%s - %s' % (self.brand, self.name)


class ProductGift(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('library.Product', on_delete=models.CASCADE, related_name='productgift')
    name = models.CharField(max_length=255)


class ProductComment(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('library.Product', on_delete=models.CASCADE, related_name='productcomment')
    name = models.CharField(max_length=255)
    post_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=0)
