from rest_framework.views import APIView
from rest_framework.response import Response

from apps.quizzes import models
from . import serializers


class ExploreApiView(APIView):
    def get(self, request):
        quizzes = models.Quiz.objects.filter(status=models.Quiz.Status.APPROVED)
        serializer = serializers.QuizSerializer(
            quizzes, many=True, context={"request": request}
        )
        return Response(serializer.data)
