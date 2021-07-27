from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from . import models


# I intentionally merged Create and Edit forms
# for Quiz and QuizItem, because they are basically
# the same. However, when they will begin to differ
# in the slightest - I'll separate them


class QuizForm(forms.ModelForm):
    title = forms.CharField(min_length=3, max_length=65)
    description = forms.CharField(min_length=3, max_length=255, widget=forms.Textarea)

    class Meta:
        model = models.Quiz
        fields = ("title", "description")


class QuizDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        fields = tuple()


class QuizItemForm(forms.ModelForm):
    question = forms.CharField(min_length=3, max_length=65)

    class Meta:
        model = models.QuizItem
        fields = ("question",)

    def __init__(self, *args, **kwargs):

        if "quiz" in kwargs:
            self.quiz = kwargs.pop("quiz")
        else:
            raise Exception("No quiz passed")

        super().__init__(*args, **kwargs)

    def clean_question(self):
        question = self.cleaned_data["question"]

        # Making sure that each quiz question is unique
        if self.quiz.items.filter(question=question).exists():
            raise ValidationError("Item with that question already exists")

        return question


class QuizItemDeleteForm(forms.ModelForm):
    class Meta:
        model = models.QuizItem
        fields = tuple()


class QuizItemAnswerFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Making sure not to account forms that are
        # about to be deleted
        forms = []

        for form in self.forms:
            if "DELETE" in form.cleaned_data and form.cleaned_data["DELETE"]:
                continue

            forms.append(form)

        # Validating number of answers
        if len(forms) < models.QuizItem.MIN_ANSWERS:
            raise ValidationError("Minimum of 2 answers is required")

        if len(forms) > models.QuizItem.MAX_ANSWERS:
            raise ValidationError("Maximum of 6 answers is allowed")

        # Validating number of correct answers
        corrects = 0
        for form in forms:
            if form.cleaned_data["correct"]:
                corrects += 1

        if corrects > models.QuizItem.MAX_CORRECT_ANSWERS:
            raise ValidationError(
                f"You must have a maximum of {models.QuizItem.MAX_CORRECT_ANSWERS}"
                " correct answers"
            )

        if corrects < models.QuizItem.MIN_CORRECT_ANSWERS:
            raise ValidationError(
                f"You must have a minimum of {models.QuizItem.MIN_CORRECT_ANSWERS}"
                " correct answers"
            )

        # Validating that every answer is unique
        answers = []
        for form in forms:
            if form.cleaned_data["text"] in answers:
                raise ValidationError("Every answer must be unique")
            else:
                answers.append(form.cleaned_data["text"])
