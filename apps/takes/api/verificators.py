from rest_framework.exceptions import ValidationError


def validate_quiz_take_post_data(data, quiz):
    """Check if quiz take POST data contains answers and they have
    exact number of answers required for quiz"""

    if "answers" not in data:
        raise ValidationError("No answers provided")

    if type(data["answers"]) != list:
        raise ValidationError("Answers are not an array")

    if len(data["answers"]) != quiz.items.count():
        raise ValidationError("Invalid number of answers")
