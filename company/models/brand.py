from django.db import models
from django.template.defaultfilters import slugify
import itertools


class Brand(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.PositiveSmallIntegerField(default=1)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None):

        if not self.id:

            self.slug = slugify(self.name)

            for x in itertools.count(1):
                if not Brand.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (self.slug, x)

        super(Brand, self).save()
