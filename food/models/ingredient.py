from django.db import models
from django.template.defaultfilters import slugify
import itertools


class Ingredient(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024)
    slug = models.SlugField(unique=True, max_length=255)
    active = models.PositiveSmallIntegerField(default=1)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    type = models.ForeignKey('food.IngredientType', on_delete=models.CASCADE)
    parent = models.ForeignKey('food.IngredientParent', on_delete=models.CASCADE)
    quality = models.ForeignKey('food.IngredientQuality', on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None):

        if not self.id:
            name = self.name[:250] if len(self.name) > 250 else self.name
            self.slug = slugify(name)

            for x in itertools.count(1):
                if not Ingredient.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (self.slug, x)

        super(Ingredient, self).save()
