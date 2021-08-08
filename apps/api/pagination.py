from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "pagination": {
                    "next": bool(self.get_next_link()),
                    "previous": bool(self.get_previous_link()),
                },
                "quizzes": data,
            }
        )
