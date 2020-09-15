from django.core.management.base import BaseCommand
from library.feeds.crawlers import ShopCrawlerRepository
from company.models import PetShop
from library.models import ProductLink


class Command(BaseCommand):

    def tiximax_comments(self):

        shop = PetShop.objects.get(id=8)
        crawler = ShopCrawlerRepository(petshop=shop)
        crawler.link = ProductLink.objects.first()
        crawler.url = shop.url +'/api/product/GetComments?productId=' + str(crawler.link.product_id)

        comments = crawler.comments()
        comments.run()

    def ticimax_shop_product(self):
        shop = PetShop.objects.get(id=8)

        crawler = ShopCrawlerRepository(petshop=shop)
        page = 1
        crawler.url = shop.url + '/api/product/GetProductList?FilterJson=%7B%22CategoryIdList%22%3A%5B' + shop.categories + '%5D%2C%22BrandIdList%22%3A%5B%5D%2C%22SupplierIdList%22%3A%5B%5D%2C%22TagIdList%22%3A%5B%5D%2C%22TagId%22%3A-1%2C%22FilterObject%22%3A%5B%5D%2C%22MinStockAmount%22%3A-1%2C%22IsShowcaseProduct%22%3A-1%2C%22IsOpportunityProduct%22%3A-1%2C%22IsNewProduct%22%3A-1%2C%22IsDiscountedProduct%22%3A-1%2C%22IsShippingFree%22%3A-1%2C%22IsProductCombine%22%3A-1%2C%22MinPrice%22%3A0%2C%22MaxPrice%22%3A0%2C%22SearchKeyword%22%3A%22%22%2C%22StrProductIds%22%3A%22%22%2C%22IsSimilarProduct%22%3Afalse%2C%22RelatedProductId%22%3A0%2C%22ProductKeyword%22%3A%22%22%2C%22PageContentId%22%3A0%2C%22StrProductIDNotEqual%22%3A%22%22%2C%22IsVariantList%22%3A-1%2C%22IsVideoProduct%22%3A-1%2C%22ShowBlokVideo%22%3A-1%2C%22VideoSetting%22%3A%7B%22ShowProductVideo%22%3A-1%2C%22AutoPlayVideo%22%3A-1%7D%2C%22ShowList%22%3A1%2C%22VisibleImageCount%22%3A6%2C%22ShowCounterProduct%22%3A-1%7D&PagingJson=%7B%22PageItemCount%22%3A0%2C%22PageNumber%22%3A' + str(page) + '%2C%22OrderBy%22%3A%22KATEGORISIRA%22%2C%22OrderDirection%22%3A%22ASC%22%7D&CreateFilter=true'

        shop = crawler.shop()
        shop.run()

        # PETBURADA: 149%2C207
        # PETGROSS: 49%2C71
        # PETZZSHOP: 25%2C26
        # ZOOPET: 54%2C37

    def arkadaspet_shop(self):
        shop = PetShop.objects.get(id=2)

        crawler = ShopCrawlerRepository()
        crawler.petshop = shop
        crawler.url = 'https://www.arkadaspet.com/kategori/kuru-mamalar-1'

        shop = crawler.shop()
        shop.run()

        # https://www.arkadaspet.com/kategori/konserveler-yas-mamalar
        # https://www.arkadaspet.com/kategori/kuru-mamalar-1

    def arkadaspet_product(self):
        product = ProductLink.objects.first()
        shop = PetShop.objects.get(id=2)

        crawler = ShopCrawlerRepository()

        crawler.petshop = shop
        crawler.link = product
        crawler.url = product.url

        shop = crawler.product()
        shop.run()

    def petlebi_shop(self):
        shop = PetShop.objects.get(id=1)

        crawler = ShopCrawlerRepository()
        crawler.petshop = shop
        crawler.url = 'https://www.petlebi.com/kedi-konserve-mamasi'

        shop = crawler.shop()
        shop.run()

        # https://www.petlebi.com/kedi-konserve-mamasi
        # https://www.petlebi.com/kedi-mamasi

    def petlebi_product(self):
        shop = PetShop.objects.get(id=1)
        product = ProductLink.objects.filter(petshop=shop).first()

        crawler = ShopCrawlerRepository()

        crawler.petshop = shop
        crawler.link = product
        crawler.url = product.url

        shop = crawler.product()
        shop.run()

    def petlebi_comments(self):
        shop = PetShop.objects.get(id=1)
        product = ProductLink.objects.filter(petshop=shop).first()

        crawler = ShopCrawlerRepository()

        crawler.petshop = shop
        crawler.link = product
        crawler.url = product.url

        shop = crawler.comments()
        shop.run()

    def juenpet_shop(self):
        shop = PetShop.objects.get(id=5)

        crawler = ShopCrawlerRepository()
        crawler.petshop = shop
        crawler.url = 'https://www.juenpetmarket.com/konserve-kedi-mamasi-k-82'

        shop = crawler.shop()
        shop.run()

        # https://www.juenpetmarket.com/konserve-kedi-mamasi-k-82
        # https://www.juenpetmarket.com/kuru-kedi-mamasi-k-81

    def juenpet_product(self):
        shop = PetShop.objects.get(id=5)
        product = ProductLink.objects.filter(petshop=shop).first()

        crawler = ShopCrawlerRepository()

        crawler.petshop = shop
        crawler.link = product
        crawler.url = product.url

        shop = crawler.product()
        shop.run()

    def kolaymama_shop(self):
        shop = PetShop.objects.get(id=9)

        crawler = ShopCrawlerRepository()
        crawler.petshop = shop
        crawler.url = 'https://www.kolaymama.com/kedi-yas-mamalar'

        shop = crawler.shop()
        shop.run()

        # https://www.kolaymama.com/srv/service/product/loader?kedi-yas-mamalar&link=kedi-yas-mamalar
        # https://www.kolaymama.com/srv/service/product/loader?kedi-kuru-mamalar&link=kedi-kuru-mamalar

    def kolaymama_product(self):
        shop = PetShop.objects.get(id=9)
        product = ProductLink.objects.filter(petshop=shop).first()

        crawler = ShopCrawlerRepository()

        crawler.petshop = shop
        crawler.link = product
        crawler.url = product.url

        shop = crawler.product()
        shop.run()

    def kolaymama_comments(self):
        shop = PetShop.objects.get(id=9)
        product = ProductLink.objects.filter(petshop=shop).first()

        crawler = ShopCrawlerRepository()

        crawler.petshop = shop
        crawler.link = product
        crawler.url = product.url

        shop = crawler.comments()
        shop.run()

    def markamama_shop(self):
        shop = PetShop.objects.get(id=4)

        crawler = ShopCrawlerRepository()
        crawler.petshop = shop
        crawler.url = 'https://www.markamama.com.tr/srv/service/product/loader?kedi-mamasi&link=kedi-mamasi  '

        shop = crawler.shop()
        shop.run()

        # https://www.markamama.com.tr/srv/service/product/loader?kedi-konserve-mamalari&link=kedi-konserve-mamalari
        # https://www.markamama.com.tr/srv/service/product/loader?kedi-mamasi&link=kedi-mamasi


    def markamama_product(self):
        shop = PetShop.objects.get(id=4)
        product = ProductLink.objects.filter(petshop=shop).first()

        crawler = ShopCrawlerRepository()

        crawler.petshop = shop
        crawler.link = product
        crawler.url = product.url

        shop = crawler.product()
        shop.run()

    def markamama_comments(self):
        shop = PetShop.objects.get(id=4)
        product = ProductLink.objects.filter(petshop=shop).first()

        crawler = ShopCrawlerRepository()

        crawler.petshop = shop
        crawler.link = product
        crawler.url = product.url

        shop = crawler.comments()
        shop.run()

    def handle(self, *args, **options):
        self.kolaymama_comments()
