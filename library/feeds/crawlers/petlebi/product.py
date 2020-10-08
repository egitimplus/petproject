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
        old_price = self.product.find("p", {"class": "old-price"})

        if old_price:
            old_price = old_price.text.replace('TL', '').replace('.', '').replace(',', '.')

        return old_price

    @property
    def price(self):
        new_price = self.product.find("p", {"class": "new-price"})

        if new_price:
            new_price = new_price.text.replace('TL', '').replace('.', '').replace(',', '.')

        return new_price

    @property
    def in_stock(self):
        in_stock = self.product.find("span", {"class": "bg-light rounded pd-badge pd-stock-badge"})

        if in_stock:
            if in_stock.text.strip() == 'Tükendi':
                in_stock = False
            else:
                in_stock = True
        else:
            in_stock = False

        return in_stock

    @property
    def shipping(self):
        free_cargo = self.product.find("span", {"class": "bg-light rounded pd-badge pd-cargofree-badge mb-2"})

        if free_cargo:
            if free_cargo.text.strip() == 'Kargo Bedava!':
                free_cargo = True
            else:
                free_cargo = False
        else:
            free_cargo = False

        return free_cargo

    def specs(self):
        title = ''
        skt = None
        size = None

        specs = self.product.findAll("div", {"class": "row mb-2"})

        for spec in specs:
            for s in spec.children:

                if isinstance(s, NavigableString):
                    continue

                if isinstance(s, Tag):

                    if title == 'AĞIRLIK':
                        size = s.text.replace(' ', '').replace('gr', 'g').replace(',', '.').strip()

                    if title == 'S.K.T.':
                        skt = datetime.strptime(s.text, '%d/%m/%Y')
                        skt = timezone.make_aware(skt, timezone.get_current_timezone())

                    title = s.text

        foodsize = None

        if size is not None:
            foodsize = FoodSize.objects.filter(name=specs["size"]).first()

            if foodsize is None:
                foodsize = FoodSize(name=specs["size"])
                foodsize.save()

        return {
            "skt": skt,
            "size": foodsize
        }

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
            ProductLink.objects.filter(id=self.link.id).update(down=F('down') + 1, updated=timezone.now())

    def add_foodsite(self):
        specs = self.specs()

        FoodPromotion.objects.filter(food_id=self.link.food_id).delete()
        promotions = self.product.findAll("div", {"class": "p-1 bd-highlight"})

        if self.foodsite is None:

            new_site = FoodSite(
                name=self.name,
                food=self.link.food,
                petshop=self.petshop,
                url=self.url,
                old_price=self.old_price,
                price=self.price,
                stock=self.in_stock,
                cargo=self.shipping,
                size=specs["size"],
                best_before=specs["skt"],
                updated=timezone.now(),
            )

            new_site.save()

            for promotion in promotions:
                if promotion.a:
                    gift = FoodPromotion(
                        site=new_site,
                        name=promotion.find('a').contents[0].strip(),
                        food=self.link.food,
                    )

                    gift.save()
        else:

            self.foodsite.old_price = self.old_price
            self.foodsite.price = self.price
            self.foodsite.stock = self.in_stock
            self.foodsite.cargo = self.shipping
            self.foodsite.updated = timezone.now()

            self.foodsite.save()

            for promotion in promotions:
                if promotion.a:
                    gift = FoodPromotion(
                        site=self.foodsite,
                        name=promotion.find('a').contents[0].strip(),
                        food=self.link.food,
                    )

                    gift.save()
