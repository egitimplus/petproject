from .product import ProductCrawler
from .shop import ShopCrawler
from .comment import CommentCrawler


class PetlebiRepository:

    def __init__(self, **kwargs):

        parent = kwargs.get('parent', None)

        self.petshop = parent.petshop
        self.url = parent.url
        self.link = parent.link
        self.prod = None

    def shop(self):
        shop = ShopCrawler(parent=self)
        return shop

    def product(self):
        product = ProductCrawler(parent=self)
        return product

    def comments(self):

        comment = CommentCrawler(parent=self)
        return comment
