from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from library.models import ProductLink
from django.utils import timezone
from food.models import FoodSite
import json


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.food_type = None
        self.food = None
        self.dry_brands = [
            '2', #acana
            '7', #advance
            '17', #dr-sachi
            '6', #hills
            '4', #nd
            '1', #orijen
            '3', #pro-plan
            '9', #reflex
            '5', #royal-canin
        ]
        self.wet_brands = [
            '78', #animonda
            '12', #gim-cat
            '6', #hills
            '25', #miglior-gatto
            '4', #nd
            '10', #pro-line
            '3', #pro-plan
            '9', #reflex
            '5', #royal-canin
            '49', #schesir
        ]
        self.brands = []

    # --type page

    def _page(self):

        for brand in self.brands:
            self._page_children(brand, 1)

    def _page_content(self, brand, page):
        url = 'https://www.zoopet.com.tr/api/product/GetProductList?FilterJson=%7B%22CategoryIdList%22%3A%5B' + self.food_type + '%5D%2C%22BrandIdList%22%3A%5B' + str(brand) + '%5D%2C%22SupplierIdList%22%3A%5B%5D%2C%22TagIdList%22%3A%5B%5D%2C%22TagId%22%3A-1%2C%22FilterObject%22%3A%5B%5D%2C%22MinStockAmount%22%3A-1%2C%22IsShowcaseProduct%22%3A-1%2C%22IsOpportunityProduct%22%3A-1%2C%22FastShipping%22%3A-1%2C%22IsNewProduct%22%3A-1%2C%22IsDiscountedProduct%22%3A-1%2C%22IsShippingFree%22%3A-1%2C%22IsProductCombine%22%3A-1%2C%22MinPrice%22%3A0%2C%22MaxPrice%22%3A0%2C%22SearchKeyword%22%3A%22%22%2C%22StrProductIds%22%3A%22%22%2C%22IsSimilarProduct%22%3Afalse%2C%22RelatedProductId%22%3A0%2C%22ProductKeyword%22%3A%22%22%2C%22PageContentId%22%3A0%2C%22StrProductIDNotEqual%22%3A%22%22%2C%22IsVariantList%22%3A-1%2C%22IsVideoProduct%22%3A-1%2C%22ShowBlokVideo%22%3A-1%2C%22VideoSetting%22%3A%7B%22ShowProductVideo%22%3A-1%2C%22AutoPlayVideo%22%3A-1%7D%2C%22ShowList%22%3A1%2C%22VisibleImageCount%22%3A6%2C%22ShowCounterProduct%22%3A-1%7D&PagingJson=%7B%22PageItemCount%22%3A0%2C%22PageNumber%22%3A' + str(page) + '%2C%22OrderBy%22%3A%22KATEGORISIRA%22%2C%22OrderDirection%22%3A%22ASC%22%7D&CreateFilter=false'
        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def _page_products(self, site_json):

        for product in site_json['products']:

            url = product.get('defaultUrl')
            brand = product.get('brand')
            name = product.get('name')

            link, created = ProductLink.objects.get_or_create(
                url='https://www.zoopet.com.tr' + url,
                defaults={
                    'brand': brand,
                    'name': name,
                    'food_type': self.food,
                    'petshop_id': 7
                }
            )
            if link.food_id is not None:
                try:
                    totalStockAmount = product.get('totalStockAmount')
                    productCartPriceStr = product.get('productCartPriceStr')
                    productSellPriceStr = product.get('productSellPriceStr')
                    free_cargo = product.get('freeShipping')

                    old_price = productSellPriceStr.replace('₺', '').replace('.', '').replace(',', '.')
                    new_price = productCartPriceStr.replace('₺', '').replace('.', '').replace(',', '.')
                    in_stock = False
                    if totalStockAmount > 0:
                        in_stock = True

                    foodsite = FoodSite.objects.filter(url='https://www.zoopet.com.tr' + url).first()

                    if foodsite is None:

                        new_site = FoodSite(
                            name=name,
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

    def _page_children(self, brand, page):
        source = self._page_content(brand, page)
        site_json = json.loads(source.text)

        totalProductCount = site_json.get('totalProductCount')
        nextProductCount = site_json.get('nextProductCount')
        currentPage = site_json.get('currentPage')

        if totalProductCount > 0:
            self._page_products(site_json)

            if nextProductCount > 0:
                self._page_children(brand, currentPage+1)

    # command

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a type prefix', )
        parser.add_argument('-f', '--food', type=str, help='Define a food prefix', )

    def handle(self, *args, **options):
        crawl_type = options.get('type', None)
        food = options.get('food', None)

        if food == 'wet':
            self.food_type = '54'
            self.brands = self.wet_brands
        elif food == 'dry':
            self.food_type = '37'
            self.brands = self.dry_brands

        if crawl_type is not None:
            if crawl_type == 'page':
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
