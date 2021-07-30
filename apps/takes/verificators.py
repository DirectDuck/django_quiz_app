from apps.quizzes import models as quizzes_models


def is_quiz_suitable_for_tryout(quiz):
    quiz_items_count = quiz.items.count()

    if quiz_items_count < 1:
        return (False, "You need to have at least 1 questions to try out quiz.")

    if quiz_items_count > 15:
        return (False, "You need to have at most 15 questions to try out quiz.")

    quiz_results = quiz.results.all()

    if quiz_results.count() < quiz_items_count:
        return (False, "You need to fill the results to try out quiz.")

    if quiz_results.filter(text=""):
        return (False, "You need to fill the results to try out quiz.")

    return (True, "")
