from apps.quizzes import models as quizzes_models


def is_quiz_suitable_for_submission(quiz):
    quiz_items_count = quiz.items.count()

    if quiz_items_count < quiz.MIN_ITEMS_COUNT:
        return (
            False,
            f"You need to have at least {quiz.MIN_ITEMS_COUNT} questions to submit quiz.",
        )

    if quiz_items_count > quiz.MAX_ITEMS_COUNT:
        return (
            False,
            f"You need to have at most {quiz.MAX_ITEMS_COUNT} questions to submit quiz.",
        )

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


def is_quiz_suitable_for_approved_cancel(quiz):
    if quiz.status != quiz.Status.APPROVED:
        return (False, "This quiz is not approved.")

    return (True, "Your quiz is now canceled from approve.")
