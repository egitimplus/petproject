from library.mixins import RequestMixin
from library.feeds.crawlers.ticimax import TicimaxRepository
from library.feeds.crawlers.petlebi import PetlebiRepository
from library.feeds.crawlers.arkadaspet import ArkadasPetRepository
from library.feeds.crawlers.juenpet import JuenPetRepository
from library.feeds.crawlers.kolaymama import KolaymamaRepository
from library.feeds.crawlers.markamama import MarkamamaRepository


class ShopCrawlerRepository(RequestMixin):

    def __init__(self, **kwargs):

        self.crawler = None
        self.__petshop = None
        self.__url = None
        self.__link = None

    def create_repository(self):
        if self.petshop.type == 1:
            self.crawler = TicimaxRepository(parent=self)
        elif self.petshop.type == 2:
            self.crawler = PetlebiRepository(parent=self)
        elif self.petshop.type == 3:
            self.crawler = ArkadasPetRepository(parent=self)
        elif self.petshop.type == 4:
            self.crawler = JuenPetRepository(parent=self)
        elif self.petshop.type == 5:
            self.crawler = MarkamamaRepository(parent=self)
        elif self.petshop.type == 6:
            self.crawler = KolaymamaRepository(parent=self)

    @property
    def link(self):
        return self.__link

    @link.setter
    def link(self, value):
        self.__link = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    @property
    def petshop(self):
        return self.__petshop

    @petshop.setter
    def petshop(self, value):
        self.__petshop = value

    def shop(self):
        self.create_repository()
        shop = self.crawler.shop()
        return shop

    def product(self):
        self.create_repository()
        product = self.crawler.product()
        return product

    def comments(self):
        self.create_repository()
        comments = self.crawler.comments()
        return comments
