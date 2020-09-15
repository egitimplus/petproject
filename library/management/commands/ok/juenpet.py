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
            'acana',
            'advance',
            'appetite',
            'beaphar',
            'bestpet',
            'bio-pet-active',
            'biyoteknik',
            'bozita',
            'brekkies',
            'brit',
            'croque',
            'dr-sacchi',
            'econature',
            'felicia',
            'gimcat',
            'hills',
            'jungle',
            'la-vital',
            'matisse',
            'naturea',
            'orijen',
            'paw-paw',
            'prochoice',
            'proplan',
            'purina',
            'royal-canin',
            'true-instinct',
            'whiskas'
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

    def _page_content(self, brand, page=1):

        url = 'https://www.juenpetmarket.com/' + self.food_type + '?m=' + brand + '&s=' + str(page)
        r = requests.get(url)
        encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None

        return BeautifulSoup(r.content, "lxml", from_encoding=encoding)

    def _page_products(self, source, brand):
        products = source.findAll("li", {"class": "col-xs-12 col-sm-4 col-md-4"})

        if products:
            for product in products:
                pr = product.find("div", {"class": "right-block"})

                url = pr.a.get('href')
                title = pr.a.text

                link, created = ProductLink.objects.get_or_create(
                    url='https://www.juenpetmarket.com' + url,
                    defaults={
                        'brand': brand,
                        'name': title,
                        'food_type': self.food,
                        'petshop_id': 5
                    }
                )
        else:
            ProductLink.objects.filter(brand=brand, food_type=self.food).update(down=1)

    def _page_children(self, source, brand):
        pagination = source.find("div", {"class": "pagination"})

        if pagination and pagination.ul:
            links = pagination.ul.find_all('li')

            if links:
                total = len(links) - 2

                if total > 1:
                    for i in range(2, total - 2):
                        source = self._page_content(brand, i)
                        self._page_products(source, brand)

    # --type product

    def _product(self):

        #last_update = timezone.now().date() - timedelta(0)
        #links = ProductLink.objects.filter(updated__lte=last_update, petshop_id=5, down=0, active=1, food__isnull=False).all()
        links = ProductLink.objects.filter(petshop_id=5, down=0, active=1, food__isnull=False).all()

        for link in links:
            if link.food_id is not None:

                try:
                    source = self._product_content(link.url)

                    old_price = source.find("span", {"class": "old-price"})

                    new_price1 = source.find("span", {"class": "price colorOrange"})
                    new_price2 = source.find("span", {"class": "priceDecimal colorOrange"})

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

                    if old_price:
                        old_price = old_price.text.strip().replace('TL', '').replace('.', '').replace(',', '.')
                    else:
                        old_price = new_price

                    in_stock = source.select("a[class*=btn-add-cart]")

                    if in_stock:
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
                            updated=timezone.now(),
                        )

                        new_site.save()

                    else:

                        foodsite.old_price = old_price
                        foodsite.price = new_price
                        foodsite.stock = in_stock

                        foodsite.save()

                    ProductLink.objects.filter(id=link.id).update(down=0, updated=timezone.now())
                except Exception as e:
                    print(e)
                    ProductLink.objects.filter(id=link.id).update(down=1, updated=timezone.now())

    def _product_content(self, url):
        r = requests.get(url)
        encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None

        return BeautifulSoup(r.content, "lxml", from_encoding=encoding)

    # command

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a type prefix', )
        parser.add_argument('-f', '--food', type=str, help='Define a food prefix', )

    def handle(self, *args, **options):
        crawl_type = options.get('type', None)
        food = options.get('food', None)

        if food == 'wet':
            self.food_type = 'konserve-kedi-mamasi-k-82'
            self.brands = self.wet_brands
        elif food == 'dry':
            self.food_type = 'kuru-kedi-mamasi-k-81'
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
