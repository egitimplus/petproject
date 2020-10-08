from django.db.models import F
from bs4 import BeautifulSoup
import requests
from library.models import ProductLink
from django.utils import timezone
from food.models import FoodSite


class ProductCrawler:

    def __init__(self, **kwargs):

        parent = kwargs.get('parent', None)

        self.product = None
        self.link = parent.link
        self.petshop = parent.petshop
        self.foodsite = FoodSite.objects.filter(url=self.url).first()

    def crawl(self):
        r = requests.get(self.url)
        return BeautifulSoup(r.content, "lxml")

    @property
    def name(self):
        return self.link.name

    @property
    def old_price(self):
        old_price = self.product.find(id="kdv_dahil_cevrilmis_fiyat")
        if old_price:
            old_price = old_price.text.strip().replace('TL', '').replace('.', '').replace(',', '.')
        else:
            old_price = self.price

        return old_price

    @property
    def price(self):
        new_price = self.product.find(id="indirimli_cevrilmis_fiyat")
        if new_price:
            new_price = new_price.text.strip().replace('İndirimli ', '').replace('TL', '').replace('.', '').replace(
                ',', '.')
        else:
            new_price = 0

        return new_price

    @property
    def in_stock(self):
        in_stock = self.product.find("div", {"class": "_floatLeft mR10"})
        if in_stock:
            if in_stock.a.get('data-selector') == 'stock-warning':
                in_stock = False
            else:
                in_stock = True
        else:
            in_stock = False

        return in_stock

    @property
    def shipping(self):
        if float(self.price) >= 100:
            free_cargo = True
        else:
            free_cargo = False

        return free_cargo

    @property
    def url(self):
        return self.link.url

    def run(self):
        try:
            self.product = self.crawl()
            if self.link.food:
                self.add_foodsite()
            ProductLink.objects.filter(id=self.link.id).update(down=0, updated=timezone.now())

        except Exception as e:
            print(e)
            ProductLink.objects.filter(id=self.link.id).update(down=F('down') + 1, updated=timezone.now())

    def add_foodsite(self):

        if self.foodsite is None:
            new_site = FoodSite(
                name=self.name,
                food=self.link.food,
                petshop=self.link.petshop,
                url=self.url,
                old_price=self.old_price,
                price=self.price,
                stock=self.in_stock,
                cargo=self.shipping,
                updated=timezone.now(),
            )

            new_site.save()
        else:

            self.foodsite.old_price = self.old_price
            self.foodsite.price = self.price
            self.foodsite.stock = self.in_stock
            self.foodsite.cargo = self.shipping

            self.foodsite.save()

