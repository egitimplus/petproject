from food.serializers import FoodSerializer
from food.models import Food
from rest_flex_fields import FlexFieldsModelViewSet
from library.pagination import CustomPagination
from rest_framework.response import Response
from django.db.models import Count
from django.db.models import Q


class FoodViewSet(FlexFieldsModelViewSet):
    permit_list_expands = ['image','brand']
    serializer_class = FoodSerializer
    pagination_class = CustomPagination
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Food.objects.filter(active=1).all()

        brands = self.request.query_params.get("brand", None)
        if brands is not None:
            query = Q()
            for brand in brands.split(","):
                q = Q(brand__slug=brand)
                query |= q

            queryset = queryset.filter(query)

        types = self.request.query_params.get("type", None)
        if types is not None:
            query = Q()
            for typ in types.split(","):
                q = Q(type__slug=typ)
                query |= q

            queryset = queryset.filter(query)

        stages = self.request.query_params.get("stage", None)
        if stages is not None:
            query = Q()
            for stage in stages.split(","):
                q = Q(stage__slug=stage)
                query |= q

            queryset = queryset.filter(query)

        total_score = self.request.query_params.get("total_score", None)
        if total_score is not None:
            scores = total_score.split("-")
            if len(scores) == 2:
                queryset = queryset.filter(total_score__gte=scores[0], total_score__lte=scores[1])

        expands = self.request.query_params.get("expand", "")

        for expand in expands.split(","):
            parts = expand.split(".")
            #count = len(parts)

            if parts[0] == 'ingredients':
                if parts[-1] == 'quality':
                    queryset = queryset.prefetch_related('ingredients__quality')

                if parts[-1] == 'ingredients':
                    queryset = queryset.prefetch_related('ingredients')

            if parts[0] == 'brand':
                if parts[-1] == 'brand':
                    queryset = queryset.select_related('brand')

            if parts[0] == 'image':
                if parts[-1] == 'image':
                    queryset = queryset.prefetch_related('image')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        disable_pagination = self.request.query_params.get("p", False)

        if disable_pagination:
            limit = self.request.query_params.get("limit", False)
            if limit:
                queryset = queryset[:int(limit)]
        else:

            category = queryset.values('type__name', 'type__slug').order_by('type').annotate(count=Count('type'))
            brand = queryset.values('brand__name', 'brand__slug').order_by('brand').annotate(count=Count('brand'))
            health = queryset.values('health__name', 'health__slug').order_by('health').annotate(count=Count('health'))
            stage = queryset.values('stage__name', 'stage__slug').order_by('stage').annotate(count=Count('stage'))

            filters = list()

            if brand:
                brands = {'name': 'Marka', 'slug': 'brand', 'type': 'check', 'value': [], 'items': []}
                for b in brand:
                    brands['items'].append({
                        'slug': b['brand__slug'],
                        'name': b['brand__name'],
                        'count': b['count']
                    })
                filters.append(brands)

            if category:
                categories = {'name': 'Kategori', 'slug': 'type', 'type': 'check', 'value': [], 'items': []}
                for c in category:
                    categories['items'].append({
                        'slug': c['type__slug'],
                        'name': c['type__name'],
                        'count': c['count']
                    })
                filters.append(categories)

            if len(stage) > 1:
                stages = {'name': 'Yaş', 'slug': 'stage', 'type': 'check', 'value': [], 'items': []}
                for s in stage:
                    if s['count']:
                        stages['items'].append({
                            'slug': s['stage__slug'],
                            'name': s['stage__name'],
                            'count': s['count']
                        })
                filters.append(stages)

            if len(health) > 1:
                healths = {'name': 'Sağlık', 'slug': 'health', 'type': 'check', 'value': [], 'items': []}
                for h in health:
                    if h['count']:
                        healths['items'].append({
                            'slug': h['health__slug'],
                            'name': h['health__name'],
                            'count': h['count']
                        })
                filters.append(healths)

            page = self.paginate_queryset(queryset)
            if page is not None:

                serializer = self.get_serializer(page, many=True)

                data = {
                    'filters': filters,
                    'items': serializer.data,
                }

                return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

