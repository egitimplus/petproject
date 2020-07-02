from django.db import models
from django.template.defaultfilters import slugify
import itertools


class Food(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024)
    slug = models.SlugField(unique=True, max_length=255)
    manufacturer_url = models.CharField(max_length=1024)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.PositiveSmallIntegerField(default=1)
    ingredient_score = models.PositiveSmallIntegerField()
    nutrition_score = models.PositiveSmallIntegerField()
    content = models.TextField()
    ingredients = models.ManyToManyField('food.Ingredient', through='food.FoodIngredient', related_name='foods')
    health = models.ManyToManyField('food.FoodFor', related_name='foods')
    stage = models.ManyToManyField('food.FoodStage', related_name='foods')
    image = models.ManyToManyField('document.Image', related_name='foods')
    brand = models.ForeignKey('company.Brand', on_delete=models.CASCADE)
    type = models.ForeignKey('food.FoodType', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None):

        if not self.id:
            name = self.name[:250] if len(self.name) > 250 else self.name
            self.slug = slugify(name)

            for x in itertools.count(1):
                if not Food.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (self.slug, x)

        super(Food, self).save()
