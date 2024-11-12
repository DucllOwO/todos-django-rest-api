
from rest_framework.pagination import PageNumberPagination


class TodoPagination(PageNumberPagination):
    page_size = 10  # Items per page
    page_size_query_param = 'page_size'  # Allow clients to set page size

    max_page_size = 100  # Maximum items per page
