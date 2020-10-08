from django.db.models import F
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from library.models import ProductLink
from django.utils import timezone
from food.models import FoodSite, FoodPromotion, FoodSize
from datetime import datetime


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

        old_price = self.product.find("span", {"class": "product-price-not-discounted"})

        if old_price:
            old_price = old_price.text.strip().replace('.', '').replace(',', '.')
        else:
            old_price = self.price

        return old_price

    @property
    def price(self):
        new_price = self.product.find("span", {"class": "product-price"})

        if new_price:
            new_price = new_price.text.strip().replace('.', '').replace(',', '.')
        else:
            new_price = 0

        return new_price

    @property
    def in_stock(self):
        in_stock = self.product.find("div", {"class": "fl col-12 add-to-cart-win inStock"})

        if in_stock:
            in_stock = True
        else:
            in_stock = False

        return in_stock

    @property
    def shipping(self):
        shippings = self.product.findAll("div", {"class": "box col-10 col-ml-1 krg"})

        free_cargo = False

        for shipping in shippings:
            divs = shipping.findAll("div", {"class": "box col-8"})
            for div in divs:
                if div.text.strip() == 'Ücretsiz Kargo':
                    free_cargo = True

        return free_cargo

    @property
    def url(self):
        return self.link.url

    @property
    def best_before(self):
        skt = self.product.find("div", {"class": "sonkullanma"})

        if skt:
            try:
                skt = skt.strong.text
                skt = skt.replace(',', '.').replace('/', '.').replace('-', '.')

                check_date = skt.split('.')

                if len(check_date) == 2:

                    if len(check_date[1]) == 2:
                        skt = datetime.strptime(skt, '%m.%y')
                        skt = timezone.make_aware(skt, timezone.get_current_timezone())
                    else:
                        skt = datetime.strptime(skt, '%m.%Y')
                        skt = timezone.make_aware(skt, timezone.get_current_timezone())
                else:
                    skt = datetime.strptime(skt, '%d.%m.%Y')
                    skt = timezone.make_aware(skt, timezone.get_current_timezone())
            except:
                skt = None

            return skt

    def run(self):
        try:
            self.product = self.crawl()
            if self.link.food:
                if self.foodsite is None:

                    new_site = FoodSite(
                        name=self.name,
                        food=self.link.food,
                        petshop=self.link.petshop,
                        url=self.link.url,
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
                    self.foodsite.best_before = self.best_before

                    self.foodsite.save()

            ProductLink.objects.filter(id=self.link.id).update(down=0, updated=timezone.now())

        except Exception as e:
            print(e)
            ProductLink.objects.filter(id=self.link.id).update(down=F('down') + 1, updated=timezone.now())
