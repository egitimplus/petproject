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

    def content(self):

        r = requests.get(self.url)
        return BeautifulSoup(r.content, "lxml")

    def author(self, comment):
        author = comment.split('"memberName":"')
        author = author[1].split('",')

        return author[0]

    def description(self, comment):
        content = comment.split('"comment":"')

        if len(content) > 1:
            content = content[1].split('"}')
            return content[0]

        return None

    def rating(self, comment):
        return 0

    def published(self, comment):
        published = comment.split('"commentDateFormatted":"')
        published = published[1].split('",')
        published = published[0].split(' ')
        published = datetime.strptime(published[0], '%d-%m-%Y')
        published = timezone.make_aware(published, timezone.get_current_timezone())
        return published

    def run(self):

        source = self.content()

        if source:
            comments = source.text
            comments = comments.replace('{"comments":[{"', '')
            comments = comments.replace('],"isError":false,"errorMessage":null,"errorCode":null,"model":null}', '')
            comments = comments.split('{')

            c = FoodComment.objects.filter(food_id=self.link.food.id, petshop_id=self.petshop.id).aggregate(max_date=Max('created'))

            for comment in comments:

                content = self.description(comment)
                if content:

                    published = self.published(comment)

                    save = 1 # daha sonra yeni yorumlar gelsin diye sıfır olacak

                    if c['max_date'] is None:
                        save = 1
                    elif published > c['max_date']:
                        save = 1

                    if save == 1:
                        fc = FoodComment(
                            food=self.link.food,
                            name=self.author(comment),
                            created=published,
                            content=content,
                            rating=self.rating(comment),
                            petshop=self.petshop,
                        )
                        fc.save()
