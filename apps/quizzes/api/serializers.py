from rest_framework import serializers

from apps.quizzes import models


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        fields = ["author", "title", "slug", "description", "status"]
