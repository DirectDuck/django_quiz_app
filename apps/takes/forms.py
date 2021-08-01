from django import forms


class QuizItemForm(forms.Form):

    answers = forms.ChoiceField(widget=forms.RadioSelect(attrs={"required": True}))

    def __init__(self, *args, **kwargs):
        if "quiz_item" in kwargs:
            self.quiz_item = kwargs.pop("quiz_item")
        else:
            raise Exception("No quiz_item passed")

        super().__init__(*args, **kwargs)

        # Configuring answers field based on dynamically obtained
        # QuizItem object
        self._generate_answers_choices()
        self._set_question_in_label()

    def _generate_answers_choices(self):
        choices = []
        for answer in self.quiz_item.answers.all():
            choices.append((answer.pk, answer.text))

        self.fields["answers"].choices = tuple(choices)

    def _set_question_in_label(self):
        self.fields["answers"].label = (
            f"{self.quiz_item.index}. " f"{self.quiz_item.question}"
        )


class BaseQuizItemFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        """This method is used to pass quiz_item from given queryset
        to form as an argument"""

        kwargs = super().get_form_kwargs(index)
        if index is None:
            raise Exception("Invalid form index")

        kwargs["quiz_item"] = kwargs.pop("quiz_item_list")[index]

        return kwargs
