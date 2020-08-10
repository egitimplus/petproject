from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from library.models import ProductLink
from django.utils import timezone
from datetime import timedelta
from food.models import FoodSite
from datetime import datetime


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.food_type = None
        self.food = None
        self.dry_brands = [
            '124', #acana
            '168', #bozita
            '42', #brit-care
            '162', #dr-sachi
            '121', #felicia
            '51', #golosi
            '66', #hills
            '114', #lavital
            '77',  # luis
            '89', #matisse
            '112',  # nd
            '7', #obivan
            '38', #orijen
            '83', #pro-plan
            '108', #pro-choice
            '371', #pro-performance
            '50', #proline
            '65', #purina-one
            '61', #reflex
            '79', #royal-canin
            '40', #sanabelle
        ]
        self.wet_brands = [
            '44', #animonda
            '122',#best-pet
            '168',  # bozita
            '42',  # brit-care
            '86', #chefs-choice
            '162', #dr-sachi
            '56', #felix
            '247', #gim-cat
            '51',  # golosi
            '87', #gourmet-gold
            '66', #hills
            '89', #matisse
            '381', #me-o
            '52', #miglior-gatto
            '112', #nd
            '7', #obivan
            '50', #proline
            '83', #pro-plan
            '61', #reflex
            '79', #royal-canin
            '85', #schesir
            '91', #vitacraft
        ]
        self.brands = []

    # --type page

    def _page(self):
        for brand in self.brands:
            source = self._page_content(brand)
            self._page_products(source, brand)
            self._page_children(brand)

    def _page_content(self, brand, page=1):

        url = 'https://www.markamama.com.tr/srv/service/product/loader?' + self.food_type + '&link=' + self.food_type + '&brand=' + str(brand) + '&pg=' + str(page)

        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def _page_products(self, source, brand):
        products = source.findAll("div", {"class": "col col-3 col-md-4 col-sm-6 col-xs-6 btm productItem ease"})

        if products:
            for product in products:

                br = product.find("a", {"class": "col col-12 productBrand"})
                url = product.a.get('href')
                title = product.img.get('alt')

                link, created = ProductLink.objects.get_or_create(
                    url='https://www.markamama.com.tr' + url,
                    defaults={
                        'brand': brand,
                        'name': title,
                        'food_type': self.food,
                        'petshop_id': 4
                    }
                )
        else:
            ProductLink.objects.filter(brand=brand, food_type=self.food).update(down=1)

    def _page_children(self, brand):
        for i in range(2, 100):
            source = self._page_content(brand, i)
            products = source.findAll("div", {"class": "col col-3 col-md-4 col-sm-6 col-xs-6 btm productItem ease"})

            if products:
                self._page_products(source, brand)
            else:
                break

    # --type product

    def _product(self):

        #last_update = timezone.now().date() - timedelta(0)
        #links = ProductLink.objects.filter(updated__lte=last_update, petshop_id=4, down=0, active=1, food__isnull=False).all()
        links = ProductLink.objects.filter(petshop_id=4, down=0, active=1, food__isnull=False).all()

        for link in links:
            if link.food_id is None:

                try:
                    source = self._product_content(link.url)

                    shippings = source.findAll("div", {"class": "box col-10 col-ml-1 krg"})

                    free_cargo = False

                    for shipping in shippings:
                        divs = shipping.findAll("div", {"class": "box col-8"})
                        for div in divs:
                            if div.text.strip() == 'Ücretsiz Kargo':
                                free_cargo = True

                    new_price = source.find("span", {"class": "product-price"})

                    if new_price:
                        new_price = new_price.text.strip().replace('.', '').replace(',', '.')
                    else:
                        new_price = 0

                    old_price = source.find("span", {"class": "product-price-not-discounted"})

                    if old_price:
                        old_price = old_price.text.strip().replace('.', '').replace(',', '.')
                    else:
                        old_price = new_price

                    in_stock = source.find("div", {"class": "fl col-12 add-to-cart-win inStock"})

                    if in_stock:
                        in_stock = True
                    else:
                        in_stock = False

                    skt = source.find("div", {"class": "sonkullanma"})

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
                            best_before=skt,
                            updated=timezone.now(),
                        )

                        new_site.save()

                    else:

                        foodsite.old_price = old_price
                        foodsite.price = new_price
                        foodsite.stock = in_stock
                        foodsite.cargo = free_cargo
                        foodsite.best_before = skt

                        foodsite.save()

                    ProductLink.objects.filter(id=link.id).update(down=0, updated=timezone.now())
                except:
                    ProductLink.objects.filter(id=link.id).update(down=1, updated=timezone.now())

    def _product_content(self, url):
        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    # command

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a username prefix', )
        parser.add_argument('-f', '--food', type=str, help='Define a food prefix', )

    def handle(self, *args, **options):
        crawl_type = options.get('type', None)
        food = options.get('food', None)

        if food == 'wet':
            self.food_type = 'kedi-konserve-mamalari'
            self.brands = self.wet_brands
        elif food == 'dry':
            self.food_type = 'kedi-mamasi'
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
