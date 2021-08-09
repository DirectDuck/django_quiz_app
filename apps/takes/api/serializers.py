from rest_framework import serializers

from apps.quizzes import models as quizzes_models
from apps.takes import models


class QuizExploreSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()
    number_of_questions = serializers.SerializerMethodField(
        method_name="get_number_of_questions"
    )
    number_of_completions = serializers.SerializerMethodField(
        method_name="get_number_of_completions"
    )
    is_completed = serializers.SerializerMethodField(method_name="get_is_completed")

    class Meta:
        model = quizzes_models.Quiz
        fields = [
            "author",
            "title",
            "slug",
            "description",
            "number_of_questions",
            "number_of_completions",
            "is_completed",
        ]

    def get_number_of_questions(self, obj):
        return obj.items.count()

    def get_number_of_completions(self, obj):
        return obj.completed_quizzes.count()

    def get_is_completed(self, obj):
        request = self.context.get("request")
        if not request:
            raise Exception("Request object wasn't passed to serializers context")
        return obj.is_completed_by(request.user)


class QuizItemAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = quizzes_models.QuizItemAnswer
        fields = [
            "pk",
            "text",
        ]


class QuizItemSerializer(serializers.ModelSerializer):

    answers = QuizItemAnswerSerializer(many=True)

    class Meta:
        model = quizzes_models.QuizItem
        fields = ["index", "question", "answers"]


class QuizTakeSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()

    number_of_questions = serializers.SerializerMethodField(
        method_name="get_number_of_questions"
    )

    items = QuizItemSerializer(many=True)

    class Meta:
        model = quizzes_models.Quiz
        fields = [
            "author",
            "title",
            "slug",
            "description",
            "number_of_questions",
            "items",
        ]

    def get_number_of_questions(self, obj):
        return obj.items.count()


class QuizShortSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()

    number_of_questions = serializers.SerializerMethodField(
        method_name="get_number_of_questions"
    )

    class Meta:
        model = quizzes_models.Quiz
        fields = [
            "author",
            "title",
            "slug",
            "description",
            "number_of_questions",
        ]

    def get_number_of_questions(self, obj):
        return obj.items.count()


class CompletedQuizSerializer(serializers.ModelSerializer):

    quiz = QuizShortSerializer()
    result_message = serializers.SerializerMethodField(method_name="get_result_message")

    class Meta:
        model = models.CompletedQuiz
        fields = [
            "quiz",
            "score",
            "result_message",
        ]

    def get_result_message(self, obj):
        return obj.get_result_message()
