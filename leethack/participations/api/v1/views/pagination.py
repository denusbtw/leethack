from rest_framework.pagination import PageNumberPagination


class HackathonParticipantPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 200


class HackathonParticipationRequestPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 200
