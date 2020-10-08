import requests
from bs4 import BeautifulSoup
from library.models import ProductLink
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
        source = self.crawl()
        self.add(source)
        self.pages(source)

    def add(self, source):
        products = source.findAll("div", {"class": "card-body pb-0"})

        if products:
            for product in products:
                url = product.a.get('href')
                name = product.find("h3", {"class": "commerce-title mt-2 mb-0"})

                link, created = ProductLink.objects.get_or_create(
                    url=url,
                    defaults={
                        'name': name.text,
                        'petshop': self.petshop
                    }
                )

                if not created:
                    if link.name != name.text:
                        FoodSite.objects.filter(url=url).delete()
                        ProductLink.objects.filter(url=url).update(name=name.text, food_id=None)

    def pages(self, source):
        pagination = source.find(id="pagination_area")

        if pagination and pagination.ul:
            links = pagination.ul.find_all('li')

            if links:
                total = len(links)

                for i in range(2, total - 1):
                    self.url = self.parent.url + '?page=' + str(i)
                    source = self.crawl()
                    self.add(source)
