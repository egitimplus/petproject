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
        products = source.findAll("div", {"class": "box col-3 col-md-4 col-sm-6 col-xs-6 productItem ease"})

        if products:
            for product in products:
                url = product.a.get('href')
                title = product.img.get('title')
                name = title.split(' - ')

                if len(name) > 2:
                    product_name = title.strip()
                    brand_name = name[0]

                elif len(name) < 2:
                    product_name = title
                    brand_name = ''
                else:
                    product_name = name[1].strip()
                    brand_name = name[0]

                link, created = ProductLink.objects.get_or_create(
                    url=self.petshop.url + url,
                    defaults={
                        'brand': brand_name,
                        'name': product_name,
                        'petshop': self.petshop
                    }
                )

    def pages(self, source):
        pagination = source.find("div", {"class": "productPager"})

        if pagination:

            links = pagination.find_all('a')

            if links:
                last = links[-1].get('href').split('pg=')
                last = last[1].split('"')
                total = int(last[0])

                for i in range(1, total):
                    self.url = self.parent.url + '?pg=' + str(i)
                    source = self.crawl()
                    self.add(source)
