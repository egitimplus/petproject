import requests
from bs4 import BeautifulSoup
from library.models import ProductLink


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
        products = source.findAll("div", {"class": "showcaseTitle"})

        if products:
            for product in products:
                url = product.a.get('href')
                title = product.a.get('title')

                link, created = ProductLink.objects.get_or_create(
                    url=self.petshop.url + url,
                    defaults={
                        'name': title,
                        'petshop': self.petshop
                    }
                )

    def pages(self, source):
        pagination = source.find("div", {"class": "_paginateContent"})

        if pagination and pagination.ul:
            links = pagination.ul.find_all('li')
            if links:
                total = len(links)

                for i in range(2, total+1):
                    url = links[i-1].a.get('href').split('?tp=')
                    self.url = self.parent.url + '?tp=' + url[1]

                    source = self.crawl()
                    self.add(source)


