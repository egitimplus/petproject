from django.db import models
from django.template.defaultfilters import slugify
import itertools


class IngredientType(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    active = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None):

        if not self.id:

            self.slug = slugify(self.name)

            for x in itertools.count(1):
                if not IngredientType.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (self.slug, x)

        super(IngredientType, self).save()
