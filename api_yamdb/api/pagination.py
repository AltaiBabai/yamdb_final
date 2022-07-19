from rest_framework.pagination import PageNumberPagination


class ReviewPagination(PageNumberPagination):
    """API's pagination."""

    page_size = 10
