from apps.quizzes import models as quizzes_models


def is_quiz_suitable_for_submission(quiz):
    quiz_items_count = quiz.items.count()

    if quiz_items_count < 3:
        return (False, "You need to have at least 3 questions to submit quiz.")

    if quiz_items_count > 15:
        return (False, "You need to have at most 15 questions to submit quiz.")

    quiz_results = quiz.results.all()

    if quiz_results.count() < quiz_items_count:
        return (False, "You need to fill the results to submit quiz.")

    if quiz_results.filter(text=""):
        return (False, "You need to fill the results to submit quiz.")

    if quiz.status not in (quiz.Status.DRAFT, quiz.Status.REJECTED):
        return (False, "This quiz does not need submission.")

    return (True, "Your quiz is now submitted.")


def is_quiz_suitable_for_review_cancel(quiz):
    if quiz.status != quiz.Status.REVIEW:
        return (False, "This quiz is not on review.")

    return (True, "Your quiz is now canceled from review.")
