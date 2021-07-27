from django import forms


class QuizItemTryoutForm(forms.Form):

    answers = forms.ChoiceField(widget=forms.RadioSelect(attrs={"required": True}))

    def __init__(self, *args, **kwargs):
        if "quiz" in kwargs:
            quiz = kwargs.pop("quiz")
        else:
            raise Exception("No quiz passed")

        if "quiz_item_index" in kwargs:
            quiz_item_index = kwargs.pop("quiz_item_index")
            self.quiz_item = quiz.items.get(index=quiz_item_index)
        else:
            raise Exception("No quiz_item_index passed")

        super().__init__(*args, **kwargs)

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


class BaseQuizItemTryoutFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        if index is None:
            raise Exception("Invalid form index")
        kwargs["quiz_item_index"] = index + 1
        return kwargs
