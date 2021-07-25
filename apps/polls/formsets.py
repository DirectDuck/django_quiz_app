from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import PollItem


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
        if len(forms) < PollItem.MIN_ANSWERS:
            raise ValidationError("Minimum of 2 answers is required")

        if len(forms) > PollItem.MAX_ANSWERS:
            raise ValidationError("Maximum of 6 answers is allowed")

        # Validating number of correct answers
        corrects = 0
        for form in forms:
            if form.cleaned_data["correct"]:
                corrects += 1

        if corrects > PollItem.MAX_CORRECT_ANSWERS:
            raise ValidationError(
                f"You must have a maximum of {PollItem.MAX_CORRECT_ANSWERS}"
                " correct answers"
            )

        if corrects < PollItem.MIN_CORRECT_ANSWERS:
            raise ValidationError(
                f"You must have a minimum of {PollItem.MIN_CORRECT_ANSWERS}"
                " correct answers"
            )
