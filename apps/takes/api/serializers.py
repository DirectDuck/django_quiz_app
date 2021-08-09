from rest_framework import serializers

from apps.quizzes import models


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
        model = models.Quiz
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
        model = models.QuizItemAnswer
        fields = [
            "pk",
            "text",
        ]


class QuizItemSerializer(serializers.ModelSerializer):

    answers = QuizItemAnswerSerializer(many=True)

    class Meta:
        model = models.QuizItem
        fields = ["index", "question", "answers"]


class QuizTakeSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()

    number_of_questions = serializers.SerializerMethodField(
        method_name="get_number_of_questions"
    )

    items = QuizItemSerializer(many=True)

    class Meta:
        model = models.Quiz
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


class QuizTakeItemSerializer(serializers.Serializer):
    item_index = serializers.IntegerField()
    answer_pk = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        self.quiz = kwargs.pop("quiz")
        super().__init__(*args, **kwargs)
