import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from food.models import FoodComment
from django.db.models import Max
from datetime import datetime


class TicimaxCommentCrawler:

    def __init__(self, **kwargs):
        self.url = kwargs.get('url', None)
        self.product_id = kwargs.get('product_id', None)
        self.food = kwargs.get('food', None)
        self.petshop = kwargs.get('petshop', None)

    def content(self, url):

        r = requests.get(url)
        return BeautifulSoup(r.content, "lxml")

    def product_comments(self):

        source = self.content(self.url +'/api/product/GetComments?productId=' + str(self.product_id))

        if source:
            comments = source.text
            comments = comments.replace('{"comments":[{"', '')
            comments = comments.replace('],"isError":false,"errorMessage":null,"errorCode":null,"model":null}', '')
            comments = comments.split('{')

            c = FoodComment.objects.filter(food_id=self.food.id, petshop_id=self.petshop.id).aggregate(max_date=Max('created'))

            for comment in comments:

                content = comment.split('"comment":"')

                if len(content) > 1:
                    content = content[1].split('"}')

                    author = comment.split('"memberName":"')
                    author = author[1].split('",')

                    published = comment.split('"commentDateFormatted":"')
                    published = published[1].split('",')
                    published = published[0].split(' ')
                    published = datetime.strptime(published[0], '%d-%m-%Y')
                    published = timezone.make_aware(published, timezone.get_current_timezone())

                    save = 1 # daha sonra yeni yorumlar gelsin diye sıfır olacak

                    if c['max_date'] is None:
                        save = 1
                    elif published > c['max_date']:
                        save = 1

                    if save == 1:
                        fc = FoodComment(
                            food=self.food,
                            name=author[0],
                            created=published,
                            content=content[0],
                            rating=0,
                            petshop=self.petshop,
                        )
                        fc.save()
