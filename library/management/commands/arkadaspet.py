from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from library.models import ProductLink
from django.utils import timezone
from datetime import timedelta
from food.models import FoodSite


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a type prefix', )
        parser.add_argument('-f', '--food', type=str, help='Define a food prefix', )

    def get_brand_content(self, brand, food_type, page=None):

        url = 'https://www.arkadaspet.com/kategori/' + food_type + '?marka=' + brand

        if page is not None:
            url = url + '&tp=' + page

        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def get_food_content(self, url):
        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def add_products(self, source, brand, food_type):
        products = source.findAll("div", {"class": "showcaseTitle"})
        ft = 'wet'
        if food_type == 'kuru-mamalar-1':
            ft = 'dry'

        if products:
            for product in products:
                url = product.a.get('href')
                title = product.a.get('title')

                obj, created = ProductLink.objects.get_or_create(
                    brand=brand,
                    url='https://www.arkadaspet.com' + url,
                    name=title,
                    food_type=ft,
                    petshop_id=2
                )
        else:
            ProductLink.objects.filter(brand=brand, food_type=ft).update(down=1)

    def add_childs(self, source, brand, food_type):
        pagination = source.find("div", {"class": "_paginateContent"})

        if pagination and pagination.ul:
            links = pagination.ul.find_all('li')

            if links:
                total = len(links)

                for i in range(1, total - 1):
                    split = links[i].a.get('href').split('?tp=')
                    source = self.get_brand_content(brand, food_type, split[1])
                    self.add_products(source, brand, food_type)

    def _data_crate(self, food_type):

        brands = [
            'royal-canin',
            'dr-sacchi',
            'pro-plan',
            'trendline',
            'reflex',
            'orijen',
            'econature',
            'acana',
            'enjoy',
        ]

        wet_brands = [
            'felix',
            'whiskas',
            'miglior',
            'purina',
            'animonda',
            'royal-canin',
            'shinycat',
            'pro-plan',
            'orijen',
        ]

        if food_type == 'konserveler-yas-mamalar':
            brands = wet_brands

        for brand in brands:
            source = self.get_brand_content(brand, food_type)
            self.add_products(source, brand, food_type)
            self.add_childs(source, brand, food_type)

    def _product_crate(self):
        last_update = timezone.now().date() - timedelta(0)
        links = ProductLink.objects.filter(updated__lte=last_update, petshop_id=2, down=0, active=1, food__isnull=False).all()

        for link in links:
            if link.food_id is not None:

                try:
                    source = self.get_food_content(link.url)

                    old_price = source.find(id="kdv_dahil_cevrilmis_fiyat")
                    new_price = source.find(id="indirimli_cevrilmis_fiyat")
                    in_stock = source.find("div", {"class": "_floatLeft mR10"})

                    if new_price:
                        new_price = new_price.text.strip().replace('İndirimli ', '').replace('TL', '').replace('.', '').replace(',', '.')
                    else:
                        new_price = 0

                    if old_price:
                        old_price = old_price.text.strip().replace('TL', '').replace('.', '').replace(',', '.')
                    else:
                        old_price = new_price

                    if float(new_price) >= 100:
                        free_cargo = True
                    else:
                        free_cargo = False

                    if in_stock:
                        if in_stock.a.get('data-selector') == 'stock-warning':
                            in_stock = False
                        else:
                            in_stock = True
                    else:
                        in_stock = False

                    foodsite = FoodSite.objects.filter(url=link.url).first()

                    if foodsite is None:

                        new_site = FoodSite(
                            name=link.name,
                            food=link.food,
                            petshop=link.petshop,
                            url=link.url,
                            old_price=old_price,
                            price=new_price,
                            stock=in_stock,
                            cargo=free_cargo,
                            updated=timezone.now(),
                        )

                        new_site.save()

                    else:

                        foodsite.old_price = old_price
                        foodsite.price = new_price
                        foodsite.stock = in_stock
                        foodsite.cargo = free_cargo

                        foodsite.save()

                    ProductLink.objects.filter(id=link.id).update(down=0, updated=timezone.now())
                    print(timezone.now())
                except:
                    ProductLink.objects.filter(id=link.id).update(down=1, updated=timezone.now())


    def handle(self, *args, **options):
        crawl_type = options.get('type', None)
        food_type = options.get('food', None)

        if crawl_type is not None:
            if crawl_type == 'product':
                self._product_crate()
            elif crawl_type == 'page':
                self._data_crate(food_type)
            else:
                print('Yanlış seçim yaptınız --type')
        else:
            print('Seçim yapmadın')

        """
        --food
        kuru-mamalar-1
        konserveler-yas-mamalar
        
        --type
        product
        page
        """
