from rest_framework.pagination import PageNumberPagination


class StandardResultsPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'page_size'


class SmallResultsPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50
    page_size_query_param = 'page_size'
