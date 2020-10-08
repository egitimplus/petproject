import requests
from bs4 import BeautifulSoup
from library.models import ProductLink
import json
from food.models import FoodSite


class ShopCrawler:

    def __init__(self, **kwargs):
        self.parent = kwargs.get('parent', None)
        self.url = self.parent.url
        self.petshop = self.parent.petshop

    def crawl(self):
        r = requests.get(self.url)
        return BeautifulSoup(r.content, "lxml")

    def run(self):
        self.url = self.parent.url + 'PageNumber%22%3A1%7D'
        source = self.crawl()
        content = json.loads(source.text)

        totalProductCount = content.get('totalProductCount')
        nextProductCount = content.get('nextProductCount')
        currentPage = content.get('currentPage')

        if totalProductCount > 0:
            self.add(content)

            if nextProductCount > 0:
                page = currentPage+1
                p = 'PageNumber%22%3A' + str(page) + '%7D'
                self.url = self.parent.url + p
                self.run()

    def add(self, content):

        for product in content['products']:

            url = product.get('defaultUrl')
            brand = product.get('brand')
            name = product.get('name')
            id = product.get('productId')

            link, created = ProductLink.objects.get_or_create(
                url=self.petshop.url + url,
                defaults={
                    'brand': brand,
                    'name': name,
                    'petshop': self.petshop,
                    'product_id': id
                }
            )

            if not created:
                if link.name != name:
                    FoodSite.objects.filter(url=url).delete()
                    ProductLink.objects.filter(url=url).update(brand=brand, name=name, food_id=None)

            self.parent.link = link
            self.parent.prod = product

            pr = self.parent.product()
            pr.run()
