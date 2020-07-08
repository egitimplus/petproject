from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 12


class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):

        limit = int(self.request.GET.get('limit', self.page_size))
        page = int(self.request.GET.get('page', DEFAULT_PAGE))
        start = (page - 1) * limit + 1
        total = self.page.paginator.count
        end = max(min(page * limit, total), start)

        return Response({
            'pages': math.ceil(total/limit),
            'total': total,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)), # can not set default = self.page
            'limit': limit,
            'from': start,
            'to': end,
            'items': data['items'],
            'filters': data['filters'],
        })
