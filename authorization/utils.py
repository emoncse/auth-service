from uuid import UUID

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from auth.settings import PAGE_SIZE, MAX_PAGE_SIZE

from rest_framework import serializers


def validate_uuid4(uuid_string):
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        raise serializers.ValidationError("Not a valid uuid")


class StandardResultsSetPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = MAX_PAGE_SIZE

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'paginator': {
                'total_count': self.page.paginator.count,
                'page_size': self.page.paginator.per_page,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
            },
            'results': data
        })
