from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class PollItemAnswerFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Validating number of answers
        if len(self.forms) < 2:
            raise ValidationError("Minimum of 2 answers is required")

        if len(self.forms) > 6:
            raise ValidationError("Maximum of 6 answers is allowed")

        # Validating number of correct answers
        corrects = 0
        for form in self.forms:
            if form.cleaned_data["correct"]:
                corrects += 1

        if corrects > 1:
            raise ValidationError("Item can have only one correct answer")

        if corrects == 0:
            raise ValidationError("Item must have an correct answer")
