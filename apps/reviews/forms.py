from django import forms

from . import models


class QuizRejectedMessageForm(forms.ModelForm):
    text = forms.CharField(
        min_length=3,
        max_length=255,
        widget=forms.Textarea,
        label="Message",
    )

    class Meta:
        model = models.QuizRejectedMessage
        fields = ("text",)
