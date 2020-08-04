from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from library.models import ProductLinks


class Command(BaseCommand):

    def get_content(self, brand, food_type, page=None):

        url = 'https://www.petlebi.com/' + brand + '/' + food_type

        if page is not None:
            url = url + '?page=' + page

        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def add_products(self, source, brand, food_type):
        products = source.findAll("div", {"class": "card-body pb-0"})

        if products:
            for product in products:
                url = product.a.get('href')
                name = product.find("h3", {"class": "commerce-title mt-2 mb-0"})

                obj, created = ProductLinks.objects.get_or_create(brand=brand, url=url, name=name.text, food_type=food_type)
        else:
            ProductLinks.objects.filter(brand=brand, food_type=food_type).update(down=1)
            print(brand)

    def add_childs(self, source, brand, food_type):
        pagination = source.find(id="pagination_area")

        if pagination and pagination.ul:
            links = pagination.ul.find_all('li')

            if links:
                total = len(links)

                for i in range(1, total - 1):
                    split = links[i].a.get('href').split('?page=')
                    source = self.get_content(brand, food_type, split[1])
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
                source = self.get_content(brand, food_type)
                self.add_products(source, brand, food_type)
                self.add_childs(source, brand, food_type)

    def handle(self, *args, **options):
        self._data_crate()
