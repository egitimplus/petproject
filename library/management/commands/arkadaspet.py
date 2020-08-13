from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from library.models import ProductLink
from django.utils import timezone
from datetime import timedelta
from food.models import FoodSite


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.food_type = None
        self.food = None
        self.dry_brands = [
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
        self.wet_brands = [
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
        self.brands = []

    # --type page

    def _page(self):

        for brand in self.brands:
            source = self._page_content(brand)
            self._page_products(source, brand)
            self._page_children(source, brand)

    def _page_content(self, brand, page=None):

        url = 'https://www.arkadaspet.com/kategori/' + self.food_type + '?marka=' + brand

        if page is not None:
            url = url + '&tp=' + str(page)

        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def _page_products(self, source, brand):
        products = source.findAll("div", {"class": "showcaseTitle"})

        if products:
            for product in products:
                url = product.a.get('href')
                title = product.a.get('title')

                link, created = ProductLink.objects.get_or_create(
                    url='https://www.arkadaspet.com' + url,
                    defaults={
                        'brand': brand,
                        'name': title,
                        'food_type': self.food,
                        'petshop_id': 2
                    }
                )
        else:
            ProductLink.objects.filter(brand=brand, food_type=self.food).update(down=1)

    def _page_children(self, source, brand):
        pagination = source.find("div", {"class": "_paginateContent"})

        if pagination and pagination.ul:
            links = pagination.ul.find_all('li')

            if links:
                total = len(links)

                for i in range(1, total - 1):
                    split = links[i].a.get('href').split('?tp=')
                    source = self._page_content(brand, split[1])
                    self._page_products(source, brand)

    # --type product

    def _product(self):
        #last_update = timezone.now().date() - timedelta(0)
        #links = ProductLink.objects.filter(updated__lte=last_update, petshop_id=2, down=0, active=1, food__isnull=False).all()
        #links = ProductLink.objects.filter(petshop_id=2, down=1, active=1, food__isnull=False).all()
        links = ProductLink.objects.filter(petshop_id=2, down=0, active=1, food__isnull=False).all()

        for link in links:
            if link.food_id is not None:

                try:
                    source = self._product_content(link.url)

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
                except Exception as e:
                    print(e)
                    ProductLink.objects.filter(id=link.id).update(down=1, updated=timezone.now())

    def _product_content(self, url):
        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    # command

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a type prefix', )
        parser.add_argument('-f', '--food', type=str, help='Define a food prefix', )

    def handle(self, *args, **options):
        crawl_type = options.get('type', None)
        food = options.get('food', None)

        if food == 'wet':
            self.food_type = 'konserveler-yas-mamalar'
            self.brands = self.wet_brands
        elif food == 'dry':
            self.food_type = 'kuru-mamalar-1'
            self.brands = self.dry_brands

        if crawl_type is not None:
            if crawl_type == 'product':
                self._product()
            elif crawl_type == 'page':
                if self.food_type is not None:
                    self.food = food
                    self._page()
                else:
                    print('Seçim yapmadın  --food')
            else:
                print('Yanlış seçim yaptınız --type')
        else:
            print('Seçim yapmadın  --type')

        """
        --food : wet, dry
        --type : product, page
        """
