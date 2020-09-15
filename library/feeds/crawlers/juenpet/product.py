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
        encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None

        return BeautifulSoup(r.content, "lxml", from_encoding=encoding)

    @property
    def name(self):
        return self.link.name

    @property
    def old_price(self):
        old_price = self.product.find("span", {"class": "old-price"})

        if old_price:
            old_price = old_price.text.strip().replace('TL', '').replace('.', '').replace(',', '.')
        else:
            old_price = self.price

        return old_price

    @property
    def price(self):
        new_price1 = self.product.find("span", {"class": "price colorOrange"})
        new_price2 = self.product.find("span", {"class": "priceDecimal colorOrange"})

        if new_price1:
            new_price1 = int(new_price1.text.strip().replace('.', '').replace(',', ''))
        else:
            new_price1 = 0

        if new_price2:
            new_price2 = round(float(
                int(new_price2.text.strip().replace('TL', '').replace('.', '').replace(',', '')) / 100), 2)
        else:
            new_price2 = 0

        new_price = new_price1 + new_price2

        return new_price

    @property
    def in_stock(self):
        in_stock = self.product.select("a[class*=btn-add-cart]")

        if in_stock:
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



