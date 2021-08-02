from django import template

register = template.Library()


@register.filter(takes_context=True)
def completed_by(quiz, user):
    """Checks if user completed quiz"""

    return quiz.completed_by(user)
