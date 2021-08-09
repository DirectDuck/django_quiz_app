from rest_framework.exceptions import ValidationError

from apps.takes import models


def initialize_completed_quiz_answers(answers, quiz, completed_quiz):
    """Initialize CompletedQuizAnswer for bulk_create from answers pks.

    May raise ValidationError since bulk_create won't call save method,
    and UniqueConstraints are not enough to validate incoming data"""

    completed_quiz_answers = []

    for answer_pk in answers:
        if answer_pk in [
            completed_quiz_answer.item_answer.pk
            for completed_quiz_answer in completed_quiz_answers
        ]:
            raise ValidationError("Can't have two of the same answers")

        try:
            quiz_answer = models.CompletedQuizAnswer.initialize_from_answer_pk(
                completed_quiz,
                answer_pk,
            )
        except Exception as e:
            raise ValidationError(e)

        if quiz_answer.item_answer.quiz_item.pk in [
            completed_quiz_answer.item_answer.quiz_item.pk
            for completed_quiz_answer in completed_quiz_answers
        ]:
            raise ValidationError("Can't have two answers on same question")

        if quiz_answer.item_answer.quiz_item.quiz.pk != quiz.pk:
            raise ValidationError("Can't set answer from different quiz")

        completed_quiz_answers.append(quiz_answer)

    return completed_quiz_answers
