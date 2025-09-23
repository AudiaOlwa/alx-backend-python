from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # 20 messages par page
    page_size_query_param = "page_size"  # permet d’overrider si besoin
    max_page_size = 100
