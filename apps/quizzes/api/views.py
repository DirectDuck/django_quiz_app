from rest_framework.views import APIView
from rest_framework.response import Response

from apps.quizzes import models
from . import serializers


class QuizApiView(APIView):
    def get(self, request):
        quizzes = models.Quiz.objects.filter(status=models.Quiz.Status.APPROVED)
        serializer = serializers.QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
