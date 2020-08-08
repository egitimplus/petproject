from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from library.models import ProductLink
from django.utils import timezone
from datetime import timedelta
from food.models import FoodSite, FoodComment, FoodPromotion, FoodSize
from django.db.models import Max
from datetime import datetime


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Define a username prefix', )
        parser.add_argument('-f', '--food', type=str, help='Define a food prefix', )

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

        ft = 'wet'
        if food_type == 'kedi-mamasi':
            ft = 'dry'

        if products:
            for product in products:
                url = product.a.get('href')
                name = product.find("h3", {"class": "commerce-title mt-2 mb-0"})

                obj, created = ProductLink.objects.get_or_create(
                    brand=brand,
                    url=url,
                    name=name.text,
                    food_type=ft,
                    petshop_id=1
                )
        else:
            ProductLink.objects.filter(brand=brand, food_type=ft).update(down=1)

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

    def _data_crate(self, food_type):

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

        if food_type == 'kedi-konserve-mamasi':
            brands = wet_brands

        for brand in brands:
            source = self.get_brand_content(brand, food_type)
            self.add_products(source, brand, food_type)
            self.add_childs(source, brand, food_type)

    def _add_comments(self, source, food):
        source = source.prettify()

        source = source.split('"review": [')
        source = source[1].split(']')

        reviews = source[0].split('},              {')

        comment = FoodComment.objects.filter(food_id=food.id, petshop_id=1).aggregate(max_date=Max('created'))

        for review in reviews:
            author = review.split('"author": "')
            author = author[1].split('"')

            description = review.split('"description": "')
            description = description[1].split('"')

            rating = review.split('"ratingValue": "')
            rating = rating[1].split('"')

            published = review.split('"datePublished": "')
            published = published[1].split('"')
            published = datetime.strptime(published[0], '%Y-%m-%d')
            published = timezone.make_aware(published, timezone.get_current_timezone())

            save = 0

            if comment['max_date'] is None:
                save = 1
            elif published > comment['max_date']:
                save = 1

            if save == 1:
                fc = FoodComment(
                    food=food,
                    name=author[0],
                    created=published,
                    content=description[0],
                    rating=rating[0],
                    petshop_id=1,
                )
                fc.save()

    def _product_crate(self):

        last_update = timezone.now().date() - timedelta(0)
        links = ProductLink.objects.filter(updated__lte=last_update, petshop_id=2, down=0, active=1, food__isnull=False).all()

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

                                if title == 'AĞIRLIK':
                                    size = s.text.replace(' ', '').replace('gr', 'g').replace(',', '.').strip()

                                title = s.text

                    foodsize = None

                    if size is not None:
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
                            updated=timezone.now(),
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
                        foodsite.updated = timezone.now()
                        foodsite.save()

                        for promotion in promotions:
                            if promotion.a:
                                gift = FoodPromotion(
                                    site=foodsite,
                                    name=promotion.find('a').contents[0].strip(),
                                    food=link.food,
                                )

                                gift.save()

                    ProductLink.objects.filter(id=link.id).update(down=0, updated=timezone.now())
                    self._add_comments(source, link.food)
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
        kedi-mamasi
        kedi-konserve-mamasi
    
        --type
        product
        page
        """
