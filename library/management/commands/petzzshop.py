from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from library.models import ProductLink
from django.utils import timezone
from food.models import FoodSite, FoodComment
import json
from django.db.models import Max
from datetime import datetime


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.food_type = None
        self.food = None
        self.dry_brands = ['45', '253', '264', '251', '283', '275', '96', '158', '252', '79', '9', '46', '48', '36',
                           '75', '280', '49', '47', '76', '37', '50', '41', '8', '43', '40', '42', '44', '159', '277',
                           '278', '7', '13', '28', '30', '255', '6', '34', '91']
        self.wet_brands = ['65', '251', '275', '96', '252', '12', '266', '46', '75', '94', '282', '57', '280', '15',
                           '16', '47', '76', '41', '43', '276', '40', '42', '32', '261', '257', '35', '7', '277', '150',
                           '30', '290', '6', '64', '180', '81', '254', '91']
        self.brands = []

    # --type page

    def _page(self):

        for brand in self.brands:
            self._page_children(brand, 1)

    def _page_content(self, brand, page):
        url = 'https://www.petzzshop.com/api/product/GetProductList?FilterJson=%7B%22CategoryIdList%22%3A%5B' + self.food_type + '%5D%2C%22BrandIdList%22%3A%5B' + str(brand) + '%5D%2C%22SupplierIdList%22%3A%5B%5D%2C%22TagIdList%22%3A%5B%5D%2C%22TagId%22%3A-1%2C%22FilterObject%22%3A%5B%5D%2C%22MinStockAmount%22%3A-1%2C%22IsShowcaseProduct%22%3A-1%2C%22IsOpportunityProduct%22%3A-1%2C%22IsNewProduct%22%3A-1%2C%22IsDiscountedProduct%22%3A-1%2C%22IsShippingFree%22%3A-1%2C%22IsProductCombine%22%3A-1%2C%22MinPrice%22%3A0%2C%22MaxPrice%22%3A0%2C%22SearchKeyword%22%3A%22%22%2C%22StrProductIds%22%3A%22%22%2C%22IsSimilarProduct%22%3Afalse%2C%22RelatedProductId%22%3A0%2C%22ProductKeyword%22%3A%22%22%2C%22PageContentId%22%3A0%2C%22StrProductIDNotEqual%22%3A%22%22%2C%22IsVariantList%22%3A-1%2C%22IsVideoProduct%22%3A-1%2C%22ShowBlokVideo%22%3A-1%2C%22VideoSetting%22%3A%7B%22ShowProductVideo%22%3A-1%2C%22AutoPlayVideo%22%3A-1%7D%2C%22ShowList%22%3A1%2C%22VisibleImageCount%22%3A6%2C%22ShowCounterProduct%22%3A-1%7D&PagingJson=%7B%22PageItemCount%22%3A0%2C%22PageNumber%22%3A' + str(page) + '%2C%22OrderBy%22%3A%22KATEGORISIRA%22%2C%22OrderDirection%22%3A%22ASC%22%7D&CreateFilter=true'
        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def _page_products(self, site_json):

        for product in site_json['products']:

            url = product.get('defaultUrl')
            brand = product.get('brand')
            name = product.get('name')

            link, created = ProductLink.objects.get_or_create(
                url='https://www.petzzshop.com' + url,
                defaults={
                    'brand': brand,
                    'name': name,
                    'food_type': self.food,
                    'petshop_id': 14
                }
            )

            if link.food_id is not None:
                try:
                    productId = product.get('productId')
                    totalStockAmount = product.get('totalStockAmount')
                    productCartPriceStr = product.get('productCartPriceStr')
                    productSellPriceStr = product.get('productSellPriceStr')
                    free_cargo = product.get('freeShipping')

                    old_price = productSellPriceStr.replace('₺', '').replace('.', '').replace(',', '.')
                    new_price = productCartPriceStr.replace('₺', '').replace('.', '').replace(',', '.')
                    in_stock = False
                    if totalStockAmount > 0:
                        in_stock = True

                    foodsite = FoodSite.objects.filter(url='https://www.petzzshop.com' + url).first()

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

                    self._product_comments(productId, link.food)
                    ProductLink.objects.filter(id=link.id).update(down=0, updated=timezone.now())
                except Exception as e:
                    print(e)
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

    def _product_content(self, url):
        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def _product_comments(self, productId, food):

        source = self._product_content('https://www.petzzshop.com/api/product/GetComments?productId=' + str(productId))
        if source:
            comments = source.text
            comments = comments.replace('{"comments":[{"', '')
            comments = comments.replace('],"isError":false,"errorMessage":null,"errorCode":null,"model":null}', '')
            comments = comments.split('{')

            c = FoodComment.objects.filter(food_id=food.id, petshop_id=14).aggregate(max_date=Max('created'))

            for comment in comments:

                content = comment.split('"comment":"')

                if len(content) > 1:
                    content = content[1].split('"}')

                    author = comment.split('"memberName":"')
                    author = author[1].split('",')

                    published = comment.split('"commentDateFormatted":"')
                    published = published[1].split('",')
                    published = published[0].split(' ')
                    published = datetime.strptime(published[0], '%d-%m-%Y')
                    published = timezone.make_aware(published, timezone.get_current_timezone())

                    save = 1 # daha sonra yeni yorumlar gelsin diye sıfır olacak

                    if c['max_date'] is None:
                        save = 1
                    elif published > c['max_date']:
                        save = 1

                    if save == 1:
                        fc = FoodComment(
                            food=food,
                            name=author[0],
                            created=published,
                            content=content[0],
                            rating=0,
                            petshop_id=14,
                        )
                        fc.save()
    # command
    # command

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a type prefix', )
        parser.add_argument('-f', '--food', type=str, help='Define a food prefix', )

    def handle(self, *args, **options):
        crawl_type = options.get('type', None)
        food = options.get('food', None)

        if food == 'wet':
            self.food_type = '26'
            self.brands = self.wet_brands
        elif food == 'dry':
            self.food_type = '25'
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
