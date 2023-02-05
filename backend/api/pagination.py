from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Кастомный пагинатор, чтобы применять
    только там, где нужно"""
    page_size = 6
    page_size_query_param = 'limit'
