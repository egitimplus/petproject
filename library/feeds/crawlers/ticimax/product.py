from library.models import ProductLink
from django.utils import timezone
from food.models import FoodSite
from django.db.models import F


class ProductCrawler:

    def __init__(self, **kwargs):

        parent = kwargs.get('parent', None)

        self.product = parent.prod
        self.link = parent.link
        self.petshop = parent.petshop

        self.foodsite = FoodSite.objects.filter(url=self.url).first()

    @property
    def name(self):
        return self.product.get('name')

    @property
    def old_price(self):
        return self.product.get('productCartPriceStr').replace('₺', '').replace('.', '').replace(',', '.')

    @property
    def price(self):
        return self.product.get('productSellPriceStr').replace('₺', '').replace('.', '').replace(',', '.')

    @property
    def in_stock(self):
        if self.product.get('totalStockAmount') > 0:
            return True

        return False

    @property
    def shipping(self):
        return self.product.get('freeShipping')

    @property
    def url(self):
        return self.petshop.url + self.product.get('defaultUrl')

    def run(self):
        try:
            if self.link.food:
                if self.foodsite is None:

                    fs = FoodSite(
                        food=self.link.food,
                        url=self.url,
                        petshop=self.petshop,
                        name=self.name,
                        old_price=self.old_price,
                        price=self.price,
                        stock=self.in_stock,
                        cargo=self.shipping,
                        updated=timezone.now,
                    )

                    fs.save()

                else:
                    self.foodsite.old_price = self.old_price
                    self.foodsite.price = self.price
                    self.foodsite.stock = self.in_stock
                    self.foodsite.cargo = self.shipping
                    self.foodsite.save()

            ProductLink.objects.filter(id=self.link.id).update(down=0, updated=timezone.now())
        except Exception as e:
            ProductLink.objects.filter(id=self.link.id).update(down=F('down')+1, updated=timezone.now())
