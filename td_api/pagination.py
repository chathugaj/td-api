from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10