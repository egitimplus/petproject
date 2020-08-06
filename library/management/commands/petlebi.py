from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from library.models import ProductLink
from django.utils import timezone
from datetime import timedelta
from food.models import FoodSite, FoodComment, FoodPromotion, FoodSize
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a username prefix', )

    def get_brand_content(self, brand, food_type, page=None):

        url = 'https://www.petlebi.com/' + brand + '/' + food_type

        if page is not None:
            url = url + '?page=' + page

        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def get_food_content(self, url):
        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def add_products(self, source, brand, food_type):
        products = source.findAll("div", {"class": "card-body pb-0"})

        if products:
            for product in products:
                url = product.a.get('href')
                name = product.find("h3", {"class": "commerce-title mt-2 mb-0"})

                obj, created = ProductLink.objects.get_or_create(
                    brand=brand,
                    url=url,
                    name=name.text,
                    food_type=food_type,
                    petshop_id=1
                )
        else:
            ProductLink.objects.filter(brand=brand, food_type=food_type).update(down=1)

    def add_childs(self, source, brand, food_type):
        pagination = source.find(id="pagination_area")

        if pagination and pagination.ul:
            links = pagination.ul.find_all('li')

            if links:
                total = len(links)

                for i in range(1, total - 1):
                    split = links[i].a.get('href').split('?page=')
                    source = self.get_brand_content(brand, food_type, split[1])
                    self.add_products(source, brand, food_type)

    def _data_crate(self):

        brands = [
            'acana',
            'advance',
            'amity',
            'appettite',
            'benefit',
            'best-pet',
            'bravery',
            'brekkies',
            'brit-care',
            'croque',
            'dr-sacchi',
            'felicia',
            'happy-cat',
            'hills',
            'instinct',
            'jungle',
            'la-cat',
            'matisse',
            'mystic',
            'nd',
            'orijen',
            'paw-paw',
            'petlebi',
            'pro-choice',
            'pro-performance',
            'pro-plan',
            'profine',
            'purina-one',
            'reflex',
            'royal-canin',
            'trendline',
            'van-cat',
            'whiskas'
        ]

        wet_brands = [
            'animonda',
            'best-pet',
            'bonnie',
            'brit-care',
            'chefs-choice',
            'club4paws',
            'dr-sacchi',
            'eurocat',
            'felicia',
            'felix',
            'gimpet',
            'gourmet',
            'hills',
            'jungle',
            'master',
            'me-o',
            'miglior-gatto',
            'nd',
            'naturon',
            'nutri',
            'plaisir',
            'pro-line',
            'pro-plan',
            'quik',
            'reflex',
            'rokus',
            'royal-canin',
            'schesir',
            'sheba',
            'simba',
            'stuzzy',
            'vitakraft',
            'whiskas'
        ]

        food_types = [
            'kedi-mamasi',
            'kedi-konserve-mamasi'
        ]

        for food_type in food_types:
            if food_type == 'kedi-konserve-mamasi':
                brands = wet_brands

            for brand in brands:
                source = self.get_brand_content(brand, food_type)
                self.add_products(source, brand, food_type)
                self.add_childs(source, brand, food_type)

    def _product_crate(self):

        last_update = timezone.now().date() - timedelta(0)
        links = ProductLink.objects.filter(updated__lte=last_update).all()

        for link in links:
            if link.food_id is not None:

                try:
                    source = self.get_food_content(link.url)

                    old_price = source.find("p", {"class": "old-price"})
                    new_price = source.find("p", {"class": "new-price"})
                    free_cargo = source.find("span", {"class": "bg-light rounded pd-badge pd-cargofree-badge mb-2"})
                    in_stock = source.find("span", {"class": "bg-light rounded pd-badge pd-stock-badge"})

                    if old_price:
                        old_price = old_price.text.replace('TL', '').replace('.', '').replace(',', '.')

                    if new_price:
                        new_price = new_price.text.replace('TL', '').replace('.', '').replace(',', '.')

                    if free_cargo:
                        if free_cargo.text.strip() == 'Kargo Bedava!':
                            free_cargo = True
                        else:
                            free_cargo = False

                    if in_stock:
                        if in_stock.text.strip() == 'Tükendi':
                            in_stock = False
                        else:
                            in_stock = True

                    title = ''
                    barkod = None
                    size = None

                    specs = source.findAll("div", {"class": "row mb-2"})

                    for spec in specs:
                        for s in spec.children:

                            if isinstance(s, NavigableString):
                                continue
                            if isinstance(s, Tag):
                                if title == 'BARKOD':
                                    barkod = s.text

                                if title == 'AĞIRLIK':
                                    size = s.text.replace(' ', '').replace('gr', 'g').replace(',', '.').strip()

                                title = s.text

                    if size is None:
                        foodsize = FoodSize.objects.get(id=1)
                    else:
                        foodsize = FoodSize.objects.filter(name=size).first()

                    if foodsize is None:
                        foodsize = FoodSize(name=size)
                        foodsize.save()

                    FoodPromotion.objects.filter(food_id=link.food_id).delete()
                    promotions = source.findAll("div", {"class": "p-1 bd-highlight"})

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
                            size=foodsize,
                            code=barkod
                        )

                        new_site.save()

                        for promotion in promotions:
                            if promotion.a:
                                gift = FoodPromotion(
                                    site=new_site,
                                    name=promotion.find('a').contents[0].strip(),
                                    food=link.food,
                                )

                                gift.save()
                    else:

                        foodsite.old_price = old_price
                        foodsite.price = new_price
                        foodsite.stock = in_stock
                        foodsite.cargo = free_cargo

                        foodsite.save()

                        for promotion in promotions:
                            if promotion.a:
                                gift = FoodPromotion(
                                    site=foodsite,
                                    name=promotion.find('a').contents[0].strip(),
                                    food=link.food,
                                )

                                gift.save()

                    ProductLink.objects.update(down=0)
                except ObjectDoesNotExist as e:
                    ProductLink.objects.update(down=1)

    def handle(self, *args, **options):
        crawl_type = options.get('type', None)

        if crawl_type is not None:
            if crawl_type == 'product':
                self._product_crate()
            else:
                self._data_crate()
        else:
            print('Seçim yapmadın')
