from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from . import models


# I intentionally merged Create and Edit forms
# for Poll and PollItem, because they are basically
# the same. However, when they will begin to differ
# in the slightest - I'll separate them


class PollForm(forms.ModelForm):
    class Meta:
        model = models.Poll
        fields = ("title", "description")


class PollDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Poll
        fields = tuple()


class PollItemForm(forms.ModelForm):
    class Meta:
        model = models.PollItem
        fields = ("question",)


class PollItemDeleteForm(forms.ModelForm):
    class Meta:
        model = models.PollItem
        fields = tuple()


class PollItemAnswerFormSet(BaseInlineFormSet):
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
        if len(forms) < models.PollItem.MIN_ANSWERS:
            raise ValidationError("Minimum of 2 answers is required")

        if len(forms) > models.PollItem.MAX_ANSWERS:
            raise ValidationError("Maximum of 6 answers is allowed")

        # Validating number of correct answers
        corrects = 0
        for form in forms:
            if form.cleaned_data["correct"]:
                corrects += 1

        if corrects > models.PollItem.MAX_CORRECT_ANSWERS:
            raise ValidationError(
                f"You must have a maximum of {models.PollItem.MAX_CORRECT_ANSWERS}"
                " correct answers"
            )

        if corrects < models.PollItem.MIN_CORRECT_ANSWERS:
            raise ValidationError(
                f"You must have a minimum of {models.PollItem.MIN_CORRECT_ANSWERS}"
                " correct answers"
            )
