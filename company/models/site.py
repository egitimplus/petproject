from django.db import models


class Site(models.Model):

    id = models.AutoField(primary_key=True)
    company = models.ForeignKey('company.PetShop', on_delete=models.CASCADE, related_name='site')
    url = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return '%s - %i' % (self.company.name, self.id)

