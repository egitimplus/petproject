from library.mixins import RequestMixin
from library.feeds import TicimaxRepository


class ShopCrawlerRepository(RequestMixin):

    def __init__(self, **kwargs):
        self.__object = kwargs.pop("shop", None)

        if self.__object is not None:
            self.create_repository()

    def create_repository(self):
        if self.__object.type == 1:
            self.__shop = TicimaxRepository(parent=self)
        else:
            self.__shop = TicimaxRepository(parent=self)

