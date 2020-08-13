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
        self.dry_brands = ['3', '5', '13', '16', '37', '185', '25', '35', '116', '646', '420', '67', '66', '456', '408',
                           '424', '86', '238', '229', '250', '236', '645', '255', '296', '476', '253', '310', '500',
                           '177', '317', '648', '641', '97', '230', '484', '415', '332', '39', '360', '364', '367',
                           '365', '248', '370', '112', '118', '125', '127', '378', '138', '619', '379', '157', '170',
                           '407']
        self.wet_brands = ['16', '185', '35', '116', '420', '67', '66', '424', '86', '238', '229', '236', '255', '476',
                           '310', '566', '500', '177', '317', '97', '230', '415', '39,360', '248', '112', '118', '125',
                           '378', '138', '379', '170']
        self.brands = []

    # --type page

    def _page(self):

        for brand in self.brands:
            self._page_children(brand, 1)

    def _page_content(self, brand, page):
        url = 'https://www.petburada.com/api/product/GetProductList?FilterJson=%7B%22CategoryIdList%22%3A%5B' + self.food_type + '%5D%2C%22BrandIdList%22%3A%5B' + str(brand) + '%5D%2C%22SupplierIdList%22%3A%5B%5D%2C%22TagIdList%22%3A%5B%5D%2C%22TagId%22%3A-1%2C%22FilterObject%22%3A%5B%5D%2C%22MinStockAmount%22%3A-1%2C%22IsShowcaseProduct%22%3A-1%2C%22IsOpportunityProduct%22%3A-1%2C%22FastShipping%22%3A-1%2C%22IsNewProduct%22%3A-1%2C%22IsDiscountedProduct%22%3A-1%2C%22IsShippingFree%22%3A-1%2C%22IsProductCombine%22%3A-1%2C%22MinPrice%22%3A0%2C%22MaxPrice%22%3A0%2C%22SearchKeyword%22%3A%22%22%2C%22StrProductIds%22%3A%22%22%2C%22IsSimilarProduct%22%3Afalse%2C%22RelatedProductId%22%3A0%2C%22ProductKeyword%22%3A%22%22%2C%22PageContentId%22%3A0%2C%22StrProductIDNotEqual%22%3A%22%22%2C%22IsVariantList%22%3A-1%2C%22IsVideoProduct%22%3A-1%2C%22ShowBlokVideo%22%3A-1%2C%22VideoSetting%22%3A%7B%22ShowProductVideo%22%3A-1%2C%22AutoPlayVideo%22%3A-1%7D%2C%22ShowList%22%3A1%2C%22VisibleImageCount%22%3A6%2C%22ShowCounterProduct%22%3A-1%7D&PagingJson=%7B%22PageItemCount%22%3A0%2C%22PageNumber%22%3A' + str(page) + '%2C%22OrderBy%22%3A%22KATEGORISIRA%22%2C%22OrderDirection%22%3A%22ASC%22%7D&CreateFilter=false'
        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def _page_products(self, site_json):

        for product in site_json['products']:
            url = product.get('defaultUrl')
            brand = product.get('brand')
            name = product.get('name')

            link, created = ProductLink.objects.get_or_create(
                url='https://www.petburada.com' + url,
                defaults={
                    'brand': brand,
                    'name': name,
                    'food_type': self.food,
                    'petshop_id': 8
                }
            )
            
            if link.food_id is not None:
                try:
                    productId = product.get('productId')
                    totalStockAmount = product.get('totalStockAmount')
                    productCartPriceStr = product.get('productCartPriceStr')
                    productSellPriceStr = product.get('productSellPriceStr')
                    free_cargo = product.get('freeShipping')

                    old_price = productSellPriceStr.replace('TL', '').replace('₺', '').replace('.', '').replace(',', '.')
                    new_price = productCartPriceStr.replace('TL', '').replace('₺', '').replace('.', '').replace(',', '.')
                    in_stock = False
                    if totalStockAmount > 0:
                        in_stock = True

                    foodsite = FoodSite.objects.filter(url='https://www.petburada.com' + url).first()

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

                    self._product_comments(productId, link.food)

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

        source = self._product_content('https://www.petburada.com/api/product/GetComments?productId=' + str(productId))
        if source:
            comments = source.text
            comments = comments.replace('{"comments":[{"', '')
            comments = comments.replace('],"isError":false,"errorMessage":null,"errorCode":null,"model":null}', '')
            comments = comments.split('{')

            c = FoodComment.objects.filter(food_id=food.id, petshop_id=8).aggregate(max_date=Max('created'))

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
                            petshop_id=8,
                        )
                        fc.save()
    # command

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a type prefix', )
        parser.add_argument('-f', '--food', type=str, help='Define a food prefix', )

    def handle(self, *args, **options):
        crawl_type = options.get('type', None)
        food = options.get('food', None)

        if food == 'wet':
            self.food_type = '207'
            self.brands = self.wet_brands
        elif food == 'dry':
            self.food_type = '149'
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
