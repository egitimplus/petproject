from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from library.models import ProductLink
from django.utils import timezone
from food.models import FoodSite
import json


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a type prefix', )
        parser.add_argument('-f', '--food', type=str, help='Define a food prefix', )

    def get_brand_content(self, brand, food_type, page):

        url = 'https://www.petgross.com/api/product/GetProductList?FilterJson=%7B%22CategoryIdList%22%3A%5B' + str(food_type) + '%5D%2C%22BrandIdList%22%3A%5B' + str(brand) + '%5D%2C%22SupplierIdList%22%3A%5B%5D%2C%22TagIdList%22%3A%5B%5D%2C%22TagId%22%3A-1%2C%22FilterObject%22%3A%5B%5D%2C%22MinStockAmount%22%3A-1%2C%22IsShowcaseProduct%22%3A-1%2C%22IsOpportunityProduct%22%3A-1%2C%22IsNewProduct%22%3A-1%2C%22IsDiscountedProduct%22%3A-1%2C%22IsShippingFree%22%3A-1%2C%22IsProductCombine%22%3A-1%2C%22MinPrice%22%3A0%2C%22MaxPrice%22%3A0%2C%22SearchKeyword%22%3A%22%22%2C%22StrProductIds%22%3A%22%22%2C%22IsSimilarProduct%22%3Afalse%2C%22RelatedProductId%22%3A0%2C%22ProductKeyword%22%3A%22%22%2C%22PageContentId%22%3A0%2C%22StrProductIDNotEqual%22%3A%22%22%2C%22IsVariantList%22%3A-1%2C%22IsVideoProduct%22%3A-1%2C%22ShowBlokVideo%22%3A-1%2C%22VideoSetting%22%3A%7B%22ShowProductVideo%22%3A-1%2C%22AutoPlayVideo%22%3A-1%7D%2C%22ShowList%22%3A1%2C%22VisibleImageCount%22%3A6%2C%22ShowCounterProduct%22%3A-1%7D&PagingJson=%7B%22PageItemCount%22%3A0%2C%22PageNumber%22%3A' + str(page) + '%2C%22OrderBy%22%3A%22KATEGORISIRA%22%2C%22OrderDirection%22%3A%22ASC%22%7D&CreateFilter=true'
        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def _data_crate(self, food_type, page=1):

        brands = [
            '12', #acana
            '115', #advance
            '223', #amity
            '224', #bravery
            '250', #brit-care
            '70',#cat-chow
            '95', #dr-sachi
            '135', #eco-nature
            '273', #enjoy
            '406', #felicia
            '76', #friskies
            '113', #go-cat
            '426', #hills
            '62', #hills
            '338', #instinct
            '288', #king
            '207', #lavital
            '31', #nd
            '119', #natures-protection
            '414', #orijen
            '45', #orijen
            '332', #pro-plan
            '175', #pro-choice
            '226', #profine
            '311', #proline
            '20', #reflex
            '34', #royal-canin
            '51', #sanabelle
        ]

        wet_brands = [
            '429', #animonda
            '174',#chefs-choice
            '29', #dr-clauders
            '95', #dr-sachi
            '406', #felicia
            '78', #felix
            '42', #gim-cat
            '57', #gourmet-gold
            '426', #hills
            '62', #hills
            '44', #matisse
            '168', #miamor
            '50', #miglior-cane
            '86', #miglior-gatto
            '31', #nd
            '283', #nutri-feline
            '368', #patimax
            '363', #perfect
            '281', #plasir
            '98', #prevital
            '332', #pro-plan
            '20', #reflex
            '165', #rokus
            '34', #royal-canin
            '116', #schesir
            '316', #single
            '89', #stuzzy
            '23', #tommy
            '65', #whiskas
        ]

        page = 1

        if food_type == '49':
            brands = wet_brands

        for brand in brands:
            self._add_children(brand, food_type, page)

    def _add_children(self, brand, food_type, page):
        source = self.get_brand_content(brand, food_type, page)
        site_json = json.loads(source.text)

        totalProductCount = site_json.get('totalProductCount')
        nextProductCount = site_json.get('nextProductCount')
        currentPage = site_json.get('currentPage')

        if totalProductCount > 0:
            self._add_products(site_json, food_type)

            if nextProductCount > 0:
                self._add_children(brand, food_type, currentPage+1)

    def _add_products(self, site_json, food_type):

        for product in site_json['products']:

            url = product.get('defaultUrl')
            brand = product.get('brand')
            name = product.get('name')

            link, created = ProductLink.objects.get_or_create(
                brand=brand,
                url='https://www.petgross.com' + url,
                name=name,
                food_type=food_type,
                petshop_id=3
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

                    foodsite = FoodSite.objects.filter(url='https://www.petgross.com' + url).first()

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

    def handle(self, *args, **options):
        crawl_type = options.get('type', None)
        food_type = options.get('food', None)

        if crawl_type is not None:
            if crawl_type == 'page':
                self._data_crate(food_type)
            else:
                print('Yanlış seçim yaptınız --type')
        else:
            print('Seçim yapmadın')

        """
        --food
        71 <- kedi-kuru-mamalari
        49 <- kedi-yas-mamalari
        
        --type
        product
        page
        """
