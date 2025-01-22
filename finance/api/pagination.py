from rest_framework.pagination import PageNumberPagination


class RevenuePagination(PageNumberPagination):
    """Кастомная пагинация для модели Revenue.

    - page_size: Количество элементов на странице по умолчанию.
    - page_size_query_param: Параметр для изменения количества элементов на странице.
    - max_page_size: Максимальное количество элементов на странице.
    """

    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 20
