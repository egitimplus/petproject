import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from food.models import FoodComment
from django.db.models import Max
from datetime import datetime
import json


class CommentCrawler:

    def __init__(self, **kwargs):
        parent = kwargs.get('parent', None)
        self.link = parent.link
        self.petshop = parent.petshop
        self.url = parent.url

    def crawl(self):
        r = requests.get(self.url)
        return BeautifulSoup(r.content, "lxml")

    def comment_crawl(self, source):
        comments_li = source.find(id="commentTab")
        comments_li = comments_li['data-href'].split('comment/')

        comment_url = self.petshop.url + 'srv/service/product-detail/comments/' + comments_li[1]

        r = requests.get(comment_url)
        return BeautifulSoup(r.content, "lxml")

    def author(self, comment):
        return comment['NAME']

    def description(self, comment):
        return comment['COMMENT']

    def rating(self, comment):
        return round(comment['RATE'] / 4)

    def published(self, comment):
        published = datetime.fromtimestamp(int(comment['DATE']))
        published = timezone.make_aware(published, timezone.get_current_timezone())

        return published

    def run(self):
        source = self.crawl()
        comment_data = self.comment_crawl(source)
        comment_json = json.loads(comment_data.text)

        comments = comment_json.get('COMMENTS')

        if comments:
            c = FoodComment.objects.filter(food=self.link.food, petshop=self.petshop).aggregate(max_date=Max('created'))

            for comment in comments:
                published = self.published(comment)

                save = 1  # daha sonra yeni yorumlar gelsin diye sıfır olacak

                if c['max_date'] is None:
                    save = 1
                elif published > c['max_date']:
                    save = 1

                if save == 1:
                    fc = FoodComment(
                        food=self.link.food,
                        name=self.author(comment),
                        created=published,
                        content=self.description(comment),
                        rating=self.rating(comment),
                        petshop=self.petshop,
                    )
                    fc.save()
