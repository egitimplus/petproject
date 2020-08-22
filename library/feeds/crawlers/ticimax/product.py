from library.models import ProductLink
from django.utils import timezone
from food.models import FoodSite
from django.db.models import F


class TicimaxProductCrawler:

    def __init__(self, **kwargs):
        self.__parent = kwargs.get('parent', None)
        self.__product = kwargs.get('product', None)
        self.__link = kwargs.get('productlink', None)
        self.__foodsite = FoodSite.objects.filter(url=self.parent.petshop.url + self.url).first()

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, value):
        self.__product = value

    @property
    def parent(self):
        return self.__parent

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
        return self.product.get('defaultUrl')

    @property
    def foodsite(self):
        return self.__foodsite

    @property
    def link(self):
        return self.__link

    def run(self):
        try:
            if self.foodsite is None:
                fs = FoodSite(
                    food=self.link.food,
                    url=self.url,
                    petshop=self.parent.petshop,
                    name=self.name,
                    old_price=self.old_price,
                    price=self.price,
                    stock=self.in_stock,
                    cargo=self.shipping,
                    updated=timezone.now,
                )

                fs.save()

            else:
                self.__foodsite.old_price = self.old_price
                self.__foodsite.price = self.price
                self.__foodsite.stock = self.in_stock
                self.__foodsite.cargo = self.shipping
                self.__foodsite.save()

            ProductLink.objects.filter(id=self.link.id).update(down=0, updated=timezone.now())
        except Exception as e:
            ProductLink.objects.filter(id=self.link.id).update(down=F('down')+1, updated=timezone.now())
