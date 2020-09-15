from django.db import models
from django.template.defaultfilters import slugify
import itertools


class PetShop(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    slug = models.SlugField(unique=True, max_length=255)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.PositiveSmallIntegerField(default=1)
    image = models.ForeignKey('document.Image', related_name='petshop', on_delete=models.SET_NULL, blank=True, null=True)
    product_crawl = models.BooleanField(default=0)
    comment_crawl = models.BooleanField(default=0)
    type = models.PositiveSmallIntegerField(default=0)
    categories = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None):

        if not self.id:

            self.slug = slugify(self.name)

            for x in itertools.count(1):
                if not PetShop.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (self.slug, x)

        super(PetShop, self).save()
