from django.db import models
from django.template.defaultfilters import slugify
import itertools
from django.contrib.auth.models import User


class Food(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255)
    manufacturer_url = models.CharField(max_length=1024)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.PositiveSmallIntegerField(default=1)
    ingredient_score = models.PositiveSmallIntegerField(default=0)
    nutrition_score = models.PositiveSmallIntegerField(default=0)
    total_score = models.PositiveSmallIntegerField(default=0)
    content = models.TextField()
    desc = models.TextField(null=True, blank=True)
    ingredients = models.ManyToManyField('food.Ingredient', through='food.FoodIngredient', related_name='foods')
    health = models.ManyToManyField('food.FoodFor', related_name='foods')
    size = models.ManyToManyField('food.FoodSize', related_name='foods')
    stage = models.ManyToManyField('food.FoodStage', related_name='foods')
    image = models.ManyToManyField('document.Image', related_name='foods')
    package = models.ForeignKey('food.FoodPackage', on_delete=models.CASCADE)
    brand = models.ForeignKey('company.Brand', on_delete=models.CASCADE)
    type = models.ForeignKey('food.FoodType', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    serie = models.ForeignKey('company.Serie', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Cat Food"
        verbose_name_plural = "Cat Foods"

    def __str__(self):
        return self.name + ' - ' + self.size.first().name

    def save(self, force_insert=False, force_update=False, using=None):

        if self.serie:
            slug = self.brand.name + '-' + self.serie.name
        else:
            slug = self.brand.name

        name = self.name[:250] if len(self.name) > 250 else self.name
        slug = slug + '-' + name

        self.slug = slugify(slug)

        x = 0
        if self.id:
            for x in itertools.count(1):
                if not Food.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                    break
        else:
            for x in itertools.count(1):
                if not Food.objects.filter(slug=self.slug).exists():
                    break

        if x > 1:
            self.slug = '%s-%d' % (self.slug, x)

        super(Food, self).save()
