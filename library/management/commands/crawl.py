from django.core.management.base import BaseCommand
from library.feeds.crawlers import ShopCrawlerRepository
from company.models import PetShop, Site
from library.models import ProductLink


class Command(BaseCommand):
    def shop(self):
        url = Site.objects.get(id=12)

        crawler = ShopCrawlerRepository()
        crawler.petshop = url.company
        crawler.url = url.company.url + url.url

        shop = crawler.shop()
        shop.run()

    def product(self):
        shop = PetShop.objects.get(id=12)
        product = ProductLink.objects.filter(petshop=shop).first()

        crawler = ShopCrawlerRepository()

        crawler.petshop = shop
        crawler.link = product
        crawler.url = product.url

        shop = crawler.product()
        shop.run()

    def comments(self):
        shop = PetShop.objects.get(id=12)
        product = ProductLink.objects.filter(petshop=shop).first()

        crawler = ShopCrawlerRepository()

        crawler.petshop = shop
        crawler.link = product
        crawler.url = product.url

        shop = crawler.comments()
        shop.run()

    def handle(self, *args, **options):
        self.shop()
