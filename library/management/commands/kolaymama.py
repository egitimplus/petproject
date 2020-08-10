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
        self.dry_brands = ['76', '66', '88', '253', '85', '196', '15', '89', '24', '236', '304', '81', '296', '285',
                           '343', '271', '87', '270', '75', '160', '129', '73', '290', '78', '79', '259', '68', '110',
                           '286', '227', '77', '7', '183', '8', '13', '67', '6', '289', '20', '80']
        self.wet_brands = ['86', '253', '196', '231', '339', '170', '24', '333', '296', '272', '102', '273', '160',
                           '302', '78', '326', '168', '109', '31', '325', '287', '79', '268', '226', '267', '338', '77',
                           '7', '301', '8', '107', '13', '218', '178', '303', '80']
        self.brands = []

    # --type page

    def _page(self):

        for brand in self.brands:
            source = self._page_content(brand)
            self._page_products(source, brand)
            self._page_children(source, brand)

    def _page_content(self, brand, page=None):

        url = 'https://www.kolaymama.com/' + self.food_type + '?brand=' + brand

        if page is not None:
            url = url + '&pg=' + str(page)

        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def _page_products(self, source, brand):
        products = source.findAll("div", {"class": "box col-3 col-md-4 col-sm-6 col-xs-6 productItem ease"})

        if products:
            for product in products:
                url = product.a.get('href')
                title = product.img.get('title')
                name = title.split(' - ')

                if len(name) > 2:
                    product_name = title.strip()
                    brand_name = name[0]

                elif len(name) < 2:
                    product_name = title
                    brand_name = brand
                else:
                    product_name = name[1].strip()
                    brand_name = name[0]

                link, created = ProductLink.objects.get_or_create(
                    url='https://www.kolaymama.com' + url,
                    defaults={
                        'brand': brand,
                        'name': product_name,
                        'food_type': self.food,
                        'petshop_id': 9
                    }
                )
        else:
            ProductLink.objects.filter(brand=brand, food_type=self.food).update(down=1)

    def _page_children(self, source, brand):
        pagination = source.find("div", {"class": "productPager"})

        if pagination:

            links = pagination.find_all('a')

            if links:
                total = len(links)

                for i in range(1, total-3):
                    source = self._page_content(brand, i)
                    self._page_products(source, brand)

    # --type product

    def _product(self):
        #last_update = timezone.now().date() - timedelta(0)
        #links = ProductLink.objects.filter(updated__lte=last_update, petshop_id=9, down=0, active=1, food__isnull=False).all()
        links = ProductLink.objects.filter(petshop_id=9, down=0, active=1, food__isnull=False).all()

        for link in links:
            if link.food_id is not None:

                try:
                    source = self._product_content(link.url)

                    old_price = source.find("span", {"class": "product-price-not-discounted"})
                    new_price = source.find("span", {"class": "product-price"})
                    in_stock = source.find("div", {"class": "fl col-12 add-to-cart-win inStock"})

                    if new_price:
                        new_price = new_price.text.strip().replace('İndirimli ', '').replace('TL', '').replace('.', '').replace(',', '.')
                    else:
                        new_price = 0

                    if old_price:
                        old_price = old_price.text.strip().replace('TL', '').replace('.', '').replace(',', '.')
                    else:
                        old_price = new_price

                    if float(new_price) >= 90:
                        free_cargo = True
                    else:
                        free_cargo = False

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
                except:
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
            self.food_type = 'kedi-yas-mamalar'
            self.brands = self.wet_brands
        elif food == 'dry':
            self.food_type = 'kedi-kuru-mamalar'
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
