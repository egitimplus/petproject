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
        products = source.findAll("div", {"class": "col col-3 col-md-4 col-sm-6 col-xs-6 btm productItem ease"})

        if products:
            for product in products:

                brand = product.find("a", {"class": "col col-12 productBrand"})
                url = product.a.get('href')
                title = product.img.get('alt')

                link, created = ProductLink.objects.get_or_create(
                    url=self.petshop.url + url,
                    defaults={
                        'brand': brand,
                        'name': title,
                        'petshop': self.petshop
                    }
                )

                if not created:
                    if link.name != title:
                        FoodSite.objects.filter(url=url).delete()
                        ProductLink.objects.filter(url=url).update(brand=brand, name=title, food_id=None)


    def pages(self, source):
        for i in range(2, 1000):
            self.url = self.parent.url + '?pg=' + str(i)
            source = self.crawl()
            products = source.findAll("div", {"class": "col col-3 col-md-4 col-sm-6 col-xs-6 btm productItem ease"})

            if products:
                self.add(source)
            else:
                break
