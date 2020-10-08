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
        encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None

        return BeautifulSoup(r.content, "lxml", from_encoding=encoding)

    def run(self):
        source = self.crawl()
        self.add(source)
        self.pages(source)

    def add(self, source):
        products = source.findAll("li", {"class": "col-xs-12 col-sm-4 col-md-4"})

        if products:
            for product in products:
                pr = product.find("div", {"class": "right-block"})

                url = pr.a.get('href')
                title = pr.a.text

                link, created = ProductLink.objects.get_or_create(
                    url= self.petshop.url + url,
                    defaults={
                        'name': title,
                        'petshop': self.petshop
                    }
                )

                if not created:
                    if link.name != title:
                        FoodSite.objects.filter(url=url).delete()
                        ProductLink.objects.filter(url=url).update(name=title, food_id=None)

    def pages(self, source):
        pagination = source.find("div", {"class": "bottom-pagination"})

        if pagination and pagination.ul:
            links = pagination.ul.find_all('li')

            if links:
                total = links[0].get("onclick").split('Reload("s", "-1", ')

                if len(total) > 1:
                    total = total[1].split(');')
                    total = int(total[0])

                if total > 1:
                    for i in range(2, total+1):
                        self.url = self.parent.url + '?s=' + str(i)
                        source = self.crawl()
                        self.add(source)
