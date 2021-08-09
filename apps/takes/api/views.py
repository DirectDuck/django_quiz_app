from django.core.exceptions import FieldError
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.api.pagination import CustomPageNumberPagination
from apps.quizzes import models as quizzes_models
from apps.takes import models
from . import serializers, verificators, utils


class ExploreApiView(APIView, CustomPageNumberPagination):
    def get(self, request):
        quizzes = quizzes_models.Quiz.objects.filter(
            status=quizzes_models.Quiz.Status.APPROVED
        ).annotate(completions=Count("completed_quizzes"))

        # Sorting
        if "sort_by" in request.GET:
            sort_by = request.GET.get("sort_by")
            try:
                quizzes = quizzes.order_by(sort_by)
            except FieldError:
                raise ValidationError("Sorting by this field is not allowed")
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
            quizzes_models.Quiz.objects.filter(
                status=quizzes_models.Quiz.Status.APPROVED
            ),
            slug=slug,
        )

        serializer = serializers.QuizTakeSerializer(quiz)

        return Response(serializer.data)

    def post(self, request, slug):
        quiz = get_object_or_404(
            quizzes_models.Quiz.objects.filter(
                status=quizzes_models.Quiz.Status.APPROVED
            ),
            slug=slug,
        )

        # Verifiying that answers are present in request.data
        verificators.validate_quiz_take_post_data(request.data, quiz)

        # Removing previous results for current user/quiz pair
        models.CompletedQuiz.remove_previous(request.user, quiz)

        # Creating empty basically CompletedQuiz
        completed_quiz = models.CompletedQuiz.objects.create(
            user=request.user, quiz=quiz, score=0
        )

        # Initializing CompletedQuizAnswers ...
        completed_quiz_answers = utils.initialize_completed_quiz_answers(
            request.data["answers"],
            quiz,
            completed_quiz,
        )

        # ... and creating them
        models.CompletedQuizAnswer.objects.bulk_create(completed_quiz_answers)

        # Updating CompletedQuiz score based on created CompletedQuizAnswer objects
        completed_quiz.update_score()

        # Generating response
        response = {
            "score": completed_quiz.score,
            "message": completed_quiz.get_result_message(),
        }

        return Response(response)
