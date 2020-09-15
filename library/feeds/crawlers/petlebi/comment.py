import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from food.models import FoodComment
from django.db.models import Max
from datetime import datetime


class CommentCrawler:

    def __init__(self, **kwargs):
        parent = kwargs.get('parent', None)
        self.link = parent.link
        self.petshop = parent.petshop
        self.url = parent.url

    def crawl(self):
        r = requests.get(self.url)
        return BeautifulSoup(r.content, "lxml")

    def content(self):

        r = requests.get(self.url)
        return BeautifulSoup(r.content, "lxml")

    def author(self, review):
        author = review.split('"author": "')

        if len(author) > 1:
            author = author[1].split('"')
            return author[0]

        return None

    def description(self, review):
        description = review.split('"description": "')
        description = description[1].split('"')

        return description[0]

    def rating(self, review):
        rating = review.split('"ratingValue": "')
        rating = rating[1].split('"')

        return rating[0]

    def published(self, review):
        published = review.split('"datePublished": "')
        published = published[1].split('"')
        published = datetime.strptime(published[0], '%Y-%m-%d')
        published = timezone.make_aware(published, timezone.get_current_timezone())

        return published

    def run(self):

        product = self.crawl()

        reviews = product.prettify()
        reviews = reviews.split('"review": [')
        reviews = reviews[1].split(']')
        reviews = reviews[0].split('},              {')

        comment = FoodComment.objects.filter(food=self.link.food, petshop=self.petshop).aggregate(max_date=Max('created'))

        for review in reviews:
            author = self.author(review)

            if author:
                published = self.published(review)

                save = 1 # daha sonra yeni yorumlar gelsin diye sıfır olacak

                if comment['max_date'] is None:
                    save = 1

                elif published > comment['max_date']:
                    save = 1

                if save == 1:

                    fc = FoodComment(
                        food=self.link.food,
                        name=author,
                        created=published,
                        content=self.description(review),
                        rating=self.rating(review),
                        petshop=self.petshop,
                    )
                    fc.save()