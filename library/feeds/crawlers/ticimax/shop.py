import requests
from bs4 import BeautifulSoup
from library.models import ProductLink
import json


class TicimaxShopCrawler:

    def __init__(self, **kwargs):
        self.petshop = kwargs.get('petshop', None)
        self.categories = kwargs.get('categories', None)

    def crawl(self, url):
        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def run(self, page=1):
        categories = '%2C'.join(self.categories)
        page_url = self.petshop.url +'/api/product/GetProductList?FilterJson=%7B%22CategoryIdList%22%3A%5B' + categories + '%5D%2C%22BrandIdList%22%3A%5B%5D%2C%22SupplierIdList%22%3A%5B%5D%2C%22TagIdList%22%3A%5B%5D%2C%22TagId%22%3A-1%2C%22FilterObject%22%3A%5B%5D%2C%22MinStockAmount%22%3A-1%2C%22IsShowcaseProduct%22%3A-1%2C%22IsOpportunityProduct%22%3A-1%2C%22IsNewProduct%22%3A-1%2C%22IsDiscountedProduct%22%3A-1%2C%22IsShippingFree%22%3A-1%2C%22IsProductCombine%22%3A-1%2C%22MinPrice%22%3A0%2C%22MaxPrice%22%3A0%2C%22SearchKeyword%22%3A%22%22%2C%22StrProductIds%22%3A%22%22%2C%22IsSimilarProduct%22%3Afalse%2C%22RelatedProductId%22%3A0%2C%22ProductKeyword%22%3A%22%22%2C%22PageContentId%22%3A0%2C%22StrProductIDNotEqual%22%3A%22%22%2C%22IsVariantList%22%3A-1%2C%22IsVideoProduct%22%3A-1%2C%22ShowBlokVideo%22%3A-1%2C%22VideoSetting%22%3A%7B%22ShowProductVideo%22%3A-1%2C%22AutoPlayVideo%22%3A-1%7D%2C%22ShowList%22%3A1%2C%22VisibleImageCount%22%3A6%2C%22ShowCounterProduct%22%3A-1%7D&PagingJson=%7B%22PageItemCount%22%3A0%2C%22PageNumber%22%3A' + str(page) + '%2C%22OrderBy%22%3A%22KATEGORISIRA%22%2C%22OrderDirection%22%3A%22ASC%22%7D&CreateFilter=true'
        source = self.crawl(page_url)
        content = json.loads(source.text)

        totalProductCount = content.get('totalProductCount')
        nextProductCount = content.get('nextProductCount')
        currentPage = content.get('currentPage')

        if totalProductCount > 0:
            self.add(content)

            if nextProductCount > 0:
                self.run(currentPage+1)

    def add(self, content):

        for product in content['products']:

            url = product.get('defaultUrl')
            brand = product.get('brand')
            name = product.get('name')

            ProductLink.objects.get_or_create(
                url=self.petshop.url + url,
                defaults={
                    'brand': brand,
                    'name': name,
                    'petshop': self.petshop,
                    'comment_crawl': 1,
                    'product_crawl': 0
                }
            )
