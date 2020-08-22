import requests
from bs4 import BeautifulSoup
from library.models import ProductLink
from django.utils import timezone
from food.models import FoodSite, FoodComment
import json
from django.db.models import Max
from datetime import datetime
from .product import TicimaxProductCrawler
from .shop import TicimaxShopCrawler
from .comment import TicimaxCommentCrawler


class TicimaxRepository:

    def __init__(self, **kwargs):
        self.petshop = kwargs.get('petshop', None)
        self.url = kwargs.get('url', None)
        self.categories = kwargs.get('categories', None)

    def shop(self):
        shop = TicimaxShopCrawler(parent=self)
        return shop

    def product(self):
        product = TicimaxProductCrawler(parent=self)
        return product

    def comment(self):
        comment = TicimaxCommentCrawler(parent=self)
        return comment
