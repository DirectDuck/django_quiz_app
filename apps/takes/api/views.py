from django.core.exceptions import FieldError
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import get_object_or_404

from apps.api.pagination import CustomPageNumberPagination
from apps.quizzes import models
from . import serializers


class ExploreApiView(APIView, CustomPageNumberPagination):
    def get(self, request):
        quizzes = models.Quiz.objects.filter(
            status=models.Quiz.Status.APPROVED
        ).annotate(completions=Count("completed_quizzes"))

        # Sorting
        if "sort_by" in request.GET:
            sort_by = request.GET.get("sort_by")
            try:
                quizzes = quizzes.order_by(sort_by)
            except FieldError:
                raise NotAcceptable("Sorting by this field is not allowed")
        else:
            quizzes = quizzes.order_by("-completions")

        # Paginating
        quizzes = self.paginate_queryset(quizzes, request, view=self)

        serializer = serializers.QuizExploreSerializer(
            quizzes, many=True, context={"request": request}
        )

        # Adding pagination links
        return self.get_paginated_response(serializer.data)


class QuizTakeApiView(APIView):
    def get(self, request, slug):
        quiz = get_object_or_404(
            models.Quiz.objects.filter(status=models.Quiz.Status.APPROVED), slug=slug
        )

        serializer = serializers.QuizTakeSerializer(quiz)

        return Response(serializer.data)
